"""
Лист «Приёмка» (gid 1168786701) — Fact: одна строка = одна клиентская приёмка (typeId=1).
"""

from __future__ import annotations

import time
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any

import gspread
import requests
from google.oauth2.service_account import Credentials as ServiceAccountCredentials

from iflat_inspection_labels import room_type_display_label
from iflat_export_color import (
    color_group_by_inspection_id,
    inspection_embed_for_mode,
    resolve_color_mode,
)
from iflat_room_metrics import CLIENT_INSPECTION_TYPE_ID, person_display
from RoomsAcceptanceColor_Refresh import (
    deal_app_label,
    deal_ddu_dkp,
    room_decoration_label,
)

SHEET_ID = 1168786701
SPREADSHEET_NAME = "УКДП-260310-Вн-Таб-CRM заселения_2026"
NCOLS = 17
LAST_COL = "R"
TAKE_DATE_FIRST_YEAR = 2025

INSPECTION_EMBED_BASE = (
    "status,responsible,user,users,room,room.house,room.house.district,"
    "room.room_type,room.decoration,room.deal,room.custom_fields,room.tags"
)
COLOR_MODE = resolve_color_mode()

FACT_HEADERS = [
    "id приёмки",
    "id помещения",
    "Адрес",
    "id дома",
    "дом",
    "жк",
    "номер помещения",
    "тип помещения",
    "номер",
    "Статус приёмки",
    "Дата проведения",
    "принимающий",
    "Тип отделки",
    "Цветовая группа",
    "ДДУ/ДКП",
    "АПП/ОАПП",
    "Кол-во",
]

SHEET_DATE_COLUMNS = ("L",)
CUTOFF_DATE = date(TAKE_DATE_FIRST_YEAR, 1, 1)


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
            if "T" in s:
                raw = s.replace("Z", "+00:00")
                try:
                    return datetime.fromisoformat(raw).date()
                except ValueError:
                    s = s.split("T", 1)[0]
            if " " in s and len(s) > 10:
                s = s.split(" ", 1)[0]
            if len(s) >= 10 and "." in s and len(s.split(".")) == 3:
                p = s.split(".")
                if len(p[0]) == 2 and len(p[2]) == 4:
                    return datetime.strptime(f"{p[0]}.{p[1]}.{p[2]}", "%d.%m.%Y").date()
            if len(s) >= 10 and s[4] == "-":
                return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None
    return None


def format_date_sheet(date_value: Any, *, missing: str = "-") -> str:
    d = parse_calendar_date(date_value)
    return d.strftime("%d.%m.%Y") if d else missing


def apply_sheet_date_formats(worksheet, end_row: int) -> None:
    if end_row < 2:
        return
    fmt = {"numberFormat": {"type": "DATE", "pattern": "dd.mm.yyyy"}}
    for col in SHEET_DATE_COLUMNS:
        worksheet.format(f"{col}2:{col}{end_row}", fmt)


def keep_inspection_for_export(insp: dict) -> bool:
    for field in ("take_date_start", "take_date", "created_at", "updated_at"):
        d = parse_calendar_date(insp.get(field))
        if d and d >= CUTOFF_DATE:
            return True
    return False


def fetch_client_inspections_history(headers: dict) -> list[dict]:
    seen: set[int] = set()
    out: list[dict] = []
    page = 1
    last_page = 1
    print("  GET /inspections typeId=1, вся история…", flush=True)
    while page <= last_page:
        r = requests.get(
            "https://YOUR_CRM_API_HOST/api/v1/inspections",
            headers=headers,
            params={
                "typeId": CLIENT_INSPECTION_TYPE_ID,
                "embed": inspection_embed_for_mode(INSPECTION_EMBED_BASE, COLOR_MODE),
                "perPage": 100,
                "page": page,
                "orderBy": "-id",
            },
            timeout=90,
        )
        r.raise_for_status()
        data = r.json()
        last_page = int((data.get("meta") or {}).get("last_page") or 1)
        for insp in data.get("data") or []:
            try:
                iid = int(insp["id"])
            except (TypeError, ValueError, KeyError):
                continue
            if iid in seen:
                continue
            seen.add(iid)
            if keep_inspection_for_export(insp):
                out.append(insp)
        if page % 20 == 0:
            print(f"    страница {page}/{last_page}, в срез: {len(out)}", flush=True)
        page += 1
    return out


def house_address_display(house: dict) -> str:
    if not house:
        return "-"
    for key in ("address", "full_address"):
        if house.get(key):
            return str(house[key])
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


def room_code(room: dict) -> str:
    """Код/номер как в iflat (tech_number и др.)."""
    for key in ("tech_number", "type_number_string", "name", "number", "id"):
        v = room.get(key)
        if v not in (None, ""):
            return str(v)
    return "-"


def inspection_status_display(insp: dict) -> str:
    st = insp.get("status") if isinstance(insp.get("status"), dict) else {}
    if (st.get("name") or "").strip():
        return str(st["name"]).strip()
    sid = insp.get("status_id")
    return f"Статус ID: {sid}" if sid is not None else "-"


def accepting_display(insp: dict) -> str:
    for src in (
        insp.get("responsible") if isinstance(insp.get("responsible"), dict) else None,
        insp.get("user") if isinstance(insp.get("user"), dict) else None,
    ):
        label = person_display(src)
        if label:
            return label
    users = insp.get("users")
    if isinstance(users, list):
        for u in users:
            label = person_display(u if isinstance(u, dict) else None)
            if label:
                return label
    return "-"


def build_fact_row(insp: dict, *, color_at_moment: str = "") -> list[Any]:
    room = insp.get("room") if isinstance(insp.get("room"), dict) else {}
    if insp.get("room_id") is not None and room.get("id") is None:
        room = {**room, "id": insp.get("room_id")}
    house = room.get("house") if isinstance(room.get("house"), dict) else {}
    rt = room.get("room_type") if isinstance(room.get("room_type"), dict) else {}
    deal = room.get("deal") if isinstance(room.get("deal"), dict) else {}
    take_raw = insp.get("take_date_start") or insp.get("take_date")

    return [
        str(insp.get("id") or "-"),
        str(room.get("id") or "-"),
        house_address_display(house),
        str(room.get("house_id") or house.get("id") or "-"),
        (house.get("name") or "-"),
        district_zhk(house),
        str(room.get("number") if room.get("number") not in (None, "") else "-"),
        room_type_display_label((rt.get("name") or "").strip() or "-", room.get("room_type_id"))
        or "-",
        room_code(room),
        inspection_status_display(insp),
        format_date_sheet(take_raw),
        accepting_display(insp),
        room_decoration_label(room),
        color_at_moment,
        deal_ddu_dkp(deal),
        deal_app_label(deal),
        1,
    ]


def parse_inspections_fact() -> None:
    start = time.time()
    print(
        f"Fact приёмки: 1 строка = 1 приёмка, цвет={COLOR_MODE}, "
        f"{len(FACT_HEADERS)} колонок, с {CUTOFF_DATE:%Y-%m-%d}",
        flush=True,
    )

    from iflat_oauth import google_service_account_path, load_iflat_oauth

    oauth = load_iflat_oauth()
    creds = google_service_account_path()
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    gs = gspread.authorize(
        ServiceAccountCredentials.from_service_account_file(str(creds), scopes=scope)
    )
    ws = gs.open(SPREADSHEET_NAME).get_worksheet_by_id(SHEET_ID)
    print(f"Лист: {ws.title} ({SHEET_ID})", flush=True)

    tok = requests.post("https://YOUR_CRM_API_HOST/api/v1/oauth/token", data=oauth, timeout=60).json()[
        "access_token"
    ]
    headers = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}

    inspections = fetch_client_inspections_history(headers)
    print(f"Клиентских приёмок в срезе: {len(inspections)}", flush=True)

    color_by_id = color_group_by_inspection_id(inspections, mode=COLOR_MODE)
    inspections.sort(
        key=lambda insp: (
            parse_calendar_date(insp.get("take_date_start") or insp.get("take_date"))
            or date.min,
            int(insp.get("id") or 0),
        ),
        reverse=True,
    )
    rows = [
        build_fact_row(
            insp,
            color_at_moment=color_by_id.get(int(insp.get("id") or 0), ""),
        )
        for insp in inspections
    ]

    ws.update([FACT_HEADERS], f"B1:{LAST_COL}1", value_input_option="USER_ENTERED")
    if rows:
        last = ws.row_count
        if last >= 2:
            ws.batch_clear([f"B2:{LAST_COL}{last}"])
        end_row = 1 + len(rows)
        if ws.row_count < end_row:
            ws.add_rows(end_row - ws.row_count)
        chunk = 1000
        for i in range(0, len(rows), chunk):
            part = rows[i : i + chunk]
            a = 2 + i
            b = a + len(part) - 1
            ws.update(part, f"B{a}:{LAST_COL}{b}", value_input_option="USER_ENTERED")
        apply_sheet_date_formats(ws, end_row)

    by_status: dict[str, int] = defaultdict(int)
    for r in rows:
        by_status[str(r[FACT_HEADERS.index("Статус приёмки")])] += 1
    top_st = sorted(by_status.items(), key=lambda x: -x[1])[:8]
    print(f"Записано {len(rows)} строк в B:{LAST_COL}", flush=True)
    print(f"  статусы (топ): {', '.join(f'{k}={v}' for k, v in top_st)}", flush=True)
    print(f"Время: {time.time() - start:.1f} сек", flush=True)


if __name__ == "__main__":
    parse_inspections_fact()
