"""
Метрики помещения для BI / лист iflat — логика MRK (parser_template_a) + заявки на клиентской приёмке.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime

import requests

CLIENT_INSPECTION_TYPE_ID = 1
INSP_NOT_ACCEPTED = 5
MRK_GREEN_STATUSES = frozenset({6, 12})
MRK_BLUE_STATUS = 11
MRK_ACCEPTED_STATUSES = frozenset({6, 11, 12})
MRK_RED_UPS_ROOM_STATUSES = frozenset({2, 4})
MRK_CLAIMS_INWORK = frozenset({1, 2, 8})
MRK_CLAIMS_DONE = frozenset({9, 3})
CLAIM_STATUS_UPS_REVIEW = "на проверке"
CLAIM_STATUS_DONE = frozenset({"выполнено", "закрыто без выполнения"})
CLAIM_STATUS_RED_UPS = "выполнено"
CLAIM_BASIS_OWNER_TYPE = "inspection"


def _parse_insp_calendar_day(insp: dict) -> date | None:
    for field in ("take_date_end", "take_date_from", "updated_at", "created_at"):
        raw = insp.get(field)
        if not raw:
            continue
        s = str(raw).strip()
        if not s:
            continue
        if "T" in s:
            s = s.split("T", 1)[0]
        elif " " in s and len(s) > 10:
            s = s.split(" ", 1)[0]
        for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
            try:
                return datetime.strptime(s[:10], fmt).date()
            except ValueError:
                continue
    return None


def _dedupe_inspections(inspections: list) -> list:
    by_id: dict[int, dict] = {}
    for insp in inspections:
        try:
            by_id[int(insp.get("id"))] = insp
        except (TypeError, ValueError):
            continue
    return list(by_id.values())


def _sort_inspections_chronologically(inspections: list) -> list:
    def _key(i: dict):
        d = _parse_insp_calendar_day(i)
        return (d or date.min, int(i.get("id") or 0))

    return sorted(_dedupe_inspections(inspections), key=_key)


def _latest_inspection(inspections: list) -> dict | None:
    ordered = _sort_inspections_chronologically(inspections)
    return ordered[-1] if ordered else None


def _parse_take_date_field(insp: dict, field: str) -> date | None:
    raw = insp.get(field)
    if not raw:
        return None
    s = str(raw).strip()
    if not s:
        return None
    if "T" in s:
        s = s.split("T", 1)[0]
    elif " " in s and len(s) > 10:
        s = s.split(" ", 1)[0]
    for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(s[:10], fmt).date()
        except ValueError:
            continue
    return None


def _parse_take_date_start_field(insp: dict) -> date | None:
    return _parse_take_date_field(insp, "take_date_start")


def _parse_take_date_end_field(insp: dict) -> date | None:
    return _parse_take_date_field(insp, "take_date_end")


def _sort_inspections_by_start(inspections: list) -> list:
    def _key(i: dict):
        d = _parse_take_date_start_field(i)
        return (d or date.min, int(i.get("id") or 0))

    return sorted(_dedupe_inspections(inspections), key=_key)


def _latest_inspection_by_start(inspections: list) -> dict | None:
    ordered = _sort_inspections_by_start(inspections)
    return ordered[-1] if ordered else None


def execution_date_range(insps: list) -> tuple[str, str]:
    """
    «Дата приёмки с / по» на листе iflat: min и max take_date_start (проведение).
    Как в «Объекты» f11 (481 в апреле): интервал [с, по] пересекает месяц
    (с <= конец месяца и по >= начало). Только «по» в диапазоне месяца = 456.
    """
    days: list[date] = []
    for insp in _dedupe_inspections(insps):
        if int(insp.get("type_id") or 0) != CLIENT_INSPECTION_TYPE_ID:
            continue
        d = _parse_take_date_start_field(insp)
        if d:
            days.append(d)
    if not days:
        return "-", "-"
    d_min, d_max = min(days), max(days)
    return d_min.strftime("%Y-%m-%d"), d_max.strftime("%Y-%m-%d")


def execution_date_end(insps: list) -> str:
    """Устар.: max take_date_start. Для листа iflat — acceptance_date_to()."""
    return execution_date_range(insps)[1]


def objects_date_sheet(insps: list) -> str:
    """
    Одна дата на строку iflat: max take_date_start по последнему месяцу с приёмкой.
    Помесячный счёт как в «Объекты» — лист «Приёмка» (1 строка = 1 приёмка).
    """
    months = objects_dates_by_month(insps)
    if not months:
        return "-"
    return months[-1][1]


def objects_dates_by_month(insps: list) -> list[tuple[tuple[int, int], str]]:
    """
    Помесячные даты для «Объекты» (takeDateFrom/To по take_date_start):
    на каждый месяц с приёмкой — max take_date_start в этом месяце.
    """
    by_month: dict[tuple[int, int], list[date]] = defaultdict(list)
    for insp in _dedupe_inspections(insps):
        if int(insp.get("type_id") or 0) != CLIENT_INSPECTION_TYPE_ID:
            continue
        ds = _parse_take_date_start_field(insp)
        if ds:
            by_month[(ds.year, ds.month)].append(ds)
    return [
        (ym, max(by_month[ym]).strftime("%Y-%m-%d"))
        for ym in sorted(by_month.keys())
    ]


def person_display(u: dict | None) -> str:
    """ФИО из embed responsible/user (CRM часто отдаёт last_name + first_name)."""
    if not isinstance(u, dict):
        return ""
    for key in ("full_name", "fio", "name", "username", "email"):
        v = u.get(key)
        if v and str(v).strip():
            return str(v).strip()
    parts = [u.get("last_name"), u.get("first_name"), u.get("middle_name")]
    joined = " ".join(str(p).strip() for p in parts if p and str(p).strip())
    return joined


def accepting_from_inspection(insp: dict) -> str:
    """Принимающий по одной приёмке: responsible, user, users[]."""
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
    return ""


def _best_client_insp_by_start(
    insps: list,
    *,
    year: int | None = None,
    month: int | None = None,
) -> dict | None:
    best_insp: dict | None = None
    best_start = date.min
    for insp in _dedupe_inspections(insps):
        if int(insp.get("type_id") or 0) != CLIENT_INSPECTION_TYPE_ID:
            continue
        ds = _parse_take_date_start_field(insp) or _parse_insp_calendar_day(insp)
        if not ds:
            continue
        if year is not None and month is not None and (ds.year, ds.month) != (year, month):
            continue
        if ds < best_start:
            continue
        best_start = ds
        best_insp = insp
    return best_insp


def last_accepting_display(insps: list) -> str:
    """Последний принимающий — по приёмке с max take_date_start."""
    best_insp = _best_client_insp_by_start(insps)
    if not best_insp:
        return "-"
    return accepting_from_inspection(best_insp) or "-"


def accepting_for_month_display(insps: list, year: int, month: int) -> str:
    """Принимающий по приёмке с max take_date_start в календарном месяце."""
    best_insp = _best_client_insp_by_start(insps, year=year, month=month)
    if not best_insp:
        return "-"
    return accepting_from_inspection(best_insp) or "-"


def filter_inspections_from_year(insps: list, first_year: int = 2025) -> list:
    """Для MRK/истории — только приёмки с датой проведения с first_year."""
    cutoff = date(first_year, 1, 1)
    out: list[dict] = []
    for insp in _dedupe_inspections(insps):
        d = _parse_take_date_start_field(insp) or _parse_insp_calendar_day(insp)
        if d and d >= cutoff:
            out.append(insp)
    return out


def _insp_status_id(insp: dict) -> int | None:
    try:
        return int(insp.get("status_id"))
    except (TypeError, ValueError):
        return None


def _norm_status_text(value) -> str:
    return str(value or "").strip().lower()


def _claim_status_name(claim: dict) -> str:
    st = claim.get("status") if isinstance(claim.get("status"), dict) else {}
    return _norm_status_text(st.get("name"))


def client_insp_ids_from_map(insp_map: dict) -> frozenset[int]:
    ids: set[int] = set()
    for insps in insp_map.values():
        for insp in _dedupe_inspections(insps):
            try:
                if int(insp.get("type_id") or 0) == CLIENT_INSPECTION_TYPE_ID:
                    ids.add(int(insp["id"]))
            except (TypeError, ValueError, KeyError):
                continue
    return frozenset(ids)


def _is_client_inspection_basis_claim(
    claim: dict,
    insp: dict,
    client_insp_ids: frozenset[int] | None = None,
) -> bool:
    if str(claim.get("owner_type") or "").strip().lower() != CLAIM_BASIS_OWNER_TYPE:
        return False
    owner = claim.get("owner") if isinstance(claim.get("owner"), dict) else {}
    owner_type_id = owner.get("type_id")
    if owner_type_id is not None:
        try:
            return int(owner_type_id) == CLIENT_INSPECTION_TYPE_ID
        except (TypeError, ValueError):
            return False
    try:
        owner_id = int(claim.get("owner_id"))
    except (TypeError, ValueError):
        return False
    if client_insp_ids is not None:
        return owner_id in client_insp_ids
    try:
        return (
            owner_id == int(insp.get("id"))
            and int(insp.get("type_id") or 0) == CLIENT_INSPECTION_TYPE_ID
        )
    except (TypeError, ValueError):
        return False


def _claims_on_client_inspections(
    insps: list,
    client_insp_ids: frozenset[int] | None = None,
) -> list[tuple[dict, dict]]:
    pairs: list[tuple[dict, dict]] = []
    for insp in _dedupe_inspections(insps):
        if int(insp.get("type_id") or 0) != CLIENT_INSPECTION_TYPE_ID:
            continue
        for claim in insp.get("claims") or []:
            if isinstance(claim, dict) and _is_client_inspection_basis_claim(
                claim, insp, client_insp_ids
            ):
                pairs.append((insp, claim))
    return pairs


def _is_red_pool(insps: list) -> bool:
    latest = _latest_inspection(insps)
    return bool(latest and _insp_status_id(latest) == INSP_NOT_ACCEPTED)


def _is_red_mrk_history(insps: list) -> bool:
    """template_b I51: любая клиентская приёмка «Не принята» в истории."""
    return any(
        _insp_status_id(i) == INSP_NOT_ACCEPTED for i in _dedupe_inspections(insps)
    )


_is_red_f17 = _is_red_mrk_history


def _is_red_done(room: dict, insps: list) -> bool:
    if room.get("status_id") not in MRK_ACCEPTED_STATUSES:
        return False
    return _is_red_mrk_history(insps)


def _red_has_claim_ups(room: dict, insps: list, client_insp_ids: frozenset[int] | None) -> bool:
    if not _is_red_pool(insps):
        return False
    if room.get("status_id") not in MRK_RED_UPS_ROOM_STATUSES:
        return False
    latest = _latest_inspection(insps)
    if not latest:
        return False
    for _, claim in _claims_on_client_inspections([latest], client_insp_ids):
        if _claim_status_name(claim) == CLAIM_STATUS_RED_UPS:
            return True
        if claim.get("status_id") in MRK_CLAIMS_DONE:
            return True
    return False


def classify_blue_bucket_mrk(room: dict, insps: list) -> str:
    if room.get("status_id") != MRK_BLUE_STATUS:
        return ""
    has_inwork = has_done = False
    for insp in insps:
        for claim in insp.get("claims") or []:
            sid = claim.get("status_id")
            if sid in MRK_CLAIMS_INWORK:
                has_inwork = True
            elif sid in MRK_CLAIMS_DONE:
                has_done = True
    if has_done and not has_inwork:
        return "передано"
    return "в_работе"


def classify_color_mrk(room: dict, insps: list, client_insp_ids: frozenset[int] | None) -> str:
    """Подсегмент MRK (как parser_template_b): зелёный / синий / красный_*."""
    sid = room.get("status_id")
    if sid in MRK_GREEN_STATUSES:
        return "ЗЕЛЁНЫЙ"
    if sid == MRK_BLUE_STATUS:
        return "СИНИЙ"
    if not _is_red_f17(insps):
        return ""
    if _is_red_done(room, insps):
        return "КРАСНЫЙ_УСТРАНЕНО"
    if _red_has_claim_ups(room, insps, client_insp_ids):
        return "КРАСНЫЙ_УПС"
    return "КРАСНЫЙ"


def classify_color_group_template_b(room: dict, insps: list) -> str:
    """Цветовая группа для BI: те же приоритеты, что template_b (6/12, 11, красный по I51)."""
    sid = room.get("status_id")
    if sid in MRK_GREEN_STATUSES:
        return "ЗЕЛЁНЫЙ"
    if sid == MRK_BLUE_STATUS:
        return "СИНИЙ"
    if _is_red_f17(insps):
        return "КРАСНЫЙ"
    return ""


def color_group_display_bi(raw: str) -> str:
    """Подпись для листов BI: Красный / Синий / Зелёный."""
    return {
        "КРАСНЫЙ": "Красный",
        "СИНИЙ": "Синий",
        "ЗЕЛЁНЫЙ": "Зелёный",
    }.get((raw or "").strip(), "")


def _room_from_inspection(insp: dict) -> dict:
    room = insp.get("room") if isinstance(insp.get("room"), dict) else {}
    if insp.get("room_id") is not None and room.get("id") is None:
        room = {**room, "id": insp.get("room_id")}
    return room


def classify_color_group_at_inspection(room: dict, prefix: list) -> str:
    """
    Цвет на момент приёмки (лист Fact):
    1) красный — I51: в префиксе была «Не принята» (status_id=5);
    2) зел/син — по последней приёмке в префиксе (4 / 8);
    3) иначе — как f17 по текущему status_id помещения в embed.
    """
    if _is_red_f17(prefix):
        return "КРАСНЫЙ"
    latest = _latest_inspection_by_start(prefix)
    if latest:
        isid = _insp_status_id(latest)
        if isid == 4:
            return "ЗЕЛЁНЫЙ"
        if isid == 8:
            return "СИНИЙ"
        if isid == INSP_NOT_ACCEPTED:
            return "КРАСНЫЙ"
    return classify_color_group_template_b(room, prefix)


def count_claims(insps: list, client_insp_ids: frozenset[int] | None) -> tuple[int, int, int]:
    """Всего / inwork / done по клиентским приёмкам."""
    total = inwork = done = 0
    for _, claim in _claims_on_client_inspections(insps, client_insp_ids):
        total += 1
        sid = claim.get("status_id")
        if sid in MRK_CLAIMS_INWORK:
            inwork += 1
        elif sid in MRK_CLAIMS_DONE:
            done += 1
    return total, inwork, done


def load_client_inspections_map(headers: dict, room_ids: list[int]) -> dict[int, list]:
    result: dict[int, list] = defaultdict(list)
    for i in range(0, len(room_ids), 50):
        chunk = room_ids[i : i + 50]
        ids_param = ",".join(str(rid) for rid in chunk)
        page = 1
        last_page = 1
        while page <= last_page:
            r = requests.get(
                "https://YOUR_CRM_API_HOST/api/v1/inspections",
                headers=headers,
                params={
                    "roomId": ids_param,
                    "typeId": CLIENT_INSPECTION_TYPE_ID,
                    "embed": "status,responsible,user,users,claims.status,claims.owner",
                    "perPage": 100,
                    "page": page,
                },
                timeout=90,
            )
            r.raise_for_status()
            data = r.json()
            last_page = int((data.get("meta") or {}).get("last_page") or 1)
            for insp in data.get("data") or []:
                try:
                    result[int(insp.get("room_id"))].append(insp)
                except (TypeError, ValueError):
                    continue
            page += 1
    return dict(result)


def room_mrk_metrics(
    room: dict,
    insps: list,
    client_insp_ids: frozenset[int] | None,
) -> dict:
    latest = _latest_inspection(insps)
    claims_total, claims_inwork, claims_done = count_claims(insps, client_insp_ids)
    red_pool = _is_red_pool(insps)
    return {
        "insp_count": len(_dedupe_inspections(insps)),
        "insp_last_status_id": _insp_status_id(latest) if latest else "",
        "red_pool": "да" if red_pool else "",
        "red_history": "да" if _is_red_mrk_history(insps) else "",
        "red_done": "да" if _is_red_done(room, insps) else "",
        "red_ups": "да" if _red_has_claim_ups(room, insps, client_insp_ids) else "",
        "red_inwork": (
            "да"
            if red_pool
            and not _is_red_done(room, insps)
            and not _red_has_claim_ups(room, insps, client_insp_ids)
            else ""
        ),
        "blue_bucket": classify_blue_bucket_mrk(room, insps),
        "color_mrk": classify_color_mrk(room, insps, client_insp_ids),
        "color_group": classify_color_group_template_b(room, insps),
        "claims_total": claims_total,
        "claims_inwork": claims_inwork,
        "claims_done": claims_done,
    }
