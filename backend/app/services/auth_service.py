# -*- coding: utf-8 -*-
"""
Authentication & Stakeholder Management Service for USAS
Implements database-backed authentication, PBKDF2-HMAC-SHA256 password hashing,
initial administrator seeding (Ishan Chipate), forced first-login password change,
and administrator-controlled verification workflow (PENDING_VERIFICATION, ACTIVE, REJECTED, SUSPENDED).
"""

import hashlib
import hmac
import json
import os
import secrets
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"
USERS_FILE = DATA_DIR / "users.json"
SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "usas-maharashtra-urban-secret-key-2026-auth-token")
TOKEN_TTL_SECONDS = 86400  # 24 Hours

# Preconfigured Single Administrator Account
INITIAL_ADMIN_NAME = os.getenv("INITIAL_ADMIN_NAME", "Ishan Chipate")
INITIAL_ADMIN_EMAIL = os.getenv("INITIAL_ADMIN_EMAIL", "ishan.chipate@usas.gov.in").strip().lower()
INITIAL_ADMIN_PASSWORD = os.getenv("INITIAL_ADMIN_PASSWORD", "plan@123")


def hash_password(password: str, salt: Optional[str] = None) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 with 100,000 iterations and 32-byte salt."""
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000,
    )
    return f"{salt}${key.hex()}"


def verify_password(stored_hash: str, password: str) -> bool:
    """Verify password against stored salt$hash."""
    try:
        salt, key_hex = stored_hash.split("$")
        check_key = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100000,
        )
        return hmac.compare_digest(key_hex, check_key.hex())
    except Exception:
        return False


def generate_token(user_id: str, email: str, role: str) -> str:
    """Generate a signed, timestamped authentication token."""
    expiry = int(time.time()) + TOKEN_TTL_SECONDS
    payload = f"{user_id}:{email}:{role}:{expiry}"
    sig = hmac.new(
        SECRET_KEY.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"{payload.encode('utf-8').hex()}.{sig}"


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify signature and expiration of authentication token."""
    try:
        if not token or "." not in token:
            return None
        payload_hex, sig = token.split(".", 1)
        payload = bytes.fromhex(payload_hex).decode("utf-8")
        expected_sig = hmac.new(
            SECRET_KEY.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(sig, expected_sig):
            return None

        user_id, email, role, expiry_str = payload.split(":")
        if int(expiry_str) < time.time():
            return None  # Expired

        return {
            "id": user_id,
            "email": email,
            "role": role,
            "expires_at": int(expiry_str),
        }
    except Exception:
        return None


class AuthService:
    def __init__(self):
        self._ensure_storage()

    def _get_mongo_collection(self):
        """Retrieve MongoDB users collection if configured and accessible."""
        try:
            from .persistence import get_db
            db = get_db()
            if db is not None:
                return db["users"]
        except Exception:
            pass
        return None

    def _ensure_storage(self):
        """Seed the single predefined administrator account (Ishan Chipate) if not present."""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        users = self._read_users()

        # Check if Ishan Chipate admin exists
        admin_exists = any(u.get("email", "").lower() == INITIAL_ADMIN_EMAIL for u in users)

        if not admin_exists:
            admin_user = {
                "id": "usr-ishan-admin",
                "name": INITIAL_ADMIN_NAME,
                "email": INITIAL_ADMIN_EMAIL,
                "password_hash": hash_password(INITIAL_ADMIN_PASSWORD),
                "role": "Administrator",
                "designation": "Chief Urban Systems Administrator",
                "department": "Maharashtra State Urban Development Directorate",
                "employee_id": "MH-UDD-DIR-001",
                "verification_evidence": "Statutory System Architect & Administrator Order No. UDD/2026/01",
                "status": "ACTIVE",
                "must_change_password": True,
                "created_at": 1772400000,
                "updated_at": int(time.time()),
            }
            users.insert(0, admin_user)
            self._write_users(users)

    def _read_users(self) -> List[dict]:
        """Read users from MongoDB (if configured) or users.json."""
        mongo_col = self._get_mongo_collection()
        if mongo_col is not None:
            try:
                records = list(mongo_col.find({}))
                for r in records:
                    r["id"] = str(r.pop("_id", r.get("id")))
                if records:
                    return records
            except Exception:
                pass

        if not USERS_FILE.exists():
            return []
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _write_users(self, users: List[dict]):
        """Persist users to MongoDB and users.json."""
        # Always write to file as primary/fallback
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)

        mongo_col = self._get_mongo_collection()
        if mongo_col is not None:
            try:
                for u in users:
                    u_copy = dict(u)
                    user_id = u_copy.pop("id", None)
                    mongo_col.update_one(
                        {"email": u_copy["email"]},
                        {"$set": u_copy},
                        upsert=True
                    )
            except Exception:
                pass

    def authenticate(self, email: str, password: str) -> Tuple[bool, Optional[str], Optional[dict], Optional[str], Optional[str]]:
        """
        Authenticate user by email and password.
        Returns (success, token, user_profile, status_code, error_msg).
        """
        clean_email = (email or "").strip().lower()
        if not clean_email or not password:
            return False, None, None, "missing_credentials", "Email address and password are required."

        users = self._read_users()
        user = next((u for u in users if u.get("email", "").lower() == clean_email), None)

        if not user:
            return False, None, None, "invalid_credentials", "Invalid official email or access credentials."

        if not verify_password(user["password_hash"], password):
            return False, None, None, "invalid_credentials", "Invalid official email or access credentials."

        status = user.get("status", "ACTIVE")

        # Check account verification state
        if status == "PENDING_VERIFICATION":
            return False, None, None, "pending_verification", (
                "Account registration is pending official verification. An administrator must verify "
                "your government affiliation and employee reference before access is granted."
            )
        elif status == "REJECTED":
            reason = user.get("rejection_reason", "Official verification failed.")
            return False, None, None, "account_rejected", f"Account registration was rejected: {reason}"
        elif status == "SUSPENDED":
            return False, None, None, "account_suspended", "Account has been suspended by the administrator."

        token = generate_token(user["id"], user["email"], user["role"])
        profile = {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "designation": user.get("designation", "Urban Planner"),
            "department": user.get("department", "Municipal Administration"),
            "employee_id": user.get("employee_id", "—"),
            "status": status,
            "must_change_password": user.get("must_change_password", False),
        }
        return True, token, profile, None, None

    def register(
        self,
        name: str,
        email: str,
        password: str,
        designation: str = "Urban Planner",
        department: str = "Municipal Administration",
        employee_id: str = "",
        verification_evidence: str = "",
    ) -> Tuple[bool, Optional[dict], Optional[str]]:
        """
        Register a new prospective official account.
        Assigned status PENDING_VERIFICATION until approved by Ishan Chipate.
        """
        clean_email = (email or "").strip().lower()
        clean_name = (name or "").strip()
        clean_emp_id = (employee_id or "").strip()
        clean_dept = (department or "").strip()
        clean_desig = (designation or "").strip()

        if not clean_email or not clean_name or not password:
            return False, None, "Full name, official email address, and password are required."

        if not clean_dept or not clean_emp_id:
            return False, None, "Government department and official employee/identification reference are required."

        if len(password) < 6:
            return False, None, "Password must be at least 6 characters long."

        users = self._read_users()
        if any(u.get("email", "").lower() == clean_email for u in users):
            return False, None, "An account with this official email address already exists."

        new_user = {
            "id": f"usr-{secrets.token_hex(5)}",
            "name": clean_name,
            "email": clean_email,
            "password_hash": hash_password(password),
            "role": "Urban Planner",
            "designation": clean_desig or "Urban Planner",
            "department": clean_dept or "Municipal Administration",
            "employee_id": clean_emp_id,
            "verification_evidence": verification_evidence or "Official Departmental Registration Request",
            "status": "PENDING_VERIFICATION",
            "must_change_password": False,
            "created_at": int(time.time()),
            "updated_at": int(time.time()),
        }
        users.append(new_user)
        self._write_users(users)

        public_profile = {
            "id": new_user["id"],
            "name": new_user["name"],
            "email": new_user["email"],
            "designation": new_user["designation"],
            "department": new_user["department"],
            "status": new_user["status"],
            "message": "Account successfully submitted for administrative verification.",
        }
        return True, public_profile, None

    def change_password(self, user_id: str, current_password: str, new_password: str) -> Tuple[bool, Optional[str]]:
        """Change user password, verifying current password and clearing must_change_password."""
        if not new_password or len(new_password) < 6:
            return False, "New password must be at least 6 characters long."

        users = self._read_users()
        user = next((u for u in users if u["id"] == user_id), None)
        if not user:
            return False, "User not found."

        if not verify_password(user["password_hash"], current_password):
            return False, "Current password is incorrect."

        user["password_hash"] = hash_password(new_password)
        user["must_change_password"] = False
        user["updated_at"] = int(time.time())
        self._write_users(users)
        return True, "Password successfully updated."

    def get_user_by_token(self, token: str) -> Optional[dict]:
        """Validate token and return active user profile. Rejects unverified accounts."""
        token_info = verify_token(token)
        if not token_info:
            return None

        users = self._read_users()
        user = next((u for u in users if u["id"] == token_info["id"]), None)
        if not user:
            return None

        # Only ACTIVE accounts are authorized
        if user.get("status", "ACTIVE") != "ACTIVE":
            return None

        return {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "designation": user.get("designation", "Urban Planner"),
            "department": user.get("department", "Municipal Administration"),
            "employee_id": user.get("employee_id", "—"),
            "status": user.get("status", "ACTIVE"),
            "must_change_password": user.get("must_change_password", False),
        }

    def list_users(self, status_filter: Optional[str] = None) -> List[dict]:
        """List stakeholder accounts with official verification details (excluding password hashes)."""
        users = self._read_users()
        if status_filter:
            users = [u for u in users if u.get("status") == status_filter]
        return [
            {
                "id": u["id"],
                "name": u["name"],
                "email": u["email"],
                "role": u["role"],
                "designation": u.get("designation", "Urban Planner"),
                "department": u.get("department", "Municipal Corporation"),
                "employee_id": u.get("employee_id", "—"),
                "verification_evidence": u.get("verification_evidence", "—"),
                "status": u.get("status", "ACTIVE"),
                "rejection_reason": u.get("rejection_reason"),
                "must_change_password": u.get("must_change_password", False),
                "created_at": u.get("created_at"),
            }
            for u in users
        ]

    def approve_user(self, user_id: str) -> Tuple[bool, str]:
        """Administrator action: Approve a pending user account."""
        users = self._read_users()
        user = next((u for u in users if u["id"] == user_id), None)
        if not user:
            return False, "User not found."

        user["status"] = "ACTIVE"
        user["updated_at"] = int(time.time())
        self._write_users(users)
        return True, f"Account for {user['name']} has been verified and approved."

    def reject_user(self, user_id: str, reason: str = "") -> Tuple[bool, str]:
        """Administrator action: Reject a pending user account with a reason."""
        users = self._read_users()
        user = next((u for u in users if u["id"] == user_id), None)
        if not user:
            return False, "User not found."

        user["status"] = "REJECTED"
        user["rejection_reason"] = reason or "Government affiliation could not be verified."
        user["updated_at"] = int(time.time())
        self._write_users(users)
        return True, f"Account registration for {user['name']} has been rejected."

    def suspend_user(self, user_id: str) -> Tuple[bool, str]:
        """Administrator action: Suspend an existing user account."""
        users = self._read_users()
        user = next((u for u in users if u["id"] == user_id), None)
        if not user:
            return False, "User not found."

        if user["role"] == "Administrator":
            admin_count = sum(1 for u in users if u["role"] == "Administrator" and u.get("status") == "ACTIVE")
            if admin_count <= 1:
                return False, "Cannot suspend the primary Administrator account."

        user["status"] = "SUSPENDED"
        user["updated_at"] = int(time.time())
        self._write_users(users)
        return True, f"Account for {user['name']} has been suspended."


auth_service = AuthService()
