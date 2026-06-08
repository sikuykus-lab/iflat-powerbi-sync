#!/usr/bin/env python3
"""
Чтение данных CRM для выгрузки в Google Sheets / Power BI.

Сеть:
  - POST /api/v1/oauth/token — только получение токена.
  - GET  — все запросы к ресурсам.

Секреты (без хардкода): переменные окружения или файл JSON:
  CRM_SECRETS_JSON — путь к файлу вида:
    {"username":"...","password":"...","account_id":379,"client_id":2,
     "client_secret":"...","grant_type":"login"}

  или отдельно: CRM_USERNAME, CRM_PASSWORD, CRM_ACCOUNT_ID,
  CRM_CLIENT_ID, CRM_CLIENT_SECRET

Примеры:
  python3 iflat_bi_readonly_pipeline.py --refs --out-dir ./iflat_export
  python3 iflat_bi_readonly_pipeline.py --rooms --status-ids 6,11,12 --out-dir ./iflat_export
  python3 iflat_bi_readonly_pipeline.py --inspections --inspection-type client \\
    --take-from 01.01.2026 --take-to 31.12.2026 --out-dir ./iflat_export
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import time
from pathlib import Path
from typing import Any, Callable, Iterator

import requests

try:
    from iflat_inspection_labels import inspection_type_id as _resolve_inspection_type
    from iflat_inspection_labels import inspection_type_label as _inspection_type_label
except ImportError:
    _resolve_inspection_type = None  # type: ignore[assignment,misc]
    _inspection_type_label = lambda x: (  # type: ignore[assignment,misc]
        str(x) if x is not None else ""
    )

API_BASE = "https://YOUR_CRM_API_HOST/api/v1"

# Рекомендуемые embed (см. iflat_powerbi_sheets_strategy.md)
ROOMS_EMBED_DEFAULT = (
    "room_type,status,floor,section,house,deal,decoration,tags"
)
INSPECTIONS_EMBED_BI = (
    "status,responsible,users,room,room.house,room.room_type,room.deal"
)
HOUSES_EMBED_DEFAULT = "district,sections"


def load_oauth_form() -> dict[str, Any]:
    path = os.environ.get("CRM_SECRETS_JSON", "").strip()
    if path:
        p = Path(path).expanduser()
        raw = json.loads(p.read_text(encoding="utf-8"))
        return {
            "username": raw["username"],
            "password": raw["password"],
            "account_id": int(raw["account_id"]),
            "client_id": int(raw["client_id"]),
            "client_secret": raw["client_secret"],
            "grant_type": raw.get("grant_type", "login"),
        }
    req = (
        "CRM_USERNAME",
        "CRM_PASSWORD",
        "CRM_ACCOUNT_ID",
        "CRM_CLIENT_ID",
        "CRM_CLIENT_SECRET",
    )
    if not all(os.environ.get(k) for k in req):
        raise SystemExit(
            "Задайте CRM_SECRETS_JSON или переменные "
            + ", ".join(req)
        )
    return {
        "username": os.environ["CRM_USERNAME"],
        "password": os.environ["CRM_PASSWORD"],
        "account_id": int(os.environ["CRM_ACCOUNT_ID"]),
        "client_id": int(os.environ["CRM_CLIENT_ID"]),
        "client_secret": os.environ["CRM_CLIENT_SECRET"],
        "grant_type": "login",
    }


def get_token(sess: requests.Session, oauth: dict[str, Any]) -> None:
    r = sess.post(f"{API_BASE}/oauth/token", data=oauth, timeout=60)
    r.raise_for_status()
    tok = r.json()["access_token"]
    sess.headers["Authorization"] = f"Bearer {tok}"


def iter_paginated_get(
    sess: requests.Session,
    path: str,
    base_params: dict[str, Any] | None = None,
    *,
    per_page: int = 100,
    pause_sec: float = 0.05,
) -> Iterator[dict[str, Any]]:
    """Итерирует страницы; каждый элемент — полный JSON ответа (data/meta)."""
    page = 1
    last_page = 1
    base = dict(base_params or {})
    base["perPage"] = per_page
    while page <= last_page:
        base["page"] = page
        r = sess.get(f"{API_BASE}{path}", params=base, timeout=90)
        r.raise_for_status()
        payload = r.json()
        meta = payload.get("meta") or {}
        last_page = int(meta.get("last_page") or 1)
        yield payload
        page += 1
        time.sleep(pause_sec)


def collect_data(sess: requests.Session, path: str, params: dict[str, Any]) -> list[Any]:
    out: list[Any] = []
    for payload in iter_paginated_get(sess, path, params):
        rows = payload.get("data")
        if isinstance(rows, list):
            out.extend(rows)
        elif rows is not None:
            out.append(rows)
    return out


def fetch_reference_tables(sess: requests.Session) -> dict[str, list[Any]]:
    """Короткие GET без пагинации (если API отдаёт всё в data)."""
    refs: dict[str, list[Any]] = {}

    def one(path: str) -> list[Any]:
        r = sess.get(f"{API_BASE}{path}", timeout=60)
        r.raise_for_status()
        js = r.json()
        d = js.get("data")
        return d if isinstance(d, list) else [d] if d is not None else []

    refs["room_types"] = one("/rooms/types")
    refs["room_statuses"] = one("/rooms/statuses")
    refs["inspection_statuses"] = one("/inspections/statuses")
    refs["contract_types"] = one("/deals/contractTypes")
    refs["districts"] = collect_data(sess, "/districts", {})
    refs["houses"] = collect_data(
        sess, "/houses", {"embed": HOUSES_EMBED_DEFAULT}
    )
    return refs


def fetch_rooms_for_statuses(
    sess: requests.Session,
    status_ids: list[int],
    *,
    embed: str = ROOMS_EMBED_DEFAULT,
    order_by: str = "-updated_at",
) -> list[dict[str, Any]]:
    all_rooms: list[dict[str, Any]] = []
    for sid in status_ids:
        chunk = collect_data(
            sess,
            "/rooms",
            {
                "statusId": sid,
                "embed": embed,
                "orderBy": order_by,
            },
        )
        for row in chunk:
            if isinstance(row, dict):
                row["_fetch_status_id"] = sid
                all_rooms.append(row)
        time.sleep(0.05)
    return all_rooms


def fetch_rooms_sold(
    sess: requests.Session,
    *,
    district_id: int | None = None,
    house_id: int | None = None,
    embed: str = "house,room_type,status",
) -> list[dict[str, Any]]:
    p: dict[str, Any] = {"saleStatuses": "SOLD", "embed": embed}
    if district_id is not None:
        p["districtId"] = district_id
    if house_id is not None:
        p["houseId"] = house_id
    return [r for r in collect_data(sess, "/rooms", p) if isinstance(r, dict)]


def fetch_inspections_period(
    sess: requests.Session,
    *,
    type_id: int = 1,
    take_from: str,
    take_to: str,
    status_id: int | None = None,
    house_id: int | None = None,
    embed: str = INSPECTIONS_EMBED_BI,
    order_by: str = "-id",
) -> list[dict[str, Any]]:
    params: dict[str, Any] = {
        "typeId": type_id,
        "takeDateFrom": take_from,
        "takeDateTo": take_to,
        "embed": embed,
        "orderBy": order_by,
    }
    if status_id is not None:
        params["statusId"] = status_id
    if house_id is not None:
        params["houseId"] = house_id
    return [r for r in collect_data(sess, "/inspections", params) if isinstance(r, dict)]


def fetch_inspections_room_chunk(
    sess: requests.Session,
    room_ids: list[int | str],
    *,
    type_id: int = 1,
    embed: str = "status,responsible,users",
) -> list[dict[str, Any]]:
    """Один запрос на список room_id (через запятую в API, как в вашем Rooms_Refresh)."""
    ids = ",".join(str(x) for x in room_ids if x)
    if not ids:
        return []
    return [
        r
        for r in collect_data(
            sess,
            "/inspections",
            {"roomId": ids, "typeId": type_id, "embed": embed},
        )
        if isinstance(r, dict)
    ]


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    cols = columns or sorted({k for r in rows for k in r.keys()})
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


def flatten_room_bi(room: dict[str, Any]) -> dict[str, Any]:
    """Плоские поля для листа «Комнаты» / Power BI (расширяйте при необходимости)."""
    rt = room.get("room_type") if isinstance(room.get("room_type"), dict) else {}
    st = room.get("status") if isinstance(room.get("status"), dict) else {}
    hs = room.get("house") if isinstance(room.get("house"), dict) else {}
    fl = room.get("floor") if isinstance(room.get("floor"), dict) else {}
    sec = room.get("section") if isinstance(room.get("section"), dict) else {}
    deal = room.get("deal") if isinstance(room.get("deal"), dict) else {}
    dec = room.get("decoration") if isinstance(room.get("decoration"), dict) else {}

    return {
        "room_id": room.get("id"),
        "house_id": room.get("house_id"),
        "house_name": hs.get("name"),
        "house_address": hs.get("address") or hs.get("full_address"),
        "district_id": hs.get("district_id"),
        "room_type_id": room.get("room_type_id"),
        "room_type_name": rt.get("name"),
        "status_id": room.get("status_id"),
        "status_name": st.get("name"),
        "status_bg": st.get("bg_color"),
        "status_text_color": st.get("text_color"),
        "floor_id": room.get("floor_id"),
        "floor_name": fl.get("name"),
        "section_id": room.get("section_id"),
        "section_name": sec.get("name"),
        "deal_id": room.get("deal_id") or deal.get("id"),
        "contract_type_id": deal.get("contract_type_id"),
        "decoration_id": room.get("decoration_id"),
        "decoration_name": dec.get("name"),
        "take_date_from": room.get("take_date_from"),
        "take_date_to": room.get("take_date_to"),
        "sale_status": room.get("sale_status"),
        "number": room.get("number"),
        "area": room.get("area"),
        "updated_at": room.get("updated_at"),
    }


def flatten_inspection_bi(row: dict[str, Any]) -> dict[str, Any]:
    room = row.get("room") if isinstance(row.get("room"), dict) else {}
    st = row.get("status") if isinstance(row.get("status"), dict) else {}
    resp = row.get("responsible") if isinstance(row.get("responsible"), dict) else {}
    hs = room.get("house") if isinstance(room.get("house"), dict) else {}
    deal = room.get("deal") if isinstance(room.get("deal"), dict) else {}

    users = row.get("users")
    user_summary = ""
    if isinstance(users, list) and users:
        first = users[0]
        if isinstance(first, dict):
            user_summary = (
                first.get("name")
                or first.get("full_name")
                or first.get("email")
                or ""
            )

    return {
        "inspection_id": row.get("id"),
        "room_id": row.get("room_id") or room.get("id"),
        "type_id": row.get("type_id"),
        "type_name": _inspection_type_label(row.get("type_id")),
        "status_id": row.get("status_id"),
        "status_name": st.get("name"),
        "status_bg": st.get("bg_color"),
        "take_date_start": row.get("take_date_start"),
        "take_date_end": row.get("take_date_end"),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
        "responsible_id": row.get("responsible_id"),
        "responsible_name": resp.get("name") or resp.get("full_name"),
        "users_preview": user_summary,
        "house_id": room.get("house_id"),
        "house_name": hs.get("name"),
        "deal_id": room.get("deal_id") or deal.get("id"),
        "contract_type_id": deal.get("contract_type_id"),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="CRM read-only export helpers")
    ap.add_argument("--out-dir", type=Path, default=Path("./iflat_export"))
    ap.add_argument("--refs", action="store_true", help="Справочники + дома + ЖК")
    ap.add_argument("--rooms", action="store_true")
    ap.add_argument(
        "--status-ids",
        default="6,11,12",
        help="Статусы помещений для /rooms (через запятую)",
    )
    ap.add_argument("--inspections", action="store_true")
    ap.add_argument(
        "--type-id",
        type=int,
        default=None,
        help="Числовой typeId (1=клиентская, 2=внутренняя, 3=УК). Игнорируется, если задан --inspection-type",
    )
    ap.add_argument(
        "--inspection-type",
        default="client",
        metavar="NAME",
        help='Тип приёмки словом: client | internal | management_company или «клиентская» / «внутренняя» / «ук»',
    )
    ap.add_argument("--take-from", default="", help="ДД.ММ.ГГГГ")
    ap.add_argument("--take-to", default="", help="ДД.ММ.ГГГГ")
    ap.add_argument("--sold-snapshot", action="store_true", help="/rooms SOLD")
    ap.add_argument("--district-id", type=int, default=None)
    args = ap.parse_args()

    oauth = load_oauth_form()
    sess = requests.Session()
    sess.headers.update(
        {"User-Agent": "iflat-bi-readonly/1.0", "Accept": "application/json"}
    )
    get_token(sess, oauth)
    out = args.out_dir

    if args.refs or not any(
        [args.rooms, args.inspections, args.sold_snapshot]
    ):
        refs = fetch_reference_tables(sess)
        write_json(out / "refs.json", refs)
        write_csv(out / "ref_room_types.csv", [dict(r) if isinstance(r, dict) else {"value": r} for r in refs.get("room_types", [])])
        write_csv(out / "ref_room_statuses.csv", [dict(r) if isinstance(r, dict) else {"value": r} for r in refs.get("room_statuses", [])])
        write_csv(out / "ref_inspection_statuses.csv", [dict(r) if isinstance(r, dict) else {"value": r} for r in refs.get("inspection_statuses", [])])
        write_csv(out / "ref_contract_types.csv", [dict(r) if isinstance(r, dict) else {"value": r} for r in refs.get("contract_types", [])])
        write_csv(out / "dim_districts.csv", refs.get("districts", []))
        write_csv(out / "dim_houses.csv", refs.get("houses", []))
        print("OK refs ->", out)

    if args.rooms:
        sids = [int(x) for x in args.status_ids.split(",") if x.strip()]
        rooms = fetch_rooms_for_statuses(sess, sids)
        write_json(out / "rooms_raw.json", rooms)
        flat = [flatten_room_bi(r) for r in rooms]
        write_csv(out / "rooms_flat.csv", flat)
        print(f"OK rooms count={len(rooms)} ->", out)

    if args.inspections:
        if not args.take_from or not args.take_to:
            raise SystemExit("--inspections требует --take-from и --take-to (ДД.ММ.ГГГГ)")
        insp = fetch_inspections_period(
            sess,
            type_id=args.type_id,
            take_from=args.take_from,
            take_to=args.take_to,
        )
        write_json(out / "inspections_raw.json", insp)
        write_csv(out / "inspections_flat.csv", [flatten_inspection_bi(r) for r in insp])
        print(f"OK inspections count={len(insp)} ->", out)

    if args.sold_snapshot:
        sold = fetch_rooms_sold(sess, district_id=args.district_id)
        write_json(out / "rooms_sold_raw.json", sold)
        write_csv(out / "rooms_sold_flat.csv", [flatten_room_bi(r) for r in sold])
        print(f"OK sold rooms count={len(sold)} ->", out)


if __name__ == "__main__":
    main()
