"""Optional live OpenAQ smoke check; requires OPENAQ_API_KEY in backend/.env."""

from backend.app.services.openaq_service import CITY_STATIONS, get_air_quality


if __name__ == "__main__":
    for city in CITY_STATIONS:
        data = get_air_quality(city)
        print(f"{city}: {data or 'No live or cached data'}")
