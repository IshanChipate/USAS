# -*- coding: utf-8 -*-
"""
Database Persistence Service for USAS
Manages MongoDB Atlas collections: users, assessments, recommendations,
impact_scenarios, and reports. Provides graceful fallback when unconfigured.
"""

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
except ImportError:
    pass

_mongo_client = None


def get_db():
    """Retrieve active MongoDB database instance or None if not configured or unreachable."""
    global _mongo_client
    uri = os.getenv("MONGODB_URI", "").strip()
    if not uri:
        return None
    try:
        from pymongo import MongoClient

        if _mongo_client is None:
            _mongo_client = MongoClient(uri, serverSelectionTimeoutMS=2500)
            _mongo_client.admin.command("ping")
        db_name = os.getenv("MONGODB_DATABASE", "usas")
        return _mongo_client[db_name]
    except Exception:
        _mongo_client = None
        return None


def get_persistence_status() -> Dict[str, Any]:
    """Check connectivity to MongoDB Atlas database."""
    uri = os.getenv("MONGODB_URI", "").strip()
    if not uri:
        return {
            "configured": False,
            "connected": False,
            "status": "not_configured",
            "message": "MongoDB Atlas is not configured; running with in-memory & file storage fallback.",
        }
    db = get_db()
    if db is not None:
        return {
            "configured": True,
            "connected": True,
            "status": "connected",
            "database": os.getenv("MONGODB_DATABASE", "usas"),
            "message": "MongoDB Atlas connected successfully.",
        }
    return {
        "configured": True,
        "connected": False,
        "status": "connection_error",
        "message": "MongoDB Atlas connection failed. Check MONGODB_URI and IP whitelist.",
    }


def save_scenario(record: Dict[str, Any], user_id: str = "anonymous") -> Dict[str, Any]:
    """Save an impact scenario calculation to MongoDB or report unconfigured status."""
    db = get_db()
    if db is None:
        return {
            "saved": False,
            "status": "not_configured",
            "message": "MongoDB is not configured; this scenario was calculated but not saved.",
        }
    try:
        document = {
            **record,
            "user_id": user_id,
            "created_at": datetime.now(timezone.utc),
        }
        inserted = db["impact_scenarios"].insert_one(document)
        return {
            "saved": True,
            "status": "saved",
            "id": str(inserted.inserted_id),
        }
    except Exception as exc:
        return {
            "saved": False,
            "status": "error",
            "message": f"MongoDB save failed: {str(exc)}",
        }


def get_scenarios(user_id: str, role: str = "Urban Planner") -> List[Dict[str, Any]]:
    """Retrieve scenario history scoped to user permissions."""
    db = get_db()
    if db is None:
        return []
    try:
        query = {} if role == "Administrator" else {"user_id": user_id}
        cursor = db["impact_scenarios"].find(query).sort("created_at", -1).limit(50)
        results = []
        for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            if isinstance(doc.get("created_at"), datetime):
                doc["created_at"] = doc["created_at"].isoformat()
            results.append(doc)
        return results
    except Exception:
        return []


def log_report_generation(city: str, report_data: Dict[str, Any], user_id: str = "anonymous") -> Optional[str]:
    """Log generated PDF assessment report to MongoDB."""
    db = get_db()
    if db is None:
        return None
    try:
        doc = {
            "city": city,
            "overall_score": report_data.get("overall_score"),
            "data_coverage_pct": report_data.get("data_coverage_pct"),
            "user_id": user_id,
            "timestamp": datetime.now(timezone.utc),
        }
        res = db["reports"].insert_one(doc)
        return str(res.inserted_id)
    except Exception:
        return None
