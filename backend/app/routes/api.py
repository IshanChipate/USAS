# -*- coding: utf-8 -*-
"""JSON API for city assessment, recommendations, impact analysis, and report generation."""

import io
import math
from datetime import date
from flask import Blueprint, g, jsonify, request, send_file

from .auth import require_auth
from ..services.data_loader import get_available_cities, get_city_source_metadata
from ..services.openaq_service import get_air_quality
from ..services.pdf_report_generator import generate_city_pdf_report
from ..services.persistence import log_report_generation, save_scenario
from ..services.problem_detector import INDICATORS, classify_indicators, identify_problem_areas
from ..services.rag_service import build_index as build_rag_index, dependency_status as rag_dependency_status
from ..services.recommendation_engine import generate_recommendations, generate_recommendations_for_city
from ..services.scoring_engine import calculate_scores, get_city_score, load_scoring_config
from ..services.spatial_analysis import fetch_osm_spatial_features, get_spatial_readiness

api_bp = Blueprint("api", __name__)


def _api_error(message, status, code):
    return jsonify({"error": message, "code": code}), status


def _json_safe(value):
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def _assessment(city):
    row = get_city_score(city)
    indicators = []
    source_metadata = get_city_source_metadata(row["city_name"])
    
    live_air = None
    try:
        live_air = get_air_quality(row["city_name"])
    except Exception as err:
        print(f"[API] OpenAQ live air check: {err}")

    for score_key, (name, raw_key, unit, note, year_key) in INDICATORS.items():
        raw_value = row.get(raw_key)
        score_value = row.get(score_key)
        indicator_id = {
            "air_quality_score": "air_quality",
            "waste_management_score": "waste_management",
            "population_density_score": "population_density",
            "green_space_score": "green_space",
            "traffic_pressure_score": "traffic",
        }[score_key]
        provenance = source_metadata.get(indicator_id, {})
        source_note = provenance.get("source") or provenance.get("source_name") or note
        raw_unit = provenance.get("unit") or unit
        direction_note = {
            "air_quality_score": "Lower AQI indicates cleaner air; higher normalized score reflects better air quality.",
            "traffic_pressure_score": "Lower vehicle volume indicates less vehicular pressure; higher normalized score reflects lower pressure.",
            "green_space_score": "Higher green cover indicates greater urban vegetation; higher normalized score reflects more green space.",
            "waste_management_score": "Higher treatment efficiency indicates better municipal waste processing; higher normalized score reflects better performance.",
            "population_density_score": "Lower density indicates less demographic pressure per sq km; higher normalized score reflects lower density.",
        }[score_key]
        indicator_unit = provenance.get("unit") or unit
        metric = None
        metric_status = None
        reference_year = row.get(year_key)
        is_live = False
        live_meta = None

        if score_key == "air_quality_score":
            reference_year = "Latest (2026)"
            if live_air and (live_air.get("status") == "LIVE" or live_air.get("aqi") is not None):
                is_live = (live_air.get("status") == "LIVE")
                live_meta = live_air
                source_note = f"CPCB CAAQMS Baseline with OpenAQ Live Telemetry (Station #{live_air.get('station_id')})"
            else:
                source_note = "CPCB CAAQMS (Latest 2026 Baseline)"

        elif score_key == "traffic_pressure_score":
            metric = row.get("traffic_congestion_metric") or row.get("traffic_metric")
            metric_status = row.get("traffic_congestion_status") or row.get("traffic_data_status")
            if score_value is None or _is_nan(score_value):
                raw_value = row.get("traffic_value")
                indicator_unit = "registered vehicles (non-scoring baseline)" if raw_value is not None and not _is_nan(raw_value) else "unavailable"
                reference_year = row.get("traffic_year")
                metric = "Registered Vehicles (Non-Scoring Context)"
                metric_status = "unscored_context"
            else:
                indicator_unit = row.get("traffic_congestion_unit") or indicator_unit
                reference_year = row.get("traffic_congestion_year")

        ind_dict = {
            "key": score_key,
            "name": name,
            "value": _first_available(raw_value),
            "raw_value": _first_available(raw_value),
            "unit": indicator_unit,
            "metric": metric,
            "metric_status": metric_status,
            "reference_year": _first_available(reference_year, provenance.get("reference_year"), provenance.get("year")),
            "year": _first_available(reference_year, provenance.get("reference_year"), provenance.get("year")),
            "available": score_value is not None and not _is_nan(score_value),
            "score": None if _is_nan(score_value) else round(float(score_value), 2),
            "source": source_note,
            "source_name": provenance.get("source_name") or source_note,
            "source_url": provenance.get("source_url") or ("https://openaq.org" if score_key == "air_quality_score" else None),
            "note": note,
            "direction_note": direction_note,
        }
        if is_live:
            ind_dict["is_live"] = True
        if live_meta:
            ind_dict["live_meta"] = live_meta
        indicators.append(ind_dict)

    spatial = get_spatial_readiness(row["city_name"])
    return {
        "city": row["city_name"],
        "overall_score": None if _is_nan(row["overall_sustainability_score"]) else round(float(row["overall_sustainability_score"]), 2),
        "overall_sustainability_score": None if _is_nan(row["overall_sustainability_score"]) else round(float(row["overall_sustainability_score"]), 2),
        "data_coverage_pct": int(row["data_coverage_pct"]),
        "score_status": row["score_status"],
        "assessment_date": date.today().strftime("%B %d, %Y"),
        "indicators": indicators,
        "indicator_classifications": classify_indicators(row),
        "problem_areas": identify_problem_areas(row),
        "missing_indicators": [item["name"] for item in indicators if item["score"] is None],
        "spatial_feasibility": spatial,
        "live_air_quality": live_air,
        "score_method": "Min-Max scores are relative to the cities in this comparison dataset, not a validated national sustainability index. Weighted Sum Model uses configured equal weights, re-normalized across available indicators for each city.",
    }


def _is_nan(value):
    try:
        return math.isnan(float(value))
    except (TypeError, ValueError):
        return False


def _first_available(*values):
    for value in values:
        if value is not None and not _is_nan(value):
            return value
    return None


@api_bp.get("/cities")
@require_auth
def cities():
    try:
        return jsonify({"cities": get_available_cities()})
    except (FileNotFoundError, ValueError) as error:
        return _api_error(str(error), 503, "dataset_unavailable")


@api_bp.get("/assessment/<path:city>")
@require_auth
def assessment(city):
    try:
        return jsonify(_json_safe(_assessment(city)))
    except ValueError as error:
        return _api_error(str(error), 404, "city_not_found")
    except (FileNotFoundError, KeyError) as error:
        return _api_error(str(error), 503, "dataset_unavailable")


@api_bp.get("/assessment")
@require_auth
def assessments():
    try:
        result = calculate_scores()
        rows = []
        for _, row in result.iterrows():
            rows.append(_json_safe(row.to_dict()))
        return jsonify({"assessments": rows})
    except (FileNotFoundError, ValueError) as error:
        return _api_error(str(error), 503, "dataset_unavailable")


@api_bp.get("/problems/<path:city>")
@require_auth
def problems(city):
    try:
        return jsonify({"city": city, "problem_areas": _json_safe(identify_problem_areas(get_city_score(city)))})
    except ValueError as error:
        return _api_error(str(error), 404, "city_not_found")
    except (FileNotFoundError, KeyError) as error:
        return _api_error(str(error), 503, "dataset_unavailable")


@api_bp.get("/recommendations/<path:city>")
@require_auth
def recommendations(city):
    try:
        city_score = get_city_score(city)
        spatial = get_spatial_readiness(city)
        recs = generate_recommendations_for_city(city, city_score, spatial, include_rag=True)
        return jsonify({"city": city, "recommendations": _json_safe(recs)})
    except ValueError as error:
        return _api_error(str(error), 404, "city_not_found")
    except (FileNotFoundError, KeyError) as error:
        return _api_error(str(error), 503, "dataset_unavailable")


@api_bp.post("/impact/<path:city>")
@require_auth
def impact(city):
    try:
        current = get_city_score(city)
    except ValueError as error:
        return _api_error(str(error), 404, "city_not_found")
    except (FileNotFoundError, KeyError) as error:
        return _api_error(str(error), 503, "dataset_unavailable")
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload, dict):
        return _api_error("Request body must be a JSON object.", 400, "invalid_request")
    key = payload.get("indicator")
    if not isinstance(key, str) or key not in INDICATORS or _is_nan(current.get(key)):
        return _api_error("Choose an available indicator.", 400, "invalid_indicator")
    try:
        improvement = float(payload.get("improvement_points", 10))
    except (TypeError, ValueError):
        return _api_error("improvement_points must be a number.", 400, "invalid_scenario")
    if not 0 < improvement <= 100:
        return _api_error("improvement_points must be greater than 0 and at most 100.", 400, "invalid_scenario")
    baseline = _assessment(city)
    current_indicator = float(current[key])
    projected_indicator = min(100.0, current_indicator + improvement)
    effective_improvement = projected_indicator - current_indicator
    baseline_score = baseline["overall_score"]
    available_count = sum(not _is_nan(current.get(score_key)) for score_key in INDICATORS)
    if baseline_score is None or available_count == 0:
        return _api_error("An overall baseline score is not available for this city.", 422, "baseline_unavailable")
    weights = load_scoring_config()["weights"]
    available_weight = sum(weights[indicator_key] for indicator_key in INDICATORS if not _is_nan(current.get(indicator_key)))
    projected_score = baseline_score + (projected_indicator - current_indicator) * weights[key] / available_weight
    result = {
        "city": current["city_name"],
        "indicator": INDICATORS[key][0],
        "indicator_key": key,
        "baseline_raw_value": current.get(INDICATORS[key][1]),
        "baseline_indicator_score": round(current_indicator, 2),
        "projected_indicator_score": round(projected_indicator, 2),
        "baseline_overall_score": baseline_score,
        "projected_overall_score": round(projected_score, 2),
        "overall_score_change": round(projected_score - baseline_score, 2),
        "assumed_normalized_score_change_points": improvement,
        "effective_normalized_score_change_points": round(effective_improvement, 2),
        "data_coverage_pct": baseline["data_coverage_pct"],
        "score_status": baseline["score_status"],
        "missing_indicators": baseline["missing_indicators"],
        "assumptions": ["Only the selected normalized indicator score changes.", "All other indicator scores and the baseline data coverage remain unchanged.", "This scenario does not predict a real-world outcome or infer a causal coefficient."],
        "constraints": baseline["spatial_feasibility"]["limitations"],
        "uncertainty": "User-defined score change; no empirical impact coefficient is applied.",
        "note": "Illustrative score scenario only; it is not a forecast or a guaranteed real-world effect.",
    }
    user_id = getattr(g, "current_user", {}).get("id", "anonymous")
    result["persistence"] = save_scenario(result, user_id=user_id)
    return jsonify(_json_safe(result))


@api_bp.get("/spatial/<path:city>")
@require_auth
def spatial_status(city):
    try:
        get_city_score(city)
    except ValueError as error:
        return _api_error(str(error), 404, "city_not_found")
    except (FileNotFoundError, KeyError) as error:
        return _api_error(str(error), 503, "dataset_unavailable")
    return jsonify(_json_safe(get_spatial_readiness(city)))


@api_bp.get("/spatial/features/<path:city>")
@require_auth
def spatial_features(city):
    try:
        get_city_score(city)
    except ValueError as error:
        return _api_error(str(error), 404, "city_not_found")
    except (FileNotFoundError, KeyError) as error:
        return _api_error(str(error), 503, "dataset_unavailable")
    return jsonify(_json_safe(fetch_osm_spatial_features(city)))


@api_bp.get("/live/air-quality/<path:city>")
@require_auth
def live_air_quality(city):
    try:
        get_city_score(city)
    except ValueError as error:
        return _api_error(str(error), 404, "city_not_found")
    except (FileNotFoundError, KeyError) as error:
        return _api_error(str(error), 503, "dataset_unavailable")
    data = get_air_quality(city)
    if data:
        return jsonify(_json_safe(data))
    return jsonify({
        "city": city,
        "status": "UNAVAILABLE",
        "message": f"No live or cached OpenAQ station measurements currently available for {city}.",
        "note": "Historical CPCB daily bulletin AQI observations are preserved in the core assessment.",
    })


@api_bp.get("/rag/status")
@require_auth
def rag_status():
    return jsonify(rag_dependency_status())


@api_bp.post("/rag/index")
@require_auth
def rag_index():
    result = build_rag_index()
    return jsonify(result), (200 if result.get("built") else 503)


@api_bp.get("/report/<path:city>")
@require_auth
def report(city):
    try:
        result = _assessment(city)
    except ValueError as error:
        return _api_error(str(error), 404, "city_not_found")
    except (FileNotFoundError, KeyError) as error:
        return _api_error(str(error), 503, "dataset_unavailable")
    result["report_title"] = "Urban Sustainability Assessment Report"
    result["weights"] = load_scoring_config()["weights"]
    result["recommendations"] = generate_recommendations_for_city(city, result, result["spatial_feasibility"], include_rag=True)
    result["limitations"] = [
        "Indicator coverage and reference years differ across cities.",
        "Traffic is scored solely where verified congestion measurements exist; unmeasured cities have Traffic marked N/A and excluded from WSM scoring, with registered vehicle counts provided as non-scoring contextual background.",
        "Green-space coverage is incomplete; available area values are not necessarily comparable or per-capita.",
        "Analytical scores reflect comparative state ranking and do not replace statutory municipal environmental clearances.",
    ]
    return jsonify(_json_safe(result))


@api_bp.get("/report/<path:city>/pdf")
@require_auth
def report_pdf(city):
    """Generate and download publication-quality PDF report."""
    try:
        result = _assessment(city)
    except ValueError as error:
        return _api_error(str(error), 404, "city_not_found")
    except (FileNotFoundError, KeyError) as error:
        return _api_error(str(error), 503, "dataset_unavailable")

    result["report_title"] = "Urban Sustainability Assessment Report"
    result["weights"] = load_scoring_config()["weights"]
    result["recommendations"] = generate_recommendations_for_city(city, result, result["spatial_feasibility"], include_rag=True)

    pdf_bytes = generate_city_pdf_report(result)
    user_id = getattr(g, "current_user", {}).get("id", "anonymous")
    log_report_generation(city, result, user_id=user_id)

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"USAS_{city}_Sustainability_Report.pdf",
    )
