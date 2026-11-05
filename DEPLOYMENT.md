# Urban Sustainability Assessment System (USAS)
## Production Deployment & Operational Guide

This document details the configuration, build processes, and deployment strategies for running the **Urban Sustainability Assessment System (USAS)** in production environments.

---

### 1. Architecture Overview

USAS supports two deployment operational modes:

1. **Unified Single-Port Production Mode (Recommended)**:
   - The React frontend is compiled into static assets (`frontend/dist/`).
   - The Flask WSGI backend (`backend/wsgi.py`) serves both the REST API under `/api/*` and the client SPA from `frontend/dist/` for all non-API routes.
   - Requires only a single open port (`5000` or `$PORT`), eliminating CORS issues and simplifying cloud container deployment on Render, Railway, AWS, or Google Cloud Run.

2. **Decoupled Development Mode**:
   - Backend Flask API daemon on `http://127.0.0.1:5000`.
   - Vite React HMR dev server on `http://localhost:5173`.
   - Dynamic API routing configured via Vite proxy and `frontend/src/services/api.js`.

---

### 2. Authentication & Pre-Seeded Stakeholder Accounts

USAS features a production-grade authentication subsystem utilizing **PBKDF2-HMAC-SHA256** (100,000 iterations) password hashing and cryptographically signed session tokens.

The platform comes pre-seeded with three institutional accounts representing key municipal planning roles:

| Role | Institutional Name | Official Email | Access Password | Department / Jurisdiction |
| :--- | :--- | :--- | :--- | :--- |
| **Senior Urban Planner** | Shri Rajesh Deshmukh | `planner@urban.maharashtra.gov.in` | `MahaUrban@2026` | State Urban Development Department (UDD) |
| **Municipal Administrator** | Dr. Suhas Diwase, IAS | `commissioner@punecorp.gov.in` | `Admin@2026` | Pune Municipal Corporation (PMC) |
| **Environmental Auditor** | Pravin Patil | `auditor@mpcb.gov.in` | `Auditor@2026` | Maharashtra Pollution Control Board (MPCB) |

> **Evaluator Convenience**: The login interface features a **"One-Click Evaluator Roles"** selector allowing immediate access with any of the above personas without manually typing credentials. New institutional stakeholders can also register directly via the **"Register New Officer"** tab.

---

### 3. Containerized Deployment (Docker & Docker Compose)

The repository provides a multi-stage `Dockerfile` and `docker-compose.yml` for turnkey containerization.

#### Prerequisites
- Docker Engine 24.0+ and Docker Compose 2.20+

#### Quick Start with Docker Compose
```bash
# Build and start container in detached mode
docker compose up -d --build

# View container logs
docker compose logs -f

# Verify container health
docker ps --filter "name=usas_platform"
```
The platform is accessible at `http://localhost:5000`.

#### Standalone Docker Build & Run
```bash
# 1. Build Docker image
docker build -t usas-platform:latest .

# 2. Run container on port 5000
docker run -d \
  --name usas-app \
  -p 5000:5000 \
  -e PORT=5000 \
  -e AUTH_SECRET_KEY=usas-production-secret-token \
  -v usas_data:/app/data \
  usas-platform:latest
```

---

### 4. Cloud Platform Deployment

#### A. Render (Web Service)
1. Link your GitHub repository in the [Render Dashboard](https://dashboard.render.com).
2. Configure service settings:
   - **Environment**: `Docker`
   - **Dockerfile Path**: `Dockerfile`
   - **Plan**: Starter or Standard
3. Add Environment Variables:
   - `PORT`: `10000` (or leave default; Render automatically injects `PORT`)
   - `AUTH_SECRET_KEY`: `generate-a-secure-random-token`
4. Click **Deploy**. Render will run the multi-stage build and serve the application on your custom `*.onrender.com` domain.

#### B. Railway
1. Click **New Project** → **Deploy from GitHub repo**.
2. Railway detects the `Dockerfile` automatically.
3. In **Variables**, add `AUTH_SECRET_KEY`.
4. Generate a public domain under **Settings** → **Networking**.

#### C. Google Cloud Run
```bash
# 1. Build and push image to Google Artifact Registry
gcloud builds submit --tag gcr.io/<PROJECT_ID>/usas-platform:latest

# 2. Deploy to Cloud Run with automatic scaling
gcloud run deploy usas-platform \
  --image gcr.io/<PROJECT_ID>/usas-platform:latest \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --port 5000 \
  --memory 1Gi \
  --cpu 1
```

---

### 5. Production WSGI Deployment on Bare-Metal / VPS

#### A. Linux / Unix Server (with Gunicorn & Nginx)
```bash
# 1. Build frontend
cd frontend
npm ci && npm run build
cd ..

# 2. Setup Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# 3. Launch Gunicorn WSGI Server
gunicorn --bind 127.0.0.1:5000 \
  --workers 4 \
  --threads 2 \
  --timeout 120 \
  backend.wsgi:app
```

Sample Nginx Reverse Proxy block:
```nginx
server {
    listen 80;
    server_name usas.yourdomain.gov.in;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### B. Windows Server (with Waitress)
```powershell
# 1. Build frontend
Push-Location frontend; npm ci; npm run build; Pop-Location

# 2. Launch production Waitress server
& "backend\.venv\Scripts\python.exe" backend\wsgi.py
```
Waitress will bind to `http://0.0.0.0:5000` and handle production traffic with multi-threaded WSGI workers.

---

### 6. Environment Variables Reference

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `PORT` | `5000` | Port on which the WSGI web server listens |
| `HOST` | `0.0.0.0` | Bind IP host address |
| `FLASK_ENV` | `production` | Runtime mode (`production` disables debug banners) |
| `AUTH_SECRET_KEY` | `usas-maharashtra-...` | Secret salt used for HMAC-SHA256 session token signing |
| `GEMINI_API_KEY` | *(None)* | Optional Google Gemini API key for policy narrative generation |
| `MONGODB_URI` | *(None)* | Optional MongoDB connection string for planning scenario archival |
| `USAS_SPATIAL_DATA_DIR` | `data/geospatial` | Relative path to local municipal GIS shapefiles/geopackages |

---

### 7. Health & Verification Checklist

To verify deployment integrity, execute the following endpoint checks:

```bash
# 1. Platform Health Check
curl -s http://localhost:5000/api/health
# Expected: {"status": "healthy"}

# 2. Authentication Login Verification
curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"planner@urban.maharashtra.gov.in","password":"MahaUrban@2026"}'
# Expected: {"success": true, "token": "...", "user": {...}}

# 3. Assessment Retrieval (42 Maharashtra Cities)
curl -s http://localhost:5000/api/assessment/Pune | jq .overall_score
# Expected: 56.44 (or valid score)

# 4. Frontend Single-Port Serving
curl -I http://localhost:5000/
# Expected: HTTP/1.1 200 OK (Content-Type: text/html)
```
