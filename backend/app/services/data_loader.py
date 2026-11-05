from pathlib import Path
import re
import pandas as pd


# Project root:
# E:\Project\USAS
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Processed master dataset
MASTER_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "master"
    / "USAS_city_indicator_master_clean.csv"
)


def load_city_data():
    """
    Load the processed USAS city indicator dataset.
    """

    if not MASTER_DATA_PATH.exists():
        raise FileNotFoundError(
            f"USAS master dataset not found at: {MASTER_DATA_PATH}"
        )

    df = pd.read_csv(MASTER_DATA_PATH)

    if df.empty:
        raise ValueError("USAS master dataset is empty.")

    if "city_name" not in df.columns:
        raise ValueError("USAS master dataset is missing the required city_name column.")

    df["city_name"] = df["city_name"].astype("string").str.strip()
    if df["city_name"].isna().any() or df["city_name"].eq("").any():
        raise ValueError("USAS master dataset contains blank city names.")
    normalized_names = df["city_name"].map(normalize_city_name)
    duplicates = df.loc[normalized_names.duplicated(keep=False), "city_name"].unique().tolist()
    if duplicates:
        raise ValueError(f"USAS master dataset contains duplicate city names: {', '.join(duplicates)}")

    return df


def normalize_city_name(value):
    """Normalize whitespace and casing for exact, conservative city matching."""
    return re.sub(r"\s+", " ", str(value or "")).strip().casefold()


def get_available_cities():
    """
    Return all cities available in the dataset.
    """

    df = load_city_data()

    cities = (
        df["city_name"]
        .dropna()
        .astype(str)
        .str.strip()
        .sort_values()
        .unique()
        .tolist()
    )

    return cities


def get_city_source_metadata(city_name):
    """Read per-indicator provenance from the existing processed component files."""
    from .data_processor import PROJECT_DATA_ROOT

    key = normalize_city_name(city_name)
    specs = {
        "air_quality": ("air_quality/USAS_air_quality_processed.csv", "avg_aqi", "AQI", "source", "source_coverage", "year"),
        "traffic": ("traffic/USAS_traffic_processed.csv", "traffic_value", None, "source", "interpretation", "reference_year"),
        "green_space": ("green_space/USAS_green_space_processed.csv", "green_area_pct", "%", "source", "method_note", "reference_year"),
        "waste_management": ("waste/USAS_waste_indicator_2023.csv", "treatment_efficiency_pct", "%", None, None, "waste_year"),
        "population_density": ("population/USAS_population_indicator_2011_compact.csv", "population_density_2011_persons_per_km2", "people/km²", "density_source", None, "year"),
    }
    results = {}
    for indicator, (relative_path, value_field, unit, source_field, note_field, year_field) in specs.items():
        path = PROJECT_DATA_ROOT / relative_path
        if not path.exists():
            results[indicator] = {"source_file": relative_path, "available": False}
            continue
        try:
            frame = pd.read_csv(path)
        except (OSError, pd.errors.ParserError):
            results[indicator] = {"source_file": relative_path, "available": False}
            continue
        city_column = "city_name" if "city_name" in frame.columns else None
        if city_column:
            matches = frame[frame[city_column].map(normalize_city_name) == key]
        else:
            matches = frame.iloc[0:0]
        if indicator == "waste_management" and matches.empty:
            master = load_city_data()
            master_match = master[master["city_name"].map(normalize_city_name) == key]
            if not master_match.empty and {"waste_generated_mt_day", "waste_treated_mt_day"}.issubset(frame.columns):
                master_row = master_match.iloc[0]
                generated = pd.to_numeric(frame["waste_generated_mt_day"], errors="coerce")
                treated = pd.to_numeric(frame["waste_treated_mt_day"], errors="coerce")
                expected_generated = pd.to_numeric(pd.Series([master_row.get("waste_generated_mt_day")]), errors="coerce").iloc[0]
                expected_treated = pd.to_numeric(pd.Series([master_row.get("waste_treated_mt_day")]), errors="coerce").iloc[0]
                if pd.notna(expected_generated) and pd.notna(expected_treated):
                    matched_rows = frame[((generated - expected_generated).abs() < 1e-6) & ((treated - expected_treated).abs() < 1e-6)]
                    if len(matched_rows) == 1:
                        matches = matched_rows
        # Keep the source row for the year represented by the master record.
        if indicator in ("air_quality", "green_space") and not matches.empty and year_field in matches.columns:
            master = load_city_data()
            master_match = master[master["city_name"].map(normalize_city_name) == key]
            target_column = "air_year" if indicator == "air_quality" else "green_year"
            target_year = master_match.iloc[0].get(target_column) if not master_match.empty else None
            if pd.notna(target_year):
                matches = matches[pd.to_numeric(matches[year_field], errors="coerce") == float(target_year)]
        row = matches.iloc[0].to_dict() if not matches.empty else {}
        source_url = row.get("source_url")
        source = row.get(source_field) if source_field else None
        reference_year = row.get(year_field)
        if indicator == "waste_management":
            source = "FinalMSWAnnualReport2023Revised.pdf (Maharashtra municipal solid waste annual report)"
            master = load_city_data()
            master_match = master[master["city_name"].map(normalize_city_name) == key]
            reference_year = master_match.iloc[0].get("waste_year") if not master_match.empty else None
        results[indicator] = {
            "available": True,
            "source_file": relative_path,
            "source": _clean_metadata(source),
            "source_secondary": _clean_metadata(row.get("population_source")) if indicator == "population_density" else None,
            "source_url": _clean_metadata(source_url),
            "reference_year": _clean_metadata(reference_year),
            "unit": _clean_metadata(row.get("traffic_unit")) or unit,
            "metric_description": _clean_metadata(row.get(note_field)) if note_field else None,
            "source_page": _clean_metadata(row.get("source_page")),
            "source_record": _clean_metadata(row.get("name")),
        }
    return results


def _clean_metadata(value):
    if value is None or pd.isna(value):
        return None
    if hasattr(value, "item"):
        value = value.item()
    return value
