from datetime import datetime
from typing import Optional

_HIJRI_AVAILABLE = False
_JALALI_AVAILABLE = False
_HEBREW_AVAILABLE = False

try:
    from hijri_converter import Gregorian
    _HIJRI_AVAILABLE = True
except ImportError:
    pass

try:
    import jdatetime
    _JALALI_AVAILABLE = True
except ImportError:
    pass

try:
    from convertdate import hebrew
    _HEBREW_AVAILABLE = True
except ImportError:
    pass

def to_hijri(dt: datetime) -> Optional[dict]:
    if not _HIJRI_AVAILABLE:
        raise ImportError("hijri-converter not installed. Run: pip install hijri-converter")
    
    hijri_date = Gregorian(dt.year, dt.month, dt.day).to_hijri()
    
    month_names = [
        "Muharram", "Safar", "Rabi' al-awwal", "Rabi' al-thani",
        "Jumada al-awwal", "Jumada al-thani", "Rajab", "Sha'ban",
        "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"
    ]
    return {
        "year": hijri_date.year,
        "month": hijri_date.month,
        "month_name": month_names[hijri_date.month - 1],
        "day": hijri_date.day,
        "calendar": "Hijri"
    }

def to_jalali(dt: datetime) -> Optional[dict]:
    if not _JALALI_AVAILABLE:
        raise ImportError("jdatetime not installed. Run: pip install jdatetime")
    jd = jdatetime.datetime.fromgregorian(datetime=dt)
    month_names = [
        "Farvardin", "Ordibehesht", "Khordad", "Tir", "Mordad", "Shahrivar",
        "Mehr", "Aban", "Azar", "Dey", "Bahman", "Esfand"
    ]
    return {
        "year": jd.year,
        "month": jd.month,
        "month_name": month_names[jd.month - 1],
        "day": jd.day,
        "calendar": "Jalali (Persian)"
    }

def to_hebrew(dt: datetime) -> Optional[dict]:
    if not _HEBREW_AVAILABLE:
        raise ImportError("convertdate not installed. Run: pip install convertdate")
    
    y, m, d = hebrew.from_gregorian(dt.year, dt.month, dt.day)
    
    hebrew_months = [
        "Nisan", "Iyar", "Sivan", "Tammuz", "Av", "Elul",
        "Tishrei", "Cheshvan", "Kislev", "Tevet", "Shevat", "Adar"
    ]
    month_name = hebrew_months[m - 1]
    return {
        "year": y,
        "month": m,
        "month_name": month_name,
        "day": d,
        "calendar": "Hebrew"
    }
