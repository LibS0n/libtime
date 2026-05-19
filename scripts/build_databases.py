import gzip
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent
DB_DIR = PROJECT_ROOT / "libtime" / "databases"
DB_DIR.mkdir(parents=True, exist_ok=True)

def find_cities_json():
    candidates = [
        Path.cwd() / "cities.json",
        SCRIPT_DIR / "cities.json",
        PROJECT_ROOT / "cities.json",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None

def extract_core(city):
    return {
        "tz": city["timezone"],
        "lat": city["latitude"],
        "lng": city["longitude"],
        "country": city["country_code"],
    }

def extract_full(city):
    return {
        "tz": city["timezone"],
        "lat": city["latitude"],
        "lng": city["longitude"],
        "country": city["country_code"],
        "state": city.get("state_name", ""),
        "capital": city.get("capital", ""),
    }

def build_lite(cities_data):
    capitals = {c["name"].lower() for c in cities_data if c.get("capital") in ["primary", "admin"]}
    result = {}
    count = 0
    for city in cities_data:
        name = city["name"].lower()
        if name in result:
            continue
        if count < 2000 or name in capitals:
            result[name] = extract_core(city)
            count += 1
    return result

def build_city(cities_data):
    result = {}
    for city in cities_data:
        name = city["name"].lower()
        if name not in result:
            result[name] = extract_core(city)
    return result

def build_full_multilingual(cities_data):
    result = {}
    for city in cities_data:
        name = city["name"].strip()
        base_data = extract_full(city)

        key = name.lower()
        if key not in result:
            result[key] = base_data

        translations = city.get("translations")
        if translations and isinstance(translations, dict):
            for lang, translated_name in translations.items():
                if not translated_name or not isinstance(translated_name, str):
                    continue
                tkey = translated_name.strip().lower()
                if tkey and tkey not in result:
                    result[tkey] = base_data

        native = city.get("native", "")
        if native and isinstance(native, str):
            nkey = native.strip().lower()
            if nkey and nkey not in result:
                result[nkey] = base_data
    return result

def save_gz(data, filename):
    path = DB_DIR / filename
    with gzip.open(path, "wt", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"))
    size = path.stat().st_size / (1024 * 1024)
    print(f"Saved {filename} – {size:.2f} MB")

def main():
    cities_path = find_cities_json()
    if not cities_path:
        print("ERROR: cities.json not found. Place it in the current directory or scripts/.")
        return

    print(f"Using local file: {cities_path}")
    with open(cities_path, "r", encoding="utf-8") as f:
        all_cities = json.load(f)
    print(f"Loaded {len(all_cities)} cities.")

    lite = build_lite(all_cities)
    print(f"Lite: {len(lite)} entries (primary names only)")

    city_db = build_city(all_cities)
    print(f"City: {len(city_db)} entries (primary names only)")

    full_db = build_full_multilingual(all_cities)
    print(f"Full: {len(full_db)} entries (multilingual + state + capital)")

    save_gz(lite, "cities_lite.json.gz")
    save_gz(city_db, "cities_city.json.gz")
    save_gz(full_db, "cities_full.json.gz")

    print("\nDatabases created successfully.")
    print("  - lite: small, only major cities")
    print("  - city: all cities, primary names only (~2 MB)")
    print("  - full: all cities + translations + extra fields (~16 MB)")
    print("Commit the .gz files to your repository.")

if __name__ == "__main__":
    main()
