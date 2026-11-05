from pathlib import Path
import pandas as pd

from .data_loader import load_city_data, normalize_city_name

PROJECT_DATA_ROOT = Path(__file__).resolve().parents[3] / "data" / "processed"


# Columns that should contain numeric values
NUMERIC_COLUMNS = [
    "avg_aqi",
    "aqi_poor_or_worse_pct",
    "aqi_completeness_pct",
    "waste_generated_mt_day",
    "waste_treated_mt_day",
    "waste_treatment_efficiency_pct",
    "waste_segregation_pct",
    "waste_transport_pct",
    "population_2011",
    "population_density_2011_persons_per_km2",
    "green_area_pct",
    "green_area_km2",
    "traffic_value",
    "traffic_congestion_value",
    "traffic_congestion_year",
]


def process_city_data():
    """
    Load and clean the complete USAS city dataset.
    """

    df = load_city_data().copy()

    # Standardize city names
    df["city_name"] = (
        df["city_name"]
        .astype(str)
        .str.strip()
    )

    # The master export contains green area (km²), while the agreed scoring
    # configuration uses the comparable percentage from the processed source.
    green_path = PROJECT_DATA_ROOT / "green_space" / "USAS_green_space_processed.csv"
    if green_path.exists():
        green = pd.read_csv(green_path)
        if {"city_name", "green_area_pct"}.issubset(green.columns):
            green["_city_key"] = green["city_name"].map(normalize_city_name)
            if "reference_year" in green.columns:
                green["_year"] = pd.to_numeric(green["reference_year"], errors="coerce")
            else:
                green["_year"] = pd.NA
            green = green.sort_values("_year")
            green_by_city = {key: group for key, group in green.groupby("_city_key", dropna=True)}
            def matching_green_pct(row):
                candidates = green_by_city.get(normalize_city_name(row["city_name"]))
                if candidates is None:
                    return None
                target_year = pd.to_numeric(pd.Series([row.get("green_year")]), errors="coerce").iloc[0]
                if pd.notna(target_year):
                    exact = candidates[candidates["_year"] == target_year]
                    if not exact.empty:
                        return exact.iloc[-1]["green_area_pct"]
                return candidates.iloc[-1]["green_area_pct"]

            source_green_pct = df.apply(matching_green_pct, axis=1)
            if "green_area_pct" in df.columns:
                existing_green_pct = pd.to_numeric(df["green_area_pct"], errors="coerce")
                df["green_area_pct"] = existing_green_pct.where(existing_green_pct.notna(), source_green_pct)
            else:
                df["green_area_pct"] = source_green_pct

    # Keep the master traffic-pressure proxy for display, but score only the
    # separately processed records explicitly marked as measured and eligible.
    traffic_path = PROJECT_DATA_ROOT / "traffic" / "USAS_traffic_processed.csv"
    if traffic_path.exists():
        traffic = pd.read_csv(traffic_path)
        required = {"city_name", "traffic_value", "traffic_metric", "score_eligible"}
        if required.issubset(traffic.columns):
            eligible = traffic[traffic["score_eligible"].map(lambda value: str(value).casefold() in {"true", "1"})].copy()
            eligible["_city_key"] = eligible["city_name"].map(normalize_city_name)
            eligible["_year"] = pd.to_numeric(eligible.get("reference_year"), errors="coerce")
            eligible = eligible.sort_values("_year").drop_duplicates("_city_key", keep="last")
            eligible_by_city = eligible.set_index("_city_key")

            def measured_traffic_value(city_name, source_column):
                key = normalize_city_name(city_name)
                return eligible_by_city.loc[key, source_column] if key in eligible_by_city.index and source_column in eligible_by_city.columns else None

            traffic_fields = {
                "traffic_value": "traffic_congestion_value",
                "traffic_metric": "traffic_congestion_metric",
                "traffic_unit": "traffic_congestion_unit",
                "reference_year": "traffic_congestion_year",
                "data_status": "traffic_congestion_status",
                "source": "traffic_congestion_source",
                "source_url": "traffic_congestion_source_url",
            }
            for source_column, target_column in traffic_fields.items():
                if source_column in eligible.columns:
                    df[target_column] = df["city_name"].map(lambda name: measured_traffic_value(name, source_column))

    # Convert available numeric columns to numeric values.
    # Invalid/missing values become NaN instead of being fabricated.
    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


def get_city_data(city_name):
    """
    Return the processed record for one city.
    """

    df = process_city_data()

    city_name = normalize_city_name(city_name)

    city = df[
        df["city_name"].map(normalize_city_name) == city_name
    ]

    if city.empty:
        raise ValueError(
            f"City '{city_name}' was not found in the USAS dataset."
        )

    return city.iloc[0].to_dict()
