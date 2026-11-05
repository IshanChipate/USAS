import os
import time
import pandas as pd
import requests

from pathlib import Path
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent

load_dotenv(BACKEND_DIR / ".env")

OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY")

if not OPENAQ_API_KEY:
    raise RuntimeError(
        "OPENAQ_API_KEY is not set in backend/.env"
    )


BASE_URL = "https://api.openaq.org/v3"

HEADERS = {
    "X-API-Key": OPENAQ_API_KEY
}


# Maharashtra approximate bounding box
# xmin = longitude
# ymin = latitude
# xmax = longitude
# ymax = latitude

MAHARASHTRA_BBOX = (
    "72.6,15.6,80.9,22.1"
)


# Master dataset
MASTER_DATASET = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "master"
    / "USAS_city_indicator_master_clean.csv"
)


# Output mapping
OUTPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "air_quality"
    / "openaq_city_station_mapping.csv"
)


# ============================================================
# READ 42 CITIES
# ============================================================

def load_cities():

    if not MASTER_DATASET.exists():

        raise FileNotFoundError(
            f"Master dataset not found:\n{MASTER_DATASET}"
        )

    df = pd.read_csv(MASTER_DATASET)

    if "city_name" not in df.columns:

        raise ValueError(
            "city_name column not found in master dataset"
        )

    cities = sorted(
        df["city_name"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

    print(f"\nCities found in master dataset: {len(cities)}")

    return cities


# ============================================================
# GET OPENAQ LOCATIONS
# ============================================================

def get_openaq_locations():

    print("\nSearching OpenAQ for Maharashtra stations...")
    print("Please wait...\n")

    url = f"{BASE_URL}/locations"

    params = {
        "bbox": MAHARASHTRA_BBOX,
        "iso": "IN",
        "limit": 1000,
        "page": 1
    }

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    locations = data.get("results", [])

    print(
        f"OpenAQ returned {len(locations)} locations."
    )

    return locations


# ============================================================
# CHECK PM2.5 / PM10
# ============================================================

def get_pollutant_info(location):

    has_pm25 = False
    has_pm10 = False

    for sensor in location.get("sensors", []):

        parameter = sensor.get("parameter", {})

        name = str(
            parameter.get("name", "")
        ).lower()

        if name in ["pm25", "pm2.5"]:
            has_pm25 = True

        if name == "pm10":
            has_pm10 = True

    return has_pm25, has_pm10


# ============================================================
# NORMALIZE CITY NAME
# ============================================================

def normalize_name(name):

    name = str(name).lower().strip()

    replacements = {
        "chhatrapati sambhajinagar": "aurangabad",
        "sambhajinagar": "aurangabad",
        "mumbai suburban": "mumbai",
        "thane city": "thane",
        "pimpri chinchwad": "pimpri-chinchwad"
    }

    return replacements.get(name, name)


# ============================================================
# MATCH CITY WITH OPENAQ LOCATION
# ============================================================

def find_city_matches(city, locations):

    city_normalized = normalize_name(city)

    matches = []

    for location in locations:

        location_name = (
            location.get("name") or ""
        )

        locality = (
            location.get("locality") or ""
        )

        location_text = (
            f"{location_name} {locality}"
        ).lower()

        normalized_text = normalize_name(
            location_text
        )

        # ----------------------------------------------------
        # Direct city-name match
        # ----------------------------------------------------

        if city_normalized in normalized_text:

            has_pm25, has_pm10 = (
                get_pollutant_info(location)
            )

            matches.append({
                "city": city,
                "station_id": location.get("id"),
                "station_name": location_name,
                "locality": locality,
                "provider": (
                    location.get("provider", {})
                    .get("name")
                ),
                "owner": (
                    location.get("owner", {})
                    .get("name")
                ),
                "latitude": (
                    location.get("coordinates", {})
                    .get("latitude")
                ),
                "longitude": (
                    location.get("coordinates", {})
                    .get("longitude")
                ),
                "pm25_available": has_pm25,
                "pm10_available": has_pm10,
                "datetime_last": (
                    location.get("datetimeLast", {})
                    .get("local")
                    if location.get("datetimeLast")
                    else None
                )
            })

    return matches


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 70)
    print("USAS - OpenAQ 42 CITY DISCOVERY")
    print("=" * 70)

    cities = load_cities()

    if len(cities) != 42:

        print(
            f"\nWARNING: Expected 42 cities, "
            f"but found {len(cities)}."
        )

    locations = get_openaq_locations()

    results = []

    print("\n")
    print("=" * 70)
    print("CITY MATCHING")
    print("=" * 70)

    for index, city in enumerate(cities, start=1):

        matches = find_city_matches(
            city,
            locations
        )

        # ----------------------------------------------------
        # No station found
        # ----------------------------------------------------

        if not matches:

            results.append({
                "city": city,
                "station_id": None,
                "station_name": None,
                "locality": None,
                "provider": None,
                "owner": None,
                "latitude": None,
                "longitude": None,
                "pm25_available": False,
                "pm10_available": False,
                "datetime_last": None,
                "status": "NO_MATCH"
            })

            print(
                f"[{index:02d}/42] "
                f"{city:<30} "
                f"NO MATCH"
            )

            continue


        # ----------------------------------------------------
        # Select best match
        #
        # Prefer stations having BOTH PM2.5 and PM10.
        # ----------------------------------------------------

        matches.sort(
            key=lambda x: (
                x["pm25_available"]
                and x["pm10_available"],
                x["datetime_last"] or ""
            ),
            reverse=True
        )

        best = matches[0]

        best["status"] = (
            "MATCHED_PM25_PM10"
            if (
                best["pm25_available"]
                and best["pm10_available"]
            )
            else "MATCHED_PARTIAL"
        )

        results.append(best)

        print(
            f"[{index:02d}/42] "
            f"{city:<30} "
            f"Station: {best['station_id']} | "
            f"PM2.5: {best['pm25_available']} | "
            f"PM10: {best['pm10_available']} | "
            f"Latest: {best['datetime_last']}"
        )


    # ========================================================
    # SAVE RESULT
    # ========================================================

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    result_df = pd.DataFrame(results)

    result_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n")
    print("=" * 70)
    print("DISCOVERY COMPLETE")
    print("=" * 70)

    print(
        f"\nMapping saved to:\n{OUTPUT_FILE}"
    )

    print(
        f"\nTotal cities: {len(result_df)}"
    )

    print(
        "Cities with OpenAQ match:",
        (
            result_df["station_id"]
            .notna()
            .sum()
        )
    )

    print(
        "Cities with PM2.5 + PM10:",
        (
            (
                result_df["pm25_available"]
                & result_df["pm10_available"]
            ).sum()
        )
    )

    print(
        "Cities with no match:",
        (
            result_df["station_id"]
            .isna()
            .sum()
        )
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()