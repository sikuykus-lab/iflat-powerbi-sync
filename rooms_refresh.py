"""
Лист комбинированного парсинга (id 1258745138):
- все помещения /rooms без фильтра по статусу;
- клиентские приёмки (typeId=1) + claims для MRK-метрик;
- «Цветовая группа» (template_b: 6/12, 11, красный по I51) и «Цвет МРК» (подсегменты).
"""

import time
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import gspread
import requests
from google.oauth2.service_account import Credentials as ServiceAccountCredentials

from iflat_deal_dates import fetch_deals_by_room_id, merged_deal_for_room
from iflat_inspection_labels import room_type_display_label
from iflat_export_color import (
    COLOR_MODE_F17,
    color_group_for_room,
    color_mrk_for_room,
    inspection_embed_for_mode,
    resolve_color_mode,
)
from iflat_room_metrics import (
    client_insp_ids_from_map,
    color_group_display_bi,
    filter_inspections_from_year,
    last_accepting_display,
    person_display,
    objects_date_sheet,
    room_mrk_metrics,
    _parse_take_date_start_field,
)

COLOR_MODE = resolve_color_mode()

SHEET_ID = 1258745138
NCOLS = 22
LAST_COL = "W"
COL_SLOT_END = 21  # "Дата последней приёмки"
SHEET_DATE_COLUMNS = ("L", "M", "U", "V", "W")

ROOMS_SHEET_HEADERS = [
    "Код",
    "ID помещения",
    "ID дома",
    "Дом",
    "Адрес",
    "ЖК",
    "Номер помещения",
    "Тип помещения",
    "Статус помещения",
    "Статус приёмки",
    "Дата ОАПП",
    "Дата АПП/АДвП",
    "АПП/ОАПП",
    "ДДУ/ДКП",
    "Кол-во приёмок",
    "Последний принимающий",
    "Тип отделки",
    "Цветовая группа",
    "Цвет МРК",
    "Дата (Объекты)",
    "Дата приёмки",
    "Дата последней приёмки",
]

_DECORATION_CANONICAL = {
    "-": "без отделки",
    "только перегородки": "отделка",
    "white box": "white box",
    "без отделки": "без отделки",
    "300": "без отделки",
    "190": "без отделки",
}

CLIENT_INSPECTION_TYPE_ID = 1
TAKE_DATE_FIRST_YEAR = 2025

# /rooms: берём все статусы.
ROOM_EMBED = "room_type,status,house,house.district,decoration,custom_fields,tags,deal"
INSP_EMBED_BASE = "status,responsible,user,room"
INSP_EMBED_WITH_CLAIMS = "status,responsible,user,room,claims.status,claims.owner"


def parse_calendar_date(date_value: Any) -> date | None:
    if not date_value or date_value in ("null", "None"):
        return None
    try:
        if isinstance(date_value, datetime):
            return date_value.date()
        if isinstance(date_value, date):
            return date_value
        if isinstance(date_value, str):
            s = date_value.strip()
            if not s or s == "-":
                return None
            if "T" in s or (len(s) > 10 and s[4] == "-" and s.count("-") >= 2):
                raw = s.replace("Z", "+00:00")
                try:
                    return datetime.fromisoformat(raw).date()
                except ValueError:
                    s = s.split("T")[0] if "T" in s else s.split(" ")[0]
            elif " " in s:
                s2 = s.split(" ")[0]
                if len(s2) >= 10 and s2[4] == "-":
                    return datetime.strptime(s2[:10], "%Y-%m-%d").date()
                s = s2
            if len(s) >= 10 and "." in s and len(s.split(".")) == 3:
                d, m, y = s.split(".")[:3]
                if len(d) == 2 and len(m) == 2 and len(y) == 4:
                    return datetime.strptime(f"{d}.{m}.{y}", "%d.%m.%Y").date()
            if len(s) >= 10 and "-" in s and len(s.split("-")) == 3:
                if s.split("-")[0].isdigit() and len(s.split("-")[0]) == 4:
                    return datetime.strptime(s[:10], "%Y-%m-%d").date()
        if isinstance(date_value, (int, float)):
            return datetime.fromtimestamp(date_value).date()
    except Exception:
        return None
    return None


def format_date_sheet(date_value: Any, *, missing: str = "-") -> str:
    d = parse_calendar_date(date_value)
    return d.strftime("%Y-%m-%d") if d else missing


def _iso_ts(s: Any) -> str:
    d = parse_calendar_date(s)
    if d:
        return d.strftime("%Y-%m-%d")
    raw = str(s or "")
    return raw[:19] if raw else ""


def apply_sheet_date_formats(worksheet, end_row: int) -> None:
    if end_row < 2:
        return
    date_fmt = {"numberFormat": {"type": "DATE", "pattern": "yyyy-mm-dd"}}
    for col in SHEET_DATE_COLUMNS:
        worksheet.format(f"{col}2:{col}{end_row}", date_fmt)


def normalize_decoration_label(raw: str) -> str:
    s = (raw or "").strip()
    if not s or s == "-":
        return "без отделки"
    return _DECORATION_CANONICAL.get(s.casefold(), s)


def _cf_collect_strings(obj, out: list[str], depth: int = 0) -> None:
    if depth > 12 or len(out) > 400:
        return
    if isinstance(obj, dict):
        for v in obj.values():
            _cf_collect_strings(v, out, depth + 1)
    elif isinstance(obj, list):
        for v in obj[:80]:
            _cf_collect_strings(v, out, depth + 1)
    elif obj is not None and str(obj).strip():
        out.append(str(obj).strip())


def room_decoration_label(room: dict) -> str:
    dec = room.get("decoration") if isinstance(room.get("decoration"), dict) else {}
    name = (dec.get("name") or "").strip()
    if name and name != "-":
        return normalize_decoration_label(name)
    chunks: list[str] = []
    for k in ("name", "title", "code"):
        v = dec.get(k)
        if v:
            chunks.append(str(v))
    tags = room.get("tags")
    if isinstance(tags, list):
        for t in tags[:20]:
            if isinstance(t, dict) and t.get("name"):
                chunks.append(str(t["name"]))
            elif isinstance(t, str):
                chunks.append(t)
    cf = room.get("custom_fields")
    if cf is not None:
        _cf_collect_strings(cf, chunks)
    blob = " ".join(chunks).lower()
    if "white" in blob and "box" in blob:
        return normalize_decoration_label("White box")
    if "перегород" in blob:
        return normalize_decoration_label("Только перегородки")
    if "без отделки" in blob:
        return normalize_decoration_label("Без отделки")
    if "только отделк" in blob or ("отделк" in blob and "перегород" not in blob and "white" not in blob):
        return normalize_decoration_label("отделка")
    if name == "-":
        return normalize_decoration_label("-")
    did = dec.get("id") if dec.get("id") is not None else room.get("decoration_id")
    if did is not None and did != "":
        return normalize_decoration_label(str(did))
    return "без отделки"


def house_address_display(house: dict) -> str:
    if not house:
        return "-"
    if house.get("address"):
        return str(house["address"])
    if house.get("full_address"):
        return str(house["full_address"])
    if house.get("street"):
        s = str(house["street"])
        if house.get("house"):
            s += f", д.{house['house']}"
        return s
    return "-"


def district_zhk(house: dict) -> str:
    if not house:
        return "-"
    d = house.get("district")
    if isinstance(d, dict) and (d.get("name") or "").strip():
        return str(d["name"]).strip()
    return "-"


def user_display(u) -> str:
    return person_display(u if isinstance(u, dict) else None)


def room_status_name(room: dict) -> str:
    st = room.get("status") if isinstance(room.get("status"), dict) else {}
    sn = (st.get("name") or "").strip()
    if sn:
        return sn
    v = room.get("status_id")
    if v is not None and str(v).strip():
        return f"Статус ID: {v}"
    return "-"


def room_code(room: dict) -> str:
    for key in ("tech_number", "type_number_string", "name", "number", "id"):
        v = room.get(key)
        if v not in (None, ""):
            return str(v)
    return "-"


def deal_ddu_dkp(deal: dict) -> str:
    if not isinstance(deal, dict):
        return ""
    v = deal.get("contract_type_id")
    if v is None or v == "":
        return ""
    try:
        ct = int(v)
    except (TypeError, ValueError):
        return ""
    if ct == 1:
        return "ДДУ"
    if ct == 2:
        return "ДКП"
    return ""


def deal_app_label(deal: dict) -> str:
    if not isinstance(deal, dict):
        return ""
    if parse_calendar_date(deal.get("one_sided_act_date")):
        return "ОАПП"
    if parse_calendar_date(deal.get("act_date")):
        return "АПП"
    return ""


def take_date_year_chunks() -> list[tuple[str, str]]:
    today = date.today()
    out: list[tuple[str, str]] = []
    for y in range(TAKE_DATE_FIRST_YEAR, today.year + 1):
        d0 = date(y, 1, 1)
        d1 = date(y, 12, 31) if y < today.year else today
        out.append((d0.strftime("%d.%m.%Y"), d1.strftime("%d.%m.%Y")))
    return out


def settlement_slot_end(take_from: str, take_to: str) -> str:
    if take_to and take_to != "-":
        return take_to
    if take_from and take_from != "-":
        return take_from
    return "-"


def fetch_inspection_status_maps(headers: dict) -> tuple[dict[int, str], dict[str, set[int]]]:
    status_map: dict[int, str] = {}
    groups = {"new": set(), "cancelled": set(), "not_accepted": set()}
    try:
        r = requests.get("https://YOUR_CRM_API_HOST/api/v1/inspections/statuses", headers=headers, timeout=60)
        r.raise_for_status()
        rows = r.json() if isinstance(r.json(), list) else []
    except Exception:
        rows = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        sid = row.get("id")
        name = (row.get("name") or "").strip()
        if sid is None:
            continue
        try:
            sid_i = int(sid)
        except (TypeError, ValueError):
            continue
        status_map[sid_i] = name
        low = name.lower()
        if "нов" in low:
            groups["new"].add(sid_i)
        if "отмен" in low:
            groups["cancelled"].add(sid_i)
        if "не принят" in low:
            groups["not_accepted"].add(sid_i)
    return status_map, groups


def aggregate_insp_history(headers: dict, chunks: list[tuple[str, str]], status_map: dict[int, str], groups: dict[str, set[int]]) -> dict[str, dict]:
    by_room: dict[str, dict] = {}
    seen: set[int] = set()
    for take_from, take_to in chunks:
        page = 1
        last = 1
        while page <= last:
            r = requests.get(
                "https://YOUR_CRM_API_HOST/api/v1/inspections",
                headers=headers,
                params={
                    "typeId": CLIENT_INSPECTION_TYPE_ID,
                    "perPage": 100,
                    "page": page,
                    "embed": INSP_EMBED_BASE,
                    "orderBy": "-id",
                    "takeDateFrom": take_from,
                    "takeDateTo": take_to,
                },
                timeout=90,
            )
            r.raise_for_status()
            data = r.json()
            meta = data.get("meta") or {}
            last = int(meta.get("last_page") or 1)
            for insp in data.get("data") or []:
                iid = insp.get("id")
                try:
                    iid_i = int(iid)
                except (TypeError, ValueError):
                    continue
                if iid_i in seen:
                    continue
                seen.add(iid_i)
                room = insp.get("room") if isinstance(insp.get("room"), dict) else {}
                rid = room.get("id") or insp.get("room_id")
                if rid is None:
                    continue
                key = str(rid)
                cur = by_room.setdefault(
                    key,
                    {
                        "count": 0,
                        "last_ts": "",
                        "last_status_id": None,
                        "last_status_name": "",
                        "last_user": "",
                        "has_not_accepted": False,
                        "has_cancelled": False,
                        "has_new": False,
                    },
                )
                cur["count"] += 1
                sid = insp.get("status_id")
                try:
                    sid_i = int(sid)
                except (TypeError, ValueError):
                    sid_i = None
                sname = ""
                st = insp.get("status") if isinstance(insp.get("status"), dict) else {}
                if st.get("name"):
                    sname = str(st.get("name")).strip()
                elif sid_i is not None:
                    sname = status_map.get(sid_i, f"Статус ID: {sid_i}")

                if sid_i is not None:
                    if sid_i in groups["not_accepted"] or "не принят" in sname.lower():
                        cur["has_not_accepted"] = True
                    if sid_i in groups["cancelled"] or "отмен" in sname.lower():
                        cur["has_cancelled"] = True
                    if sid_i in groups["new"] or "нов" in sname.lower():
                        cur["has_new"] = True

                uts = _iso_ts(insp.get("updated_at") or insp.get("take_date_end") or "")
                if uts >= cur["last_ts"]:
                    cur["last_ts"] = uts
                    cur["last_status_id"] = sid_i
                    cur["last_status_name"] = sname
                    ru = insp.get("responsible") if isinstance(insp.get("responsible"), dict) else {}
                    uu = insp.get("user") if isinstance(insp.get("user"), dict) else {}
                    cur["last_user"] = user_display(ru) or user_display(uu) or cur["last_user"]
            page += 1
    return by_room


def aggregate_client_inspections_map(
    headers: dict,
    chunks: list[tuple[str, str]] | None = None,
) -> dict[int, list]:
    """Клиентские приёмки с claims. chunks — пары takeDateFrom/To (в прогоне: с 2025 по годам)."""
    by_room: dict[int, list] = defaultdict(list)
    seen: set[int] = set()
    date_ranges: list[tuple[str, str] | None] = (
        list(chunks) if chunks is not None else [None]
    )
    for take_range in date_ranges:
        page = 1
        last = 1
        while page <= last:
            params: dict = {
                "typeId": CLIENT_INSPECTION_TYPE_ID,
                "perPage": 100,
                "page": page,
                "embed": INSP_EMBED_WITH_CLAIMS,
                "orderBy": "-id",
            }
            if take_range is not None:
                take_from, take_to = take_range
                params["takeDateFrom"] = take_from
                params["takeDateTo"] = take_to
            r = requests.get(
                "https://YOUR_CRM_API_HOST/api/v1/inspections",
                headers=headers,
                params=params,
                timeout=90,
            )
            r.raise_for_status()
            data = r.json()
            meta = data.get("meta") or {}
            last = int(meta.get("last_page") or 1)
            for insp in data.get("data") or []:
                try:
                    iid_i = int(insp.get("id"))
                except (TypeError, ValueError):
                    continue
                if iid_i in seen:
                    continue
                seen.add(iid_i)
                room = insp.get("room") if isinstance(insp.get("room"), dict) else {}
                rid = room.get("id") or insp.get("room_id")
                if rid is None:
                    continue
                try:
                    by_room[int(rid)].append(insp)
                except (TypeError, ValueError):
                    continue
            page += 1
    return dict(by_room)


def insp_history_from_map(
    insp_map: dict[int, list],
    status_map: dict[int, str],
    groups: dict[str, set[int]],
) -> dict[str, dict]:
    """Агрегат для legacy «Цвет iflat» из полной карты приёмок."""
    by_room: dict[str, dict] = {}
    for rid, insps in insp_map.items():
        key = str(rid)
        cur = {
            "count": 0,
            "last_ts": "",
            "last_status_id": None,
            "last_status_name": "",
            "last_user": "",
            "has_not_accepted": False,
            "has_cancelled": False,
            "has_new": False,
        }
        for insp in insps:
            cur["count"] += 1
            sid = insp.get("status_id")
            try:
                sid_i = int(sid)
            except (TypeError, ValueError):
                sid_i = None
            sname = ""
            st = insp.get("status") if isinstance(insp.get("status"), dict) else {}
            if st.get("name"):
                sname = str(st.get("name")).strip()
            elif sid_i is not None:
                sname = status_map.get(sid_i, f"Статус ID: {sid_i}")
            if sid_i is not None:
                if sid_i in groups["not_accepted"] or "не принят" in sname.lower():
                    cur["has_not_accepted"] = True
                if sid_i in groups["cancelled"] or "отмен" in sname.lower():
                    cur["has_cancelled"] = True
                if sid_i in groups["new"] or "нов" in sname.lower():
                    cur["has_new"] = True
            uts = _iso_ts(insp.get("updated_at") or insp.get("take_date_end") or "")
            if uts >= cur["last_ts"]:
                cur["last_ts"] = uts
                cur["last_status_id"] = sid_i
                cur["last_status_name"] = sname
                ru = insp.get("responsible") if isinstance(insp.get("responsible"), dict) else {}
                uu = insp.get("user") if isinstance(insp.get("user"), dict) else {}
                cur["last_user"] = user_display(ru) or user_display(uu) or cur["last_user"]
        by_room[key] = cur
    return by_room


def fetch_all_rooms(headers: dict) -> list[dict]:
    by_room: dict[str, dict] = {}
    page = 1
    last = 1
    while page <= last:
        r = requests.get(
            "https://YOUR_CRM_API_HOST/api/v1/rooms",
            headers=headers,
            params={"embed": ROOM_EMBED, "orderBy": "-updated_at", "perPage": 100, "page": page},
            timeout=90,
        )
        r.raise_for_status()
        payload = r.json()
        meta = payload.get("meta") or {}
        last = int(meta.get("last_page") or 1)
        for room in payload.get("data") or []:
            if not isinstance(room, dict):
                continue
            rid = room.get("id")
            if rid is None:
                continue
            k = str(rid)
            prev = by_room.get(k)
            cur_ts = _iso_ts(room.get("updated_at") or "")
            prev_ts = _iso_ts(prev.get("updated_at") or "") if isinstance(prev, dict) else ""
            if prev is None or cur_ts >= prev_ts:
                by_room[k] = room
        page += 1
    return list(by_room.values())


def _status_tokens(text: str) -> set[str]:
    t = (text or "").lower().replace("ё", "е")
    out = set()
    if "в процессе" in t:
        out.add("in_process")
    if "открыта запись" in t:
        out.add("open_record")
    if "замечан" in t:
        out.add("remarks")
    if "приемка отмен" in t or "приёмка отмен" in t:
        out.add("acceptance_cancelled")
    if "принято с замеч" in t:
        out.add("accepted_remarks")
    if "принято" in t:
        out.add("accepted")
    return out


def classify_color(room_status: str, insp: dict) -> str:
    tok = _status_tokens(room_status)
    if "accepted_remarks" in tok:
        return "СИНИЙ"
    if "accepted" in tok and "accepted_remarks" not in tok:
        return "ЗЕЛЕНЫЙ"
    if "acceptance_cancelled" in tok:
        return "КРАСНЫЙ"

    has_not = bool(insp.get("has_not_accepted"))
    has_cancel = bool(insp.get("has_cancelled"))
    has_new = bool(insp.get("has_new"))
    in_process = "in_process" in tok
    open_record = "open_record" in tok
    remarks = "remarks" in tok

    if in_process and has_not and has_cancel and has_new:
        return "КРАСНЫЙ"
    if remarks and has_cancel and has_not:
        return "КРАСНЫЙ"
    if open_record and has_not and not has_new:
        return "КРАСНЫЙ"
    if (in_process or open_record) and int(insp.get("count", 0) or 0) == 0:
        return "ПРИЁМКА НЕ ОСУЩЕСТВЛЯЛАСЬ"
    return ""


def inspection_status_text(room_status: str, insp: dict) -> str:
    cnt = int(insp.get("count", 0) or 0)
    if cnt > 0:
        s = (insp.get("last_status_name") or "").strip()
        return s or "-"
    tok = _status_tokens(room_status)
    if "in_process" in tok or "open_record" in tok:
        return "Приёмка не осуществлялась"
    return "-"


def build_room_export_rows(
    room: dict,
    insp_history: dict[str, dict],
    deals_by_room: dict[int, dict] | None = None,
    *,
    insp_map: dict[int, list] | None = None,
    client_insp_ids: frozenset[int] | None = None,
) -> list[list[Any]]:
    deal = merged_deal_for_room(room, deals_by_room)
    house = room.get("house") if isinstance(room.get("house"), dict) else {}
    rt = room.get("room_type") if isinstance(room.get("room_type"), dict) else {}

    room_id = str(room.get("id", "")) if room.get("id") else "-"
    hid = room.get("house_id", "")
    house_name = house.get("name") or "-"
    addr = house_address_display(house)
    zhk = district_zhk(house)
    room_number = room.get("number") if room.get("number") not in (None, "") else "-"
    room_type = room_type_display_label((rt.get("name") or "").strip() or "-", room.get("room_type_id")) or "-"
    status_name = room_status_name(room)

    inf = insp_history.get(room_id, {})
    insp_status = inspection_status_text(status_name, inf)

    one_sided = format_date_sheet(deal.get("one_sided_act_date")) if deal else "-"
    act_date = format_date_sheet(deal.get("act_date")) if deal else "-"
    app_lbl = deal_app_label(deal)
    ddkp = deal_ddu_dkp(deal)

    take_from = format_date_sheet(room.get("take_date_from"))
    take_to = format_date_sheet(room.get("take_date_to"))
    slot_end = settlement_slot_end(take_from, take_to)

    rid_i = room.get("id")
    insps_full = []
    if insp_map is not None and rid_i is not None:
        try:
            insps_full = insp_map.get(int(rid_i), [])
        except (TypeError, ValueError):
            insps_full = []

    insps_mrk = filter_inspections_from_year(insps_full, TAKE_DATE_FIRST_YEAR)
    mrk = room_mrk_metrics(room, insps_mrk, client_insp_ids)
    if COLOR_MODE == COLOR_MODE_F17:
        color_group = color_group_display_bi(mrk["color_group"])
    else:
        color_group = color_group_for_room(
            room, insps_mrk, mode=COLOR_MODE, client_insp_ids=client_insp_ids
        )
    color_mrk = color_mrk_for_room(room, insps_mrk, client_insp_ids)
    # Статус последней приёмки — по updated_at / take_date_end.
    if inf.get("last_status_id") not in (None, ""):
        mrk["insp_last_status_id"] = inf["last_status_id"]
    base = [
        room_code(room),
        room_id,
        str(hid) if hid else "-",
        house_name,
        addr,
        zhk,
        room_number,
        room_type,
        status_name,
        insp_status,
        one_sided,
        act_date,
        app_lbl,
        ddkp,
        int(inf.get("count", 0) or 0),
        last_accepting_display(insps_full) if insps_full else (inf.get("last_user") or "-"),
        room_decoration_label(room),
        color_group,
        color_mrk,
        objects_date_sheet(insps_full),
        take_from,
        slot_end,
    ]
    return [base]


def parse_rooms_acceptance_color():
    start_time = time.time()

    from iflat_oauth import google_service_account_path, load_iflat_oauth

    data = load_iflat_oauth()
    creds = str(google_service_account_path())
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_service_account_file(
        creds,
        scopes=scope,
    )
    gs = gspread.authorize(credentials)
    ss = gs.open("УКДП-260310-Вн-Таб-CRM заселения_2026")
    worksheet = ss.get_worksheet_by_id(SHEET_ID)
    print(f"Лист найден: {worksheet.title}, цвет={COLOR_MODE}", flush=True)

    tok = requests.post("https://YOUR_CRM_API_HOST/api/v1/oauth/token", data, timeout=60).json()["access_token"]
    headers = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}
    print("Подключение к CRM установлено", flush=True)

    status_map, groups = fetch_inspection_status_maps(headers)
    print(f"Справочник статусов приёмки: {len(status_map)}", flush=True)

    print("Объекты /rooms (все статусы, без дублей)…", flush=True)
    rooms = fetch_all_rooms(headers)
    print(f"Уникальных помещений: {len(rooms)}", flush=True)

    chunks = take_date_year_chunks()
    print(
        f"Клиентские приёмки + claims (проход по годам с {TAKE_DATE_FIRST_YEAR}, "
        f"{len(chunks)} периодов)…",
        flush=True,
    )
    t_insp = time.time()
    insp_map = aggregate_client_inspections_map(headers, chunks)
    insp_map_mrk = {
        rid: filter_inspections_from_year(arr, TAKE_DATE_FIRST_YEAR)
        for rid, arr in insp_map.items()
    }
    client_insp_ids = client_insp_ids_from_map(insp_map_mrk)
    insp_history = insp_history_from_map(insp_map, status_map, groups)
    print(
        f"  приёмки загружены за {time.time() - t_insp:.1f} сек; "
        f"room_id с приёмками: {len(insp_map)}, записей: {sum(len(v) for v in insp_map.values())}, "
        f"с {TAKE_DATE_FIRST_YEAR}+ для MRK: {sum(len(v) for v in insp_map_mrk.values())}, "
        f"клиентских inspection_id: {len(client_insp_ids)}",
        flush=True,
    )

    print("Сделки GET /deals (АПП/ОАПП)…", flush=True)
    deals_by_room = fetch_deals_by_room_id(headers=headers)
    print(f"room_id со сделкой: {len(deals_by_room)}", flush=True)

    all_rows: list[list[Any]] = []
    for room in rooms:
        try:
            all_rows.extend(
                build_room_export_rows(
                    room,
                    insp_history,
                    deals_by_room,
                    insp_map=insp_map,
                    client_insp_ids=client_insp_ids,
                )
            )
        except Exception as e:
            print(f"ошибка room {room.get('id')}: {e}", flush=True)

    worksheet.update([ROOMS_SHEET_HEADERS], f"B1:{LAST_COL}1", value_input_option="USER_ENTERED")

    if not all_rows:
        print("Нет данных для записи", flush=True)
        return

    all_rows.sort(key=lambda x: x[COL_SLOT_END] if x[COL_SLOT_END] != "-" else "", reverse=True)

    last_row = max(worksheet.row_count, 2)
    if last_row >= 2:
        worksheet.batch_clear([f"B2:{LAST_COL}{last_row}"])

    start_row = 2
    end_row = start_row + len(all_rows) - 1
    if worksheet.row_count < end_row:
        worksheet.add_rows(end_row - worksheet.row_count)
    chunk = 1000
    for i in range(0, len(all_rows), chunk):
        part = all_rows[i : i + chunk]
        a = start_row + i
        b = a + len(part) - 1
        try:
            worksheet.update(part, f"B{a}:{LAST_COL}{b}", value_input_option="USER_ENTERED")
        except TypeError:
            worksheet.update(part, f"B{a}:{LAST_COL}{b}", raw=False)

    apply_sheet_date_formats(worksheet, end_row)

    idx_group = ROOMS_SHEET_HEADERS.index("Цветовая группа")
    idx_mrk = ROOMS_SHEET_HEADERS.index("Цвет МРК")

    def _cnt_color(rows, col_idx, val):
        return sum(1 for r in rows if r[col_idx] == val)

    empty_group = sum(1 for r in all_rows if not (r[idx_group] or "").strip())

    print(f"Записано {len(all_rows)} строк в B:{LAST_COL} ({NCOLS} колонок)", flush=True)
    print(
        f"Цветовая группа ({COLOR_MODE}): "
        f"Зелёный={_cnt_color(all_rows, idx_group, 'Зелёный')}, "
        f"Синий={_cnt_color(all_rows, idx_group, 'Синий')}, "
        f"Красный={_cnt_color(all_rows, idx_group, 'Красный')}, "
        f"без группы={empty_group}",
        flush=True,
    )
    mrk_colors: dict[str, int] = {}
    for r in all_rows:
        c = r[idx_mrk] or "(пусто)"
        mrk_colors[c] = mrk_colors.get(c, 0) + 1
    top_mrk = ", ".join(f"{k}={v}" for k, v in sorted(mrk_colors.items(), key=lambda x: -x[1])[:8])
    print(f"Цвет МРК: {top_mrk}", flush=True)
    idx_hid = ROOMS_SHEET_HEADERS.index("ID дома")
    idx_rid = ROOMS_SHEET_HEADERS.index("ID помещения")
    idx_type = ROOMS_SHEET_HEADERS.index("Тип помещения")
    for hid, label in (("4662", "11_к3"), ("4824", "17_к3")):
        rows_h = [r for r in all_rows if str(r[idx_hid]) == hid]
        apt = [
            r
            for r in rows_h
            if "квартир" in str(r[idx_type]).lower()
            or "апарт" in str(r[idx_type]).lower()
        ]
        uniq = len({str(r[idx_rid]) for r in apt if r[idx_rid]})
        print(
            f"  {label} (id {hid}): строк={len(rows_h)}, квартир={len(apt)}, уник. ID={uniq}",
            flush=True,
        )
    print(f"Время: {time.time() - start_time:.1f} сек", flush=True)


if __name__ == "__main__":
    parse_rooms_acceptance_color()
