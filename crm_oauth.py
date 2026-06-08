"""Загрузка OAuth CRM из env или файла в личная-информация (не коммитить)."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

_PRIVATE_DEFAULT = (
    Path(__file__).resolve().parent.parent
    / "личная-информация"
    / "credentials"
    / "iflat_secrets.json"
)


def load_iflat_oauth() -> dict[str, Any]:
    path = os.environ.get("CRM_SECRETS_JSON", "").strip()
    if not path:
        path = str(_PRIVATE_DEFAULT)
    p = Path(path).expanduser()
    if not p.is_file():
        raise FileNotFoundError(
            f"Файл секретов CRM не найден: {p}. "
            "Скопируйте iflat_secrets.json.example в личная-информация/credentials/ "
            "или задайте CRM_SECRETS_JSON."
        )
    raw = json.loads(p.read_text(encoding="utf-8"))
    return {
        "username": raw["username"],
        "password": raw["password"],
        "account_id": int(raw["account_id"]),
        "client_id": int(raw["client_id"]),
        "client_secret": raw["client_secret"],
        "grant_type": raw.get("grant_type", "login"),
    }


def google_service_account_path() -> Path:
    env = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if env:
        return Path(env).expanduser()
    p = (
        Path(__file__).resolve().parent.parent
        / "личная-информация"
        / "credentials"
        / "service-account.json"
    )
    if not p.is_file():
        raise FileNotFoundError(
            f"Service account не найден: {p}. "
            "Положите JSON в личная-информация/credentials/ "
            "или задайте GOOGLE_SERVICE_ACCOUNT_JSON."
        )
    return p
