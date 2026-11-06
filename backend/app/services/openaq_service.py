import os
import json
import csv
from pathlib import Path
from datetime import datetime, timezone

import requests
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
except ImportError:
    pass

OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY")

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_URL = os.getenv("OPENAQ_BASE_URL", "https://api.openaq.org/v3")

BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_DIR.parent

CACHE_DIR = BACKEND_DIR / "data" / "api_cache" / "air_quality"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# OPENAQ STATION MAPPING
# --------------------------------------------------

# Fallback default stations
DEFAULT_STATIONS = {
    "Nagpur": 5621,
    "Chhatrapati Sambhajinagar": 5642,
    "Nashik": 5592,
    "Mumbai": 6945,
    "Pune": 11609,
}

CITY_STATIONS = dict(DEFAULT_STATIONS)

# Attempt to load verified mapping from CSV if available
MAPPING_CSV_PATH = PROJECT_ROOT / "data" / "processed" / "air_quality" / "openaq_city_station_mapping.csv"
if MAPPING_CSV_PATH.exists():
    try:
        with open(MAPPING_CSV_PATH, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                city = row.get("city", "").strip()
                st_id = row.get("station_id", "").strip()
                status = row.get("status", "").strip()
                if city and st_id and status != "NO_MATCH":
                    try:
                        CITY_STATIONS[city] = int(float(st_id))
                    except ValueError:
                        pass
    except Exception as err:
        print(f"[OpenAQ] Warning: failed to load mapping CSV: {err}")


# --------------------------------------------------
# CACHE FUNCTIONS
# --------------------------------------------------

def get_cache_path(city_name):
    """Return cache file path for a city."""
    safe_name = city_name.lower().replace(" ", "_")
    return CACHE_DIR / f"{safe_name}.json"


def save_cache(city_name, data):
    """Save latest successful API result."""
    cache_path = get_cache_path(city_name)
    with open(cache_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    return cache_path


def load_cache(city_name):
    """Load previously saved API result."""
    cache_path = get_cache_path(city_name)
    if not cache_path.exists():
        return None
    try:
        with open(cache_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return None


# --------------------------------------------------
# FETCH LIVE AIR QUALITY FROM OPENAQ
# --------------------------------------------------

def fetch_live_air_quality(city_name):
    """
    Fetch the newest PM2.5 and PM10 measurements
    from the configured OpenAQ station.
    """
    api_key = os.getenv("OPENAQ_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAQ_API_KEY is not configured")

    # Match city (case-insensitive)
    station_id = None
    for c, sid in CITY_STATIONS.items():
        if c.casefold() == city_name.strip().casefold():
            station_id = sid
            break

    if not station_id:
        raise ValueError(f"No OpenAQ station configured for {city_name}")

    headers = {
        "X-API-Key": api_key
    }

    url = f"{BASE_URL}/locations/{station_id}/sensors"

    response = requests.get(url, headers=headers, timeout=12)
    response.raise_for_status()

    result = response.json()
    sensors = result.get("results", [])

    pm25_candidates = []
    pm10_candidates = []

    for sensor in sensors:
        parameter = sensor.get("parameter", {})
        parameter_name = str(parameter.get("name", "")).lower()
        latest = sensor.get("latest")
        if not latest:
            continue

        value = latest.get("value")
        timestamp = latest.get("datetime")
        if value is None or timestamp is None:
            continue

        local_time = timestamp.get("local") if isinstance(timestamp, dict) else str(timestamp)
        if not local_time:
            continue

        if parameter_name in ["pm25", "pm2.5"]:
            pm25_candidates.append({
                "value": value,
                "time": local_time
            })
        elif parameter_name == "pm10":
            pm10_candidates.append({
                "value": value,
                "time": local_time
            })

    pm25 = None
    pm25_time = None
    if pm25_candidates:
        newest_pm25 = max(pm25_candidates, key=lambda x: str(x["time"]))
        pm25 = newest_pm25["value"]
        pm25_time = newest_pm25["time"]

    pm10 = None
    pm10_time = None
    if pm10_candidates:
        newest_pm10 = max(pm10_candidates, key=lambda x: str(x["time"]))
        pm10 = newest_pm10["value"]
        pm10_time = newest_pm10["time"]

    if pm25 is None and pm10 is None:
        raise RuntimeError(f"No PM2.5 or PM10 data available for {city_name}")

    aqi_val = calculate_cpcb_aqi(pm25, pm10)

    data = {
        "city": city_name,
        "station_id": station_id,
        "aqi": aqi_val,
        "pm25": pm25,
        "pm25_measurement_time": pm25_time,
        "pm10": pm10,
        "pm10_measurement_time": pm10_time,
        "unit": "µg/m³",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": "OpenAQ API v3",
        "status": "LIVE",
        "year": "2026"
    }

    return data


# --------------------------------------------------
# CPCB AQI SUB-INDEX CALCULATION (OFFICIAL INDIAN STANDARD)
# --------------------------------------------------

def calculate_cpcb_aqi(pm25=None, pm10=None):
    """
    Calculate official Indian CPCB Air Quality Index from PM2.5 and PM10 concentrations.
    Uses official breakpoint linear interpolation formulas.
    """
    sub_indices = []
    if pm25 is not None and pm25 >= 0:
        if pm25 <= 30:
            sub_indices.append((50 / 30) * pm25)
        elif pm25 <= 60:
            sub_indices.append(50 + ((100 - 50) / (60 - 30)) * (pm25 - 30))
        elif pm25 <= 90:
            sub_indices.append(100 + ((200 - 100) / (90 - 60)) * (pm25 - 60))
        elif pm25 <= 120:
            sub_indices.append(200 + ((300 - 200) / (120 - 90)) * (pm25 - 90))
        elif pm25 <= 250:
            sub_indices.append(300 + ((400 - 300) / (250 - 120)) * (pm25 - 120))
        else:
            sub_indices.append(min(500, 400 + ((500 - 400) / (380 - 250)) * (pm25 - 250)))

    if pm10 is not None and pm10 >= 0:
        if pm10 <= 50:
            sub_indices.append(pm10)
        elif pm10 <= 100:
            sub_indices.append(50 + (pm10 - 50))
        elif pm10 <= 250:
            sub_indices.append(100 + ((200 - 100) / (250 - 100)) * (pm10 - 100))
        elif pm10 <= 350:
            sub_indices.append(200 + ((300 - 200) / (350 - 250)) * (pm10 - 250))
        elif pm10 <= 430:
            sub_indices.append(300 + ((400 - 300) / (430 - 350)) * (pm10 - 350))
        else:
            sub_indices.append(min(500, 400 + ((500 - 400) / (500 - 430)) * (pm10 - 430)))

    if not sub_indices:
        return None
    return round(max(sub_indices), 1)


# --------------------------------------------------
# MAIN FUNCTION WITH CACHE FALLBACK
# --------------------------------------------------

def get_air_quality(city_name):
    """
    Get air-quality data using:
    1. OpenAQ live API
    2. Local cached API data
    3. None if neither is available
    """
    try:
        data = fetch_live_air_quality(city_name)
        save_cache(city_name, data)
        return data
    except Exception as error:
        print(f"[OpenAQ] Live API fetch failed for {city_name}: {error}")

    cached_data = load_cache(city_name)
    if cached_data:
        cached_data["status"] = "CACHED"
        return cached_data

    return None
