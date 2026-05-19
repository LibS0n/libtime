import gzip
import json
from datetime import datetime
from functools import lru_cache
from importlib.resources import files
from typing import Optional, Dict, Any
import zoneinfo

from . import _tz_cache

_DB = None
_DB_MODE = None

def _get_db_path(mode: str):
    from pathlib import Path
    return files("libtime.databases") / f"cities_{mode}.json.gz"

def _load_database(mode: str = None) -> Dict[str, Any]:
    global _DB, _DB_MODE
    if _DB is not None and (mode is None or mode == _DB_MODE):
        return _DB

    if mode is None:
        for candidate in ["full", "city", "lite"]:
            if _get_db_path(candidate).exists():
                mode = candidate
                break
        else:
            raise FileNotFoundError("No city database found. Reinstall libtime.")
    else:
        if not _get_db_path(mode).exists():
            raise FileNotFoundError(f"Database '{mode}' not found in package.")

    path = _get_db_path(mode)
    with gzip.open(path, "rt", encoding="utf-8") as f:
        _DB = json.load(f)
    _DB_MODE = mode
    return _DB

@lru_cache(maxsize=4096)
def get_city_data(city_name: str, db_mode: str = None) -> Optional[Dict[str, Any]]:
    db = _load_database(db_mode)
    key = city_name.strip().lower()
    return db.get(key)

def resolve_city(city_name: str) -> Optional[Dict[str, Any]]:
    return get_city_data(city_name)

def timezone_for_city(city_name: str) -> Optional[str]:
    data = resolve_city(city_name)
    return data["tz"] if data else None

def country_for_city(city_name: str) -> Optional[str]:
    data = resolve_city(city_name)
    return data["country"] if data else None

def preload_database(mode: str = "city"):
    _load_database(mode)

def local_datetime(city_name: str) -> Optional[datetime]:
    tz_str = timezone_for_city(city_name)
    if not tz_str:
        return None
    tz = zoneinfo.ZoneInfo(tz_str)
    return datetime.now(tz)

def local_time(
    city_name: str,
    format: str = "24h",
    ampm_uppercase: bool = True
) -> Optional[str]:
    dt = local_datetime(city_name)
    if dt is None:
        return None

    if format == "24h" or format == "24h_sec":
        return dt.strftime("%H:%M:%S")
    elif format == "24h_no_sec":
        return dt.strftime("%H:%M")
    elif format == "12h":
        return dt.strftime("%I:%M:%S %p") if ampm_uppercase else dt.strftime("%I:%M:%S %p").lower()
    elif format == "12h_lower":
        return dt.strftime("%I:%M:%S %p").lower()
    elif format == "12h_no_sec":
        return dt.strftime("%I:%M %p")
    else:
        return dt.strftime(format)