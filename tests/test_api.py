"""Smoke, contract, and security verification tests for USAS."""

import unittest
import math
import json
import os
import tempfile
import types
from pathlib import Path
from unittest.mock import patch

from backend.app import create_app
from backend.app.services.data_loader import get_available_cities, get_city_source_metadata, load_city_data
from backend.app.services.data_processor import process_city_data
from backend.app.services.problem_detector import classify_indicators, identify_problem_areas
from backend.app.services.scoring_engine import calculate_indicator_scores, calculate_overall_scores, get_city_score, load_scoring_config, min_max_score
from backend.app.services.spatial_analysis import get_spatial_readiness
from backend.app.services import persistence, rag_service
from backend.app.services.auth_service import (
    auth_service,
    hash_password,
    generate_token,
    INITIAL_ADMIN_EMAIL,
    INITIAL_ADMIN_PASSWORD,
    INITIAL_ADMIN_NAME,
)
import pandas as pd


class ScoringTests(unittest.TestCase):
    def test_min_max_score_respects_direction_and_missing_values(self):
        values = pd.Series([1.0, 2.0, 3.0, None])
        scores = min_max_score(values).tolist()
        self.assertEqual(scores[:3], [0.0, 50.0, 100.0])
        self.assertTrue(math.isnan(scores[3]))
        self.assertEqual(min_max_score(values, higher_is_better=False).iloc[:3].tolist(), [100.0, 50.0, 0.0])

    def test_constant_values_score_50_and_preserve_missing(self):
        scores = min_max_score(pd.Series([5.0, 5.0, None]))
        self.assertEqual(scores.iloc[:2].tolist(), [50.0, 50.0])
        self.assertTrue(math.isnan(scores.iloc[2]))

    def test_weights_are_renormalized_for_available_indicators(self):
        df = pd.DataFrame({"city_name": ["A", "B"]})
        scores = pd.DataFrame({
            "air_quality_score": [100.0, 0.0],
            "waste_management_score": [float("nan"), 100.0],
            "population_density_score": [0.0, 50.0],
            "green_space_score": [float("nan"), 50.0],
            "traffic_pressure_score": [float("nan"), 100.0],
        })
        result = calculate_overall_scores(df, scores)
        self.assertEqual(result.loc[0, "overall_sustainability_score"], 50.0)
        self.assertEqual(result.loc[0, "data_coverage_pct"], 40.0)
        self.assertEqual(result.loc[0, "score_status"], "Partial")
        self.assertEqual(result.loc[1, "score_status"], "Full")

    def test_no_available_indicators_produce_no_overall_score(self):
        df = pd.DataFrame({"city_name": ["No Data"]})
        scores = pd.DataFrame({key: [float("nan")] for key in load_scoring_config()["weights"]})
        result = calculate_overall_scores(df, scores)
        self.assertIsNone(result.loc[0, "overall_sustainability_score"])
        self.assertEqual(result.loc[0, "data_coverage_pct"], 0.0)
        self.assertEqual(result.loc[0, "available_indicator_count"], 0)
        self.assertEqual(result.loc[0, "score_status"], "Partial")

    def test_green_space_uses_documented_percentage_not_raw_area(self):
        df = process_city_data()
        pune = df[df["city_name"] == "Pune"].iloc[0]
        scores = calculate_indicator_scores(df)
        self.assertAlmostEqual(float(pune["green_area_pct"]), 0.7156, places=4)
        self.assertEqual(scores.loc[pune.name, "green_space_score"], 0.33)

    def test_thresholds_classify_problem_attention_acceptable_and_missing(self):
        score = {
            "air_quality_score": 39.99,
            "waste_management_score": 40,
            "population_density_score": 59.99,
            "green_space_score": 60,
            "traffic_pressure_score": float("nan"),
        }
        self.assertEqual([item["classification"] for item in classify_indicators(score)], [
            "Problem Area", "Needs Attention", "Needs Attention", "Acceptable", "Unavailable",
        ])

    def test_problem_areas_only_include_low_available_scores(self):
        areas = identify_problem_areas({"air_quality_score": 20, "waste_management_score": 70, "green_space_score": None})
        self.assertEqual([area["indicator"] for area in areas], ["Air Quality"])
        self.assertEqual(areas[0]["severity"], "high")


class AuthenticatedTestClient:
    def __init__(self, raw_client, token):
        self._raw = raw_client
        self._token = token

    def set_token(self, token):
        self._token = token

    def get(self, *args, **kwargs):
        headers = kwargs.setdefault("headers", {})
        if "Authorization" not in headers:
            headers["Authorization"] = f"Bearer {self._token}"
        return self._raw.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        headers = kwargs.setdefault("headers", {})
        if "Authorization" not in headers:
            headers["Authorization"] = f"Bearer {self._token}"
        return self._raw.post(*args, **kwargs)

    def put(self, *args, **kwargs):
        headers = kwargs.setdefault("headers", {})
        if "Authorization" not in headers:
            headers["Authorization"] = f"Bearer {self._token}"
        return self._raw.put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        headers = kwargs.setdefault("headers", {})
        if "Authorization" not in headers:
            headers["Authorization"] = f"Bearer {self._token}"
        return self._raw.delete(*args, **kwargs)


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure Ishan Chipate exists in user store
        auth_service._ensure_storage()
        raw = create_app().test_client()
        token = generate_token("usr-ishan-admin", INITIAL_ADMIN_EMAIL, "Administrator")
        cls.client = AuthenticatedTestClient(raw, token)
        cls.raw_client = raw

    def test_health_and_city_list(self):
        self.assertEqual(self.client.get("/api/health").status_code, 200)
        response = self.client.get("/api/cities")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["cities"])

    def test_assessment_payload_has_coverage_and_indicators(self):
        response = self.client.get("/api/assessment/Pune")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["city"], "Pune")
        self.assertIn("data_coverage_pct", response.json)
        self.assertEqual(len(response.json["indicators"]), 5)
        self.assertIn(response.json["score_status"], ("Full", "Partial"))
        self.assertTrue(any(item["value"] is not None for item in response.json["indicators"]))
        self.assertIn("reference_year", response.json["indicators"][0])

    def test_city_lookup_is_case_and_whitespace_insensitive(self):
        result = get_city_score("  pUnE   ")
        self.assertEqual(result["city_name"], "Pune")
        self.assertEqual(len(get_available_cities()), 42)

    def test_component_source_metadata_preserves_available_links(self):
        sources = get_city_source_metadata("Pune")
        self.assertEqual(sources["traffic"]["source"], "TomTom Traffic Index 2025")
        self.assertIn("tomtom.com", sources["traffic"]["source_url"])
        self.assertEqual(sources["green_space"]["unit"], "%")
        self.assertEqual(sources["waste_management"]["source_page"], 35)

    def test_traffic_without_congestion_is_excluded_from_scoring_with_contextual_baseline(self):
        nagpur = self.client.get("/api/assessment/Nagpur").json
        traffic = next(item for item in nagpur["indicators"] if item["name"] == "Traffic")
        self.assertFalse(traffic["available"])
        self.assertIsNone(traffic["score"])
        self.assertEqual(traffic["unit"], "registered vehicles (non-scoring baseline)")
        self.assertEqual(traffic["value"], 2227000)
        self.assertEqual(nagpur["data_coverage_pct"], 80)
        self.assertEqual(nagpur["score_status"], "Partial")
        self.assertIn("Traffic", nagpur["missing_indicators"])

    def test_measured_traffic_source_is_used_when_score_eligible(self):
        mumbai = self.client.get("/api/assessment/Mumbai").json
        traffic = next(item for item in mumbai["indicators"] if item["name"] == "Traffic")
        self.assertTrue(traffic["available"])
        self.assertEqual(traffic["value"], 63.2)
        self.assertEqual(traffic["unit"], "percent")
        self.assertEqual(traffic["metric"], "average_congestion_level")
        self.assertIsNotNone(traffic["score"])

    def test_master_loader_rejects_duplicate_normalized_city_names(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as temp_dir:
            path = Path(temp_dir) / "master.csv"
            path.write_text("city_name,value\nPune,1\n pune ,2\n", encoding="utf-8")
            with patch("backend.app.services.data_loader.MASTER_DATA_PATH", path):
                with self.assertRaisesRegex(ValueError, "duplicate city names"):
                    load_city_data()

    def test_spatial_and_rag_readiness_report_missing_inputs_honestly(self):
        spatial = get_spatial_readiness("Pune")
        self.assertFalse(spatial["available"])
        self.assertFalse(spatial["candidate_analysis_available"])
        self.assertEqual(spatial["candidate_count"], 0)
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as temp_dir:
            with patch.object(rag_service, "KNOWLEDGE_DIR", Path(temp_dir) / "no-documents"), patch.object(rag_service, "INDEX_DIR", Path(temp_dir) / "no-index"):
                result = rag_service.build_index()
                self.assertEqual(result["status"], "no_documents")

    def test_rag_retrieval_preserves_document_metadata(self):
        import numpy as np
        class FakeIndex:
            def search(self, vector, limit):
                return np.array([[0.91]]), np.array([[0]])
        class FakeEncoder:
            def encode(self, texts, **kwargs):
                return np.array([[1.0, 0.0]], dtype="float32")
        fake_faiss = types.SimpleNamespace(read_index=lambda path: FakeIndex())
        fake_transformers = types.SimpleNamespace(SentenceTransformer=lambda model: FakeEncoder())
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as temp_dir:
            index_dir = Path(temp_dir)
            (index_dir / "index.faiss").write_bytes(b"fixture index marker")
            (index_dir / "metadata.json").write_text(json.dumps([{
                "title": "Fixture planning guideline", "source_url": "https://example.test/source",
                "publication_year": 2024, "page": 7, "document_path": "fixture.pdf", "text": "Public park access guidance.",
            }]), encoding="utf-8")
            with patch.object(rag_service, "INDEX_DIR", index_dir), patch.object(rag_service, "_get_encoder", return_value=FakeEncoder()), patch.dict("sys.modules", {"faiss": fake_faiss, "sentence_transformers": fake_transformers}):
                evidence = rag_service.retrieve_evidence("park access")
        self.assertEqual(evidence["evidence"][0]["title"], "Fixture planning guideline")
        self.assertEqual(evidence["evidence"][0]["page"], 7)
        self.assertEqual(evidence["evidence"][0]["source_url"], "https://example.test/source")

    def test_gemini_missing_key_is_reported_without_external_call(self):
        evidence = [{"evidence_id": "E1", "excerpt": "source excerpt"}]
        with patch.dict(os.environ, {"GEMINI_API_KEY": ""}):
            result = rag_service.generate_grounded_text({"indicator": "Air Quality"}, evidence)
        self.assertEqual(result["status"], "missing_api_key")
        self.assertIsNone(result["text"])

    def test_gemini_rate_limit_is_returned_without_exception_details(self):
        import sys
        class RateLimitError(Exception):
            status_code = 429
        class FailingModels:
            def generate_content(self, **kwargs):
                raise RateLimitError("provider-specific internal detail")
        fake_google = types.ModuleType("google")
        fake_google.__path__ = []
        fake_google.genai = types.SimpleNamespace(Client=lambda **kwargs: types.SimpleNamespace(models=FailingModels()))
        context = [{"evidence_id": "E1", "title": "A source", "excerpt": "A cited excerpt"}]
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}), patch.dict(sys.modules, {"google": fake_google}):
            result = rag_service.generate_grounded_text({"indicator": "Air Quality"}, context)
        self.assertEqual(result["status"], "rate_limited")
        self.assertIsNone(result["text"])
        self.assertNotIn("provider-specific", result["message"])

    def test_mongo_unconfigured_response_does_not_claim_a_save(self):
        with patch.dict(os.environ, {"MONGODB_URI": ""}):
            result = persistence.save_scenario({"city": "Pune"})
        self.assertFalse(result["saved"])
        self.assertEqual(result["status"], "not_configured")

    def test_unknown_city_and_invalid_impact_are_rejected(self):
        self.assertEqual(self.client.get("/api/assessment/Atlantis").status_code, 404)
        response = self.client.post("/api/impact/Pune", json={"indicator": "unknown"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["code"], "invalid_indicator")
        self.assertEqual(self.client.post("/api/impact/Pune", json=[]).status_code, 400)
        self.assertEqual(self.client.post("/api/impact/Pune", json={"indicator": "air_quality_score", "improvement_points": 101}).status_code, 400)

    def test_missing_master_dataset_returns_json_service_error(self):
        from backend.app.services import data_loader
        with patch.object(data_loader, "MASTER_DATA_PATH", Path("Z:/missing/USAS_master.csv")):
            response = self.client.get("/api/cities")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json["code"], "dataset_unavailable")

    def test_report_and_impact_return_explanatory_payloads(self):
        report = self.client.get("/api/report/Pune")
        self.assertEqual(report.status_code, 200)
        self.assertIn("limitations", report.json)
        city_data = self.client.get("/api/assessment/Pune").json
        available = next(item for item in city_data["indicators"] if item["available"])
        with patch.dict(os.environ, {"MONGODB_URI": ""}):
            impact = self.client.post("/api/impact/Pune", json={"indicator": available["key"], "improvement_points": 5})
        self.assertEqual(impact.status_code, 200)
        self.assertIn("note", impact.json)
        self.assertIn("baseline_raw_value", impact.json)
        self.assertIn("assumptions", impact.json)
        self.assertFalse(impact.json["persistence"]["saved"])
        self.assertIn("overall_score_change", impact.json)

    def test_live_air_quality_endpoint_handles_known_and_unknown_cities(self):
        self.assertEqual(self.client.get("/api/live/air-quality/Atlantis").status_code, 404)
        response = self.client.get("/api/live/air-quality/Pune")
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json)
        self.assertIn("city", response.json)

    def test_rag_status_reports_dependency_and_index_state(self):
        response = self.client.get("/api/rag/status")
        self.assertEqual(response.status_code, 200)
        self.assertIn("knowledge_directory", response.json)
        self.assertIn("document_count", response.json)

    def test_pdf_report_generation_endpoint(self):
        """PDF endpoint generates a valid binary application/pdf payload."""
        res = self.client.get("/api/report/Pune/pdf")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.mimetype, "application/pdf")
        self.assertTrue(len(res.data) > 1000)
        self.assertTrue(res.data.startswith(b"%PDF"))

    def test_unauthenticated_requests_are_rejected(self):
        """Protected assessment and report endpoints reject unauthenticated requests with 401."""
        endpoints = [
            "/api/cities",
            "/api/assessment/Pune",
            "/api/report/Pune",
            "/api/report/Pune/pdf",
            "/api/problems/Pune",
            "/api/recommendations/Pune",
            "/api/rag/status",
        ]
        for ep in endpoints:
            res = self.raw_client.get(ep)
            self.assertEqual(res.status_code, 401, f"Endpoint {ep} should require authentication")
            self.assertEqual(res.json["code"], "unauthorized")

        post_res = self.raw_client.post("/api/impact/Pune", json={})
        self.assertEqual(post_res.status_code, 401)

    # =========================================================================
    # AUTHENTICATION & ACCESS CONTROL INTEGRITY TESTS
    # =========================================================================

    def test_ishan_chipate_admin_authentication_and_password_change(self):
        """Test single preconfigured admin authentication and forced password change workflow."""
        # Authenticate Ishan Chipate with initial password
        res = self.raw_client.post("/api/auth/login", json={
            "email": INITIAL_ADMIN_EMAIL,
            "password": INITIAL_ADMIN_PASSWORD,
        })
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json["success"])
        token = res.json["token"]
        user = res.json["user"]
        self.assertEqual(user["name"], INITIAL_ADMIN_NAME)
        self.assertEqual(user["role"], "Administrator")
        self.assertTrue(user["must_change_password"])

        # Change password to new password
        change_res = self.raw_client.post(
            "/api/auth/change-password",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "current_password": INITIAL_ADMIN_PASSWORD,
                "new_password": "NewPlan@2026Safe!",
            },
        )
        self.assertEqual(change_res.status_code, 200)

        # Login again with new password
        new_login = self.raw_client.post("/api/auth/login", json={
            "email": INITIAL_ADMIN_EMAIL,
            "password": "NewPlan@2026Safe!",
        })
        self.assertEqual(new_login.status_code, 200)
        self.assertFalse(new_login.json["user"]["must_change_password"])

        # Reset password back to INITIAL_ADMIN_PASSWORD so test suite remains idempotent
        self.raw_client.post(
            "/api/auth/change-password",
            headers={"Authorization": f"Bearer {new_login.json['token']}"},
            json={
                "current_password": "NewPlan@2026Safe!",
                "new_password": INITIAL_ADMIN_PASSWORD,
            },
        )

    def test_registration_assigns_pending_verification_and_blocks_access(self):
        """Prospective official registration receives PENDING_VERIFICATION and cannot log in until approved."""
        test_email = "neha.patil@punecorp.gov.in"
        reg_payload = {
            "name": "Smt. Neha Patil",
            "email": test_email,
            "password": "Password123!",
            "designation": "Assistant Director of Town Planning",
            "department": "Pune Municipal Corporation",
            "employee_id": "MH-PMC-TP-2024-082",
            "verification_evidence": "Government Resolution UDD/2024/CR-12",
        }

        # Clean any prior user with same email
        users = [u for u in auth_service._read_users() if u["email"] != test_email]
        auth_service._write_users(users)

        # Register
        res = self.raw_client.post("/api/auth/register", json=reg_payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json["user"]["status"], "PENDING_VERIFICATION")

        # Unapproved user cannot login (403 pending_verification)
        login_res = self.raw_client.post("/api/auth/login", json={
            "email": test_email,
            "password": "Password123!",
        })
        self.assertEqual(login_res.status_code, 403)
        self.assertEqual(login_res.json["code"], "pending_verification")

        # Ishan Chipate (Administrator) inspects pending registrations
        pending_res = self.client.get("/api/auth/pending-users")
        self.assertEqual(pending_res.status_code, 200)
        pending_emails = [u["email"] for u in pending_res.json["pending_users"]]
        self.assertIn(test_email, pending_emails)

        # Administrator approves Neha Patil
        user_id = res.json["user"]["id"]
        approve_res = self.client.post(f"/api/auth/users/{user_id}/approve")
        self.assertEqual(approve_res.status_code, 200)

        # Now Neha Patil CAN log in
        login_after_approval = self.raw_client.post("/api/auth/login", json={
            "email": test_email,
            "password": "Password123!",
        })
        self.assertEqual(login_after_approval.status_code, 200)
        self.assertEqual(login_after_approval.json["user"]["status"], "ACTIVE")

        # Neha Patil can access protected city assessment
        neha_token = login_after_approval.json["token"]
        neha_client = AuthenticatedTestClient(self.raw_client, neha_token)
        city_res = neha_client.get("/api/assessment/Pune")
        self.assertEqual(city_res.status_code, 200)

        # Non-admin cannot access user management endpoints (403 forbidden)
        users_res = neha_client.get("/api/auth/users")
        self.assertEqual(users_res.status_code, 403)


if __name__ == "__main__":
    unittest.main()
