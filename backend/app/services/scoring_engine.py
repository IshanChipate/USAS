import json
from pathlib import Path
import numpy as np
import pandas as pd

from .data_processor import process_city_data
from .data_loader import normalize_city_name

SCORING_CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "scoring.json"


def load_scoring_config():
    with open(SCORING_CONFIG_PATH, encoding="utf-8") as config_file:
        config = json.load(config_file)
    weights = config.get("weights", {})
    if set(weights) != {
        "air_quality_score", "waste_management_score", "population_density_score",
        "green_space_score", "traffic_pressure_score",
    }:
        raise ValueError("Scoring configuration must define a weight for each of the five indicators.")
    if any(not isinstance(weight, (int, float)) or weight < 0 for weight in weights.values()):
        raise ValueError("Indicator weights must be non-negative numbers.")
    if not abs(sum(weights.values()) - 1.0) < 1e-9:
        raise ValueError("Configured indicator weights must sum to 1.0.")
    thresholds = config.get("problem_thresholds", {})
    problem = thresholds.get("problem_below")
    attention = thresholds.get("needs_attention_below")
    if not isinstance(problem, (int, float)) or not isinstance(attention, (int, float)) or not 0 <= problem < attention <= 100:
        raise ValueError("Problem thresholds must satisfy 0 <= problem_below < needs_attention_below <= 100.")
    return config


# ============================================================
# NORMALIZATION
# ============================================================

def min_max_score(series, higher_is_better=True):
    """
    Normalize a pandas Series to a 0-100 score.

    Missing values remain missing.

    Higher-is-better:
        minimum -> 0
        maximum -> 100

    Lower-is-better:
        minimum -> 100
        maximum -> 0
    """

    series = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan)
    minimum = series.min(skipna=True)
    maximum = series.max(skipna=True)

    # No usable data
    if pd.isna(minimum) or pd.isna(maximum):
        return pd.Series(index=series.index, dtype="float64")

    # All available values are the same
    if minimum == maximum:
        return series.where(series.isna(), 50.0)

    if higher_is_better:
        scores = (
            (series - minimum)
            / (maximum - minimum)
        ) * 100
    else:
        scores = (
            (maximum - series)
            / (maximum - minimum)
        ) * 100

    # Keep missing values as NaN
    scores = scores.where(series.notna())

    # Keep scores between 0 and 100
    return scores.clip(0, 100).round(2)


# ============================================================
# INDICATOR SCORES
# ============================================================

def calculate_indicator_scores(df):
    """
    Calculate normalized 0-100 scores for all available indicators.
    """

    scores = pd.DataFrame(index=df.index)

    # --------------------------------------------------------
    # 1. AIR QUALITY
    # Lower AQI = better
    # --------------------------------------------------------

    if "avg_aqi" in df.columns:
        scores["air_quality_score"] = min_max_score(
            df["avg_aqi"],
            higher_is_better=False
        )
    else:
        scores["air_quality_score"] = None

    # --------------------------------------------------------
    # 2. WASTE MANAGEMENT
    # Higher treatment efficiency = better
    # --------------------------------------------------------

    if "waste_treatment_efficiency_pct" in df.columns:
        scores["waste_management_score"] = min_max_score(
            df["waste_treatment_efficiency_pct"],
            higher_is_better=True
        )
    else:
        scores["waste_management_score"] = None

    # --------------------------------------------------------
    # 3. POPULATION DENSITY
    # Higher density = greater pressure
    # Therefore lower density gets higher score
    # --------------------------------------------------------

    if "population_density_2011_persons_per_km2" in df.columns:
        scores["population_density_score"] = min_max_score(
            df["population_density_2011_persons_per_km2"],
            higher_is_better=False
        )
    else:
        scores["population_density_score"] = None

    # --------------------------------------------------------
    # 4. GREEN SPACE
    # The agreed source field is documented green area as a percentage.
    # --------------------------------------------------------

    if "green_area_pct" in df.columns:
        scores["green_space_score"] = min_max_score(
            df["green_area_pct"],
            higher_is_better=True
        )
    else:
        scores["green_space_score"] = None

    # --------------------------------------------------------
    # 5. TRAFFIC
    #
    # Score only measured congestion rows marked score-eligible by the
    # processed traffic source. Registered vehicles remain an unscored proxy.
    # --------------------------------------------------------

    if "traffic_congestion_value" in df.columns:
        scores["traffic_pressure_score"] = min_max_score(
            df["traffic_congestion_value"],
            higher_is_better=False
        )
    else:
        scores["traffic_pressure_score"] = None

    return scores


# ============================================================
# OVERALL SCORE
# ============================================================

def calculate_overall_scores(df, scores, weights=None):
    """
    Calculate the overall sustainability score.

    Baseline weight:
        Air Quality          = 20%
        Waste Management     = 20%
        Population Density   = 20%
        Green Space          = 20%
        Traffic              = 20%

    If an indicator is unavailable for a city:
        - It is excluded from the calculation.
        - The remaining weights are re-normalized.
        - Missing data is NOT treated as zero.
    """

    weights = weights or load_scoring_config()["weights"]
    default_weights = {
        "air_quality_score": 0.20,
        "waste_management_score": 0.20,
        "population_density_score": 0.20,
        "green_space_score": 0.20,
        "traffic_pressure_score": 0.20
    }

    indicator_names = {
        "air_quality_score": "Air Quality",
        "waste_management_score": "Waste Management",
        "population_density_score": "Population Density",
        "green_space_score": "Green Space",
        "traffic_pressure_score": "Traffic"
    }

    overall_scores = []
    coverage_values = []
    available_counts = []
    missing_indicators = []

    for index in df.index:

        available = {}
        missing = []

        # Check each indicator
        for column in default_weights:

            value = scores.loc[index, column]

            if pd.notna(value):
                available[column] = float(value)
            else:
                missing.append(indicator_names[column])

        # ----------------------------------------------------
        # Calculate score using only available indicators
        # ----------------------------------------------------

        if available:

            available_weight = sum(
                weights[column]
                for column in available
            )

            weighted_score = sum(
                available[column] * weights[column]
                for column in available
            )

            overall_score = weighted_score / available_weight

        else:
            overall_score = None

        # ----------------------------------------------------
        # Data coverage
        # ----------------------------------------------------

        coverage = (
            len(available)
            / len(default_weights)
        ) * 100

        overall_scores.append(
            round(overall_score, 2)
            if overall_score is not None
            else None
        )

        coverage_values.append(
            round(coverage, 2)
        )

        available_counts.append(
            len(available)
        )

        missing_indicators.append(
            missing
        )

    result = scores.copy()

    result["overall_sustainability_score"] = overall_scores

    result["data_coverage_pct"] = coverage_values

    result["available_indicator_count"] = available_counts

    result["missing_indicators"] = missing_indicators
    result["score_status"] = ["Full" if count == len(default_weights) else "Partial" for count in available_counts]

    return result


# ============================================================
# CALCULATE ALL CITY SCORES
# ============================================================

def calculate_scores():
    """
    Process all city data and calculate sustainability scores.
    """

    # Load and process real USAS data
    df = process_city_data()

    # Calculate individual indicator scores
    scores = calculate_indicator_scores(df)

    # Calculate overall scores
    result = calculate_overall_scores(
        df,
        scores,
        load_scoring_config()["weights"],
    )

    # Add city name
    result.insert(
        0,
        "city_name",
        df["city_name"].values
    )

    raw_columns = [
        "avg_aqi", "aqi_poor_or_worse_pct", "aqi_completeness_pct", "air_year",
        "waste_treatment_efficiency_pct", "waste_generated_mt_day", "waste_treated_mt_day", "waste_year",
        "population_density_2011_persons_per_km2", "population_2011", "population_year",
        "green_area_pct", "green_area_km2", "green_year", "traffic_value", "traffic_metric",
        "traffic_data_status", "traffic_year", "traffic_congestion_value",
        "traffic_congestion_metric", "traffic_congestion_unit", "traffic_congestion_year",
        "traffic_congestion_status", "traffic_congestion_source", "traffic_congestion_source_url",
    ]
    for column in raw_columns:
        if column in df.columns:
            result[column] = df[column].values

    return result


# ============================================================
# GET ONE CITY SCORE
# ============================================================

def get_city_score(city_name):
    """
    Return calculated sustainability results for one city.
    """

    results = calculate_scores()

    city_name = normalize_city_name(city_name)

    city = results[
        results["city_name"].map(normalize_city_name)
        == city_name
    ]

    if city.empty:
        raise ValueError(
            f"City '{city_name}' was not found."
        )

    return city.iloc[0].to_dict()
