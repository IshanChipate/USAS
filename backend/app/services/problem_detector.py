"""Indicator classification and problem detection based on configurable thresholds."""

import math
from .scoring_engine import get_city_score


# Initial project thresholds; not officially validated standards.
PROBLEM_THRESHOLD = 40.0
ATTENTION_THRESHOLD = 60.0

# 5 Indicators: (Name, Raw Field, Unit, Note, Year Field)
INDICATORS = {
    "air_quality_score": (
        "Air Quality",
        "avg_aqi",
        "AQI",
        "CPCB daily bulletin average AQI (lower is better)",
        "air_year",
    ),
    "waste_management_score": (
        "Waste Management",
        "waste_treatment_efficiency_pct",
        "%",
        "MPCB treated waste divided by generated waste (higher is better)",
        "waste_year",
    ),
    "population_density_score": (
        "Population Density",
        "population_density_2011_persons_per_km2",
        "people/km²",
        "Census 2011 population divided by geographic area (lower density treated as lower pressure)",
        "population_year",
    ),
    "green_space_score": (
        "Green Space",
        "green_area_pct",
        "%",
        "Documented green space coverage percentage (higher is better)",
        "green_year",
    ),
    "traffic_pressure_score": (
        "Traffic",
        "traffic_congestion_value",
        "%",
        "Measured congestion level or non-scoring vehicle baseline",
        "traffic_year",
    ),
}

INDICATOR_SCORE_COLUMNS = {key: val[0] for key, val in INDICATORS.items()}


def _is_nan(value):
    if value is None:
        return True
    try:
        val = float(value)
        return math.isnan(val) or not math.isfinite(val)
    except (TypeError, ValueError):
        return True


def classify_indicator(score):
    """Classify a single normalized indicator score."""
    if _is_nan(score):
        return "Unavailable"

    score_val = float(score)
    if score_val < PROBLEM_THRESHOLD:
        return "Problem Area"
    if score_val < ATTENTION_THRESHOLD:
        return "Needs Attention"
    return "Acceptable"


def classify_indicators(row_or_scores):
    """
    Classify all five indicator scores in a consistent order.
    Returns list of classification objects with metadata.
    """
    classifications = []
    for score_key, (name, raw_key, unit, note, year_key) in INDICATORS.items():
        score = row_or_scores.get(score_key)
        status = classify_indicator(score)
        score_val = round(float(score), 2) if status != "Unavailable" else None

        # Build informative metric description
        metric_desc = note
        raw_val = row_or_scores.get(raw_key)
        ref_year = row_or_scores.get(year_key)
        indicator_unit = unit

        if score_key == "traffic_pressure_score":
            if score_val is None:
                traffic_val = row_or_scores.get("traffic_value")
                if traffic_val is not None and not _is_nan(traffic_val):
                    metric_desc = "Registered vehicles provided as contextual baseline; not scored as congestion."
                    raw_val = traffic_val
                    indicator_unit = "registered vehicles (non-scoring baseline)"
                    ref_year = row_or_scores.get("traffic_year") or 2022
                else:
                    metric_desc = "Traffic data unavailable; not scored as congestion."
            else:
                metric_desc = (
                    row_or_scores.get("traffic_congestion_metric")
                    or "Measured traffic congestion level (higher congestion = lower score)."
                )

        is_available = (status != "Unavailable") or (raw_val is not None and not _is_nan(raw_val))

        classifications.append({
            "indicator": name,
            "key": score_key,
            "score": score_val,
            "classification": status,
            "available": is_available,
            "metric_description": metric_desc,
            "raw_value": raw_val,
            "unit": indicator_unit,
            "reference_year": ref_year,
        })

    return classifications


def identify_problem_areas(row_or_scores, threshold=PROBLEM_THRESHOLD):
    """
    Identify indicators whose normalized score is below the problem threshold (< 40).
    Missing/NaN indicators are excluded from problem areas.
    """
    classifications = classify_indicators(row_or_scores)
    problems = []
    for item in classifications:
        if item["classification"] == "Problem Area":
            problems.append({
                "indicator": item["indicator"],
                "key": item["key"],
                "score": item["score"],
                "severity": "high",
                "classification": item["classification"],
                "metric_description": item["metric_description"],
                "raw_value": item["raw_value"],
                "unit": item["unit"],
                "reference_year": item["reference_year"],
                "threshold": threshold,
            })
    return problems


def detect_problems(city_name):
    """Assess a city and classify its available indicator scores."""
    result = get_city_score(city_name)
    classifications = classify_indicators(result)

    indicators = {}
    problem_areas = []
    needs_attention = []
    unavailable_indicators = []

    for item in classifications:
        name = item["indicator"]
        status = item["classification"]
        indicators[name] = {
            "score": item["score"],
            "status": status,
            "metric_description": item["metric_description"],
        }
        if status == "Problem Area":
            problem_areas.append(name)
        elif status == "Needs Attention":
            needs_attention.append(name)
        elif status == "Unavailable":
            unavailable_indicators.append(name)

    try:
        coverage = float(result.get("data_coverage_pct", 0) or 0)
    except (TypeError, ValueError):
        coverage = 0.0

    return {
        "city_name": result.get("city_name", city_name),
        "overall_sustainability_score": result.get("overall_sustainability_score"),
        "data_coverage_pct": coverage,
        "available_indicator_count": result.get("available_indicator_count", 0),
        "missing_indicators": result.get("missing_indicators", []),
        "indicators": indicators,
        "indicator_classifications": classifications,
        "problem_areas": problem_areas,
        "needs_attention": needs_attention,
        "unavailable_indicators": unavailable_indicators,
        "score_status": "Full" if coverage >= 100 else "Partial",
    }
