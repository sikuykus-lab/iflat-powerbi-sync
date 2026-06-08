"""
Цвет для BI-выгрузок (лист iflat, лист Приёмка).

Режимы (env ``CRM_COLOR_MODE``):
- ``f17`` — ``classify_color_group_template_b`` (template_b: I38 зелёные, синие st=11, I51 красные)
- ``f11`` — ``classify_color_mrk`` (template_a: те же статусы + красный УПС/снято)
- ``v1``  — legacy: префикс приёмок + эвристика по последней приёмке (сохранён)

На листе **Приёмка** цвет считается по **префиксу** истории ОН до строки включительно
(как в отчётах, но построчно, без суммирования).
"""

from __future__ import annotations

import os
from collections import defaultdict

from iflat_room_metrics import (
    _dedupe_inspections,
    _room_from_inspection,
    _sort_inspections_by_start,
    classify_color_group_at_inspection,
    classify_color_group_template_b,
    classify_color_mrk,
    color_group_display_bi,
)

COLOR_MODE_F17 = "f17"
COLOR_MODE_F11 = "f11"
COLOR_MODE_V1 = "v1"
COLOR_MODES = frozenset({COLOR_MODE_F17, COLOR_MODE_F11, COLOR_MODE_V1})
DEFAULT_COLOR_MODE = COLOR_MODE_F17

INSP_EMBED_CLAIMS_SUFFIX = ",claims.status,claims.owner"


def resolve_color_mode(mode: str | None = None) -> str:
    raw = (mode or os.environ.get("CRM_COLOR_MODE") or DEFAULT_COLOR_MODE).strip().lower()
    if raw not in COLOR_MODES:
        return DEFAULT_COLOR_MODE
    return raw


def _collapse_f11_group(raw: str) -> str:
    """Три корзины template_b-стиля из детального MRK (template_a)."""
    s = (raw or "").strip()
    if s.startswith("КРАСНЫЙ"):
        return "КРАСНЫЙ"
    return s


def classify_color_raw(
    room: dict,
    insps: list,
    *,
    mode: str | None = None,
    client_insp_ids: frozenset[int] | None = None,
) -> str:
    """Сырой код группы: ЗЕЛЁНЫЙ / СИНИЙ / КРАСНЫЙ / …"""
    m = resolve_color_mode(mode)
    if m == COLOR_MODE_V1:
        return classify_color_group_at_inspection(room, insps)
    if m == COLOR_MODE_F11:
        return _collapse_f11_group(classify_color_mrk(room, insps, client_insp_ids))
    return classify_color_group_template_b(room, insps)


def classify_color_mrk_raw(
    room: dict,
    insps: list,
    client_insp_ids: frozenset[int] | None = None,
) -> str:
    """Детальный MRK (template_a): КРАСНЫЙ_УПС, КРАСНЫЙ_УСТРАНЕНО, …"""
    return classify_color_mrk(room, insps, client_insp_ids)


def color_mrk_display_bi(raw: str) -> str:
    return {
        "ЗЕЛЁНЫЙ": "Зелёный",
        "СИНИЙ": "Синий",
        "КРАСНЫЙ": "Красный",
        "КРАСНЫЙ_УСТРАНЕНО": "Красный (снято)",
        "КРАСНЫЙ_УПС": "Красный (УПС)",
    }.get((raw or "").strip(), "")


def color_group_for_room(
    room: dict,
    insps: list,
    *,
    mode: str | None = None,
    client_insp_ids: frozenset[int] | None = None,
) -> str:
    """Подпись «Цветовая группа» на листе iflat (вся история приёмок ОН)."""
    return color_group_display_bi(
        classify_color_raw(room, insps, mode=mode, client_insp_ids=client_insp_ids)
    )


def color_mrk_for_room(
    room: dict,
    insps: list,
    client_insp_ids: frozenset[int] | None = None,
) -> str:
    """Подпись «Цвет МРК» — всегда template_a."""
    return color_mrk_display_bi(classify_color_mrk_raw(room, insps, client_insp_ids))


def color_group_by_inspection_id(
    inspections: list[dict],
    *,
    mode: str | None = None,
    client_insp_ids: frozenset[int] | None = None,
) -> dict[int, str]:
    """Цвет на каждую приёмку: префикс истории по помещению."""
    m = resolve_color_mode(mode)
    by_room: dict[int, list[dict]] = defaultdict(list)
    for insp in _dedupe_inspections(inspections):
        try:
            rid = int(insp.get("room_id") or _room_from_inspection(insp).get("id"))
        except (TypeError, ValueError):
            continue
        by_room[rid].append(insp)

    if client_insp_ids is None and m == COLOR_MODE_F11:
        ids: set[int] = set()
        for insp in _dedupe_inspections(inspections):
            try:
                if int(insp.get("type_id") or 0) == 1:
                    ids.add(int(insp["id"]))
            except (TypeError, ValueError, KeyError):
                continue
        client_insp_ids = frozenset(ids)

    out: dict[int, str] = {}
    for insps in by_room.values():
        prefix: list[dict] = []
        for insp in _sort_inspections_by_start(insps):
            prefix.append(insp)
            try:
                iid = int(insp["id"])
            except (TypeError, ValueError, KeyError):
                continue
            raw = classify_color_raw(
                _room_from_inspection(insp),
                prefix,
                mode=m,
                client_insp_ids=client_insp_ids,
            )
            out[iid] = color_group_display_bi(raw)
    return out


def inspection_embed_for_mode(base_embed: str, mode: str | None = None) -> str:
    """Для f11 в embed нужны claims на приёмках."""
    if resolve_color_mode(mode) == COLOR_MODE_F11 and INSP_EMBED_CLAIMS_SUFFIX not in base_embed:
        return base_embed + INSP_EMBED_CLAIMS_SUFFIX
    return base_embed
