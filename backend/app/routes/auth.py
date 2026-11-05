# -*- coding: utf-8 -*-
"""
Authentication & Authorization Blueprint for USAS
Handles stakeholder login, registration with PENDING_VERIFICATION state,
session verification, forced password changes, and administrator-controlled
verification workflow (approve, reject, suspend, list).
"""

from functools import wraps
from flask import Blueprint, g, jsonify, request
from ..services.auth_service import auth_service

auth_bp = Blueprint("auth", __name__)


def _auth_error(message: str, status_code: int = 400, code: str = "auth_error"):
    return jsonify({"error": message, "code": code}), status_code


def require_auth(f):
    """Decorator to require a valid Bearer token for protected endpoints."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = ""
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
        elif "X-Auth-Token" in request.headers:
            token = request.headers.get("X-Auth-Token", "").strip()

        if not token:
            return _auth_error("Authentication required. Please provide a valid Bearer token.", 401, "unauthorized")

        profile = auth_service.get_user_by_token(token)
        if not profile:
            return _auth_error("Session expired or invalid authentication token. Please sign in again.", 401, "unauthorized")

        g.current_user = profile
        return f(*args, **kwargs)
    return decorated


def require_role(*allowed_roles):
    """Decorator to enforce role-based access control (e.g. Administrator)."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            token = ""
            if auth_header.startswith("Bearer "):
                token = auth_header[7:].strip()
            elif "X-Auth-Token" in request.headers:
                token = request.headers.get("X-Auth-Token", "").strip()

            if not token:
                return _auth_error("Authentication required.", 401, "unauthorized")

            profile = auth_service.get_user_by_token(token)
            if not profile:
                return _auth_error("Session expired or invalid token.", 401, "unauthorized")

            user_role = profile.get("role", "")
            is_allowed = any(r.lower() in user_role.lower() for r in allowed_roles) or "Admin" in user_role
            if not is_allowed:
                return _auth_error("Access forbidden: Insufficient privileges for this operation.", 403, "forbidden")

            g.current_user = profile
            return f(*args, **kwargs)
        return decorated
    return decorator


@auth_bp.post("/login")
def login():
    """Authenticate official stakeholder with email and password."""
    data = request.get_json(silent=True) or {}
    email = data.get("email", "")
    password = data.get("password", "")

    if not email or not password:
        return _auth_error("Email address and password are required.", 400, "missing_credentials")

    success, token, profile, error_code, error_msg = auth_service.authenticate(email, password)
    if not success:
        status_code = 401 if error_code == "invalid_credentials" else 403 if error_code in ("pending_verification", "account_rejected", "account_suspended") else 400
        return _auth_error(error_msg or "Invalid email or access credentials.", status_code, error_code or "auth_failed")

    return jsonify({
        "success": True,
        "token": token,
        "user": profile,
        "message": f"Welcome back, {profile['name']}.",
    }), 200


@auth_bp.post("/register")
def register():
    """
    Register a new prospective official account.
    Receives PENDING_VERIFICATION status; requires administrator verification before access.
    """
    data = request.get_json(silent=True) or {}
    name = data.get("name", "")
    email = data.get("email", "")
    password = data.get("password", "")
    designation = data.get("designation", "Urban Planner")
    department = data.get("department", "")
    employee_id = data.get("employee_id", "")
    verification_evidence = data.get("verification_evidence", "")

    if not name or not email or not password:
        return _auth_error("Full name, official email address, and password are required.", 400, "missing_fields")

    if not department or not employee_id:
        return _auth_error("Government department and official employee/identification reference are required.", 400, "missing_official_details")

    success, profile, error_msg = auth_service.register(
        name=name,
        email=email,
        password=password,
        designation=designation,
        department=department,
        employee_id=employee_id,
        verification_evidence=verification_evidence,
    )

    if not success:
        return _auth_error(error_msg or "Registration failed.", 400, "registration_failed")

    return jsonify({
        "success": True,
        "user": profile,
        "message": "Account submitted successfully. Your status is PENDING_VERIFICATION. An administrator will review your official credentials before access is granted.",
    }), 201


@auth_bp.post("/change-password")
@require_auth
def change_password():
    """Secure password change facility for authenticated users (mandatory on first login)."""
    data = request.get_json(silent=True) or {}
    current_password = data.get("current_password", "")
    new_password = data.get("new_password", "")

    if not current_password or not new_password:
        return _auth_error("Current password and new password are required.", 400, "missing_fields")

    user_id = g.current_user["id"]
    success, msg = auth_service.change_password(user_id, current_password, new_password)
    if not success:
        return _auth_error(msg or "Failed to change password.", 400, "password_change_failed")

    return jsonify({
        "success": True,
        "message": "Password successfully updated. First-login security requirement fulfilled.",
    }), 200


@auth_bp.get("/me")
@require_auth
def me():
    """Validate active session token and return user profile."""
    return jsonify({
        "success": True,
        "user": g.current_user,
    }), 200


@auth_bp.post("/logout")
def logout():
    """Invalidate client session."""
    return jsonify({
        "success": True,
        "message": "Session terminated successfully.",
    }), 200


@auth_bp.get("/users")
@require_role("Administrator")
def list_users():
    """Administrator-only: List all stakeholder accounts across verification statuses."""
    status_filter = request.args.get("status")
    users = auth_service.list_users(status_filter=status_filter)
    return jsonify({"success": True, "users": users}), 200


@auth_bp.get("/pending-users")
@require_role("Administrator")
def pending_users():
    """Administrator-only: List registrations awaiting official identity and departmental verification."""
    users = auth_service.list_users(status_filter="PENDING_VERIFICATION")
    return jsonify({"success": True, "pending_users": users}), 200


@auth_bp.post("/users/<user_id>/approve")
@require_role("Administrator")
def approve_user(user_id):
    """Administrator-only: Approve and activate a verified official account."""
    success, msg = auth_service.approve_user(user_id)
    if not success:
        return _auth_error(msg, 400, "approval_failed")
    return jsonify({"success": True, "message": msg}), 200


@auth_bp.post("/users/<user_id>/reject")
@require_role("Administrator")
def reject_user(user_id):
    """Administrator-only: Reject a registration with an official reason."""
    data = request.get_json(silent=True) or {}
    reason = data.get("reason", "Government affiliation or official reference could not be verified.")
    success, msg = auth_service.reject_user(user_id, reason=reason)
    if not success:
        return _auth_error(msg, 400, "rejection_failed")
    return jsonify({"success": True, "message": msg}), 200


@auth_bp.post("/users/<user_id>/suspend")
@require_role("Administrator")
def suspend_user(user_id):
    """Administrator-only: Suspend an existing stakeholder account."""
    success, msg = auth_service.suspend_user(user_id)
    if not success:
        return _auth_error(msg, 400, "suspension_failed")
    return jsonify({"success": True, "message": msg}), 200
