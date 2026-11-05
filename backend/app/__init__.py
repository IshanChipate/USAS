# -*- coding: utf-8 -*-
"""
Application Factory for USAS (Urban Sustainability Assessment System)
Configures CORS, registers API and Auth blueprints, and serves compiled
production frontend assets when available.
"""

from pathlib import Path
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from .routes.health import health_bp
from .routes.api import api_bp
from .routes.auth import auth_bp

FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"


def create_app():
    app = Flask(__name__, static_folder=None)

    # Enable CORS for API routes in both development and production
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register API blueprints under /api
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        if isinstance(error, HTTPException):
            return jsonify({"error": error.description, "code": error.name.lower().replace(" ", "_")}), error.code
        app.logger.error("Unhandled API error", exc_info=(type(error), error, error.__traceback__))
        return jsonify({"error": "An unexpected server error occurred.", "code": "internal_error"}), 500

    # Production single-port deployment: serve compiled Vite SPA from frontend/dist
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        if path.startswith("api/"):
            return jsonify({"error": "Resource not found", "code": "not_found"}), 404

        if FRONTEND_DIST.exists():
            target = FRONTEND_DIST / path
            if path and target.is_file():
                return send_from_directory(FRONTEND_DIST, path)
            return send_from_directory(FRONTEND_DIST, "index.html")

        return jsonify({
            "status": "USAS State Urban Analytics Platform Online",
            "environment": "API Server Only (Frontend not built in frontend/dist)",
            "documentation": "/api/health",
            "api_endpoints": {
                "cities": "/api/cities",
                "assessment": "/api/assessment",
                "auth_login": "/api/auth/login",
                "auth_me": "/api/auth/me",
            },
        }), 200

    return app
