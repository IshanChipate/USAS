# -*- coding: utf-8 -*-
"""
WSGI Entry Point for Production Deployment of USAS
Compatible with Gunicorn, Waitress, uWSGI, and cloud container environments.
"""

import os
from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    # In Windows or environments without gunicorn, waitress is used if available
    try:
        from waitress import serve
        print(f"Starting USAS Production Server with Waitress on http://{host}:{port}")
        serve(app, host=host, port=port)
    except ImportError:
        print(f"Starting USAS Server with Werkzeug on http://{host}:{port}")
        app.run(host=host, port=port)
