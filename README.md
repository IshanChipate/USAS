# USAS — Urban Sustainability Assessment System
## A Data-Driven Decision Support Framework for Maharashtra Cities

**USAS (Urban Sustainability Assessment System)** is a comprehensive, deterministic, and evidence-grounded urban planning decision support platform designed for 42 municipal urban centers in Maharashtra. 

The platform integrates a high-performance **React/Vite** frontend with a **Python Flask REST API**, **Pandas/NumPy deterministic Weighted Sum Model (WSM)** scoring engine, **Sentence Transformers + FAISS Retrieval-Augmented Generation (RAG)** policy recommendation pipeline with **Google Gemini**, **PBKDF2-HMAC-SHA256** authentication, **MongoDB Atlas** persistence, and **ReportLab** publication-quality PDF reporting.

---

### 1. Final Application Pipeline & Sections

USAS implements a strictly deterministic intelligence pipeline:
```
City Data Ingestion
       ↓
Empirical Data Processing (CPCB, MPCB, Census, TomTom)
       ↓
Five Sustainability Indicators
       ↓
Min-Max Normalization (0–100 Direction-Aware)
       ↓
Weighted Sum Model (WSM — MCDM)
       ↓
Overall Sustainability Score & Data Coverage
       ↓
Threshold-Based Problem Detection (<40 Problem Area, 40–59 Attention, ≥60 Acceptable)
       ↓
RAG Policy Evidence Retrieval (FAISS + Sentence Transformers)
       ↓
Google Gemini Contextual Synthesis (with 100% Offline Rule-Based Fallback)
       ↓
Actionable Recommendations with Phased Roadmaps
       ↓
Hypothetical Scenario-Based Impact Simulation
       ↓
High-Fidelity PDF & Statutory Assessment Reports
```

The application strictly contains **only functioning, presentable sections**:
1. **Login & Registration** — Secure authentication with institutional roles, validation, and evaluator quick-select.
2. **Dashboard** — Executive state overview, city selection, Recharts metrics, and workflow navigation.
3. **City Assessment** — Complete diagnostic scorecard, normalized 0–100 scores, coverage percentages, and metadata.
4. **Indicators** — Detailed breakdown of all 5 core pillars with statutory source provenance and reference years.
5. **Problem Areas** — Severity audit (<40 Problem Area, 40–59 Needs Attention) with explainable deficit diagnoses.
6. **Recommendations** — Grounded interventions synthesized over NCAP, URDPFI 2015, MPCB, and TOD regulations.
7. **Impact Analysis** — Interactive sensitivity calculator modeling target score gains and overall index recalculation.
8. **Reports** — Clean 9-section statutory assessment dossier with direct PDF export via ReportLab.

---

### 2. Technology Stack

- **Frontend:** React.js, Vite, Recharts, Fetch API, Vanilla CSS.
- **Backend:** Python 3.11+, Flask REST API, Pandas, NumPy, SciPy, Werkzeug.
- **Authentication & Security:** PBKDF2-HMAC-SHA256 (100,000 rounds), HMAC-SHA256 cryptographically signed tokens, Protected endpoints, Role-based access control (`Administrator`, `Urban Planner`).
- **AI & Evidence Retrieval (RAG):** Sentence Transformers (`all-MiniLM-L6-v2`), FAISS vector index, Google Gemini (`gemini-2.5-flash` via official `google-genai` SDK).
- **Reporting Engine:** ReportLab 5.x for publication-quality, 9-section statutory PDF generation.
- **Database:** MongoDB Atlas via PyMongo (with graceful in-memory/file fallback when unconfigured).
- **Deployment:** Multi-stage Docker, Docker Compose, Gunicorn (Linux/Cloud), Waitress (Windows).

---

### 3. Five Core Indicators & Data Provenance

1. **Air Quality:**
   - *Primary Measure:* Average AQI from Central Pollution Control Board (CPCB) daily bulletins (2021–2025).
   - *Supplementary Live Measure:* Real-time PM2.5 and PM10 concentrations (µg/m³) fetched via OpenAQ API v3.
   - *Direction:* Lower AQI is better; normalized so higher score reflects cleaner air.
2. **Traffic:**
   - *Primary Measure:* Measured congestion level (%) from TomTom Traffic Index for supported cities (e.g. Mumbai, Pune).
   - *Traffic-Pressure Proxy:* Registered motor vehicle counts (MMVD records). Strictly labeled as an unscored *pressure proxy* and never conflated with congestion.
3. **Green Space:**
   - *Primary Measure:* Documented green space coverage percentage (`green_area_pct = Mapped Green Area / City Area * 100`) from official Municipal Environmental Status Reports (ESR).
4. **Waste Management:**
   - *Primary Measure:* Waste Treatment Efficiency (`(Waste Treated / Waste Generated) * 100`) from Maharashtra Pollution Control Board (MPCB) Annual MSW Reports (2023).
5. **Population Density:**
   - *Primary Measure:* Census of India 2011 population divided by geographic area (persons per km²). Evaluated as an urban pressure indicator (lower density = lower infrastructure stress).

---

### 4. Authentication & Pre-Seeded Stakeholder Accounts

The platform includes pre-seeded institutional accounts for evaluator convenience:

| Role | Name | Official Email | Password | Department |
| :--- | :--- | :--- | :--- | :--- |
| **Senior Urban Planner** | Shri Rajesh Deshmukh | `planner@urban.maharashtra.gov.in` | `MahaUrban@2026` | State Urban Development Department (UDD) |
| **System Administrator** | USAS Administrator | `admin@usas.gov.in` | `Admin@USAS2026` | State Urban Analytics Directorate |
| **Municipal Administrator** | Dr. Suhas Diwase, IAS | `commissioner@punecorp.gov.in` | `Admin@2026` | Pune Municipal Corporation (PMC) |

> **Evaluator Quick-Access:** The login interface features **"One-Click Evaluator Roles"** allowing immediate login as any role without manually typing credentials.

---

### 5. Quickstart & Local Execution

#### Option A: Unified Single-Port Mode (Recommended)
```bash
# 1. Build React frontend into frontend/dist
cd frontend && npm install && npm run build && cd ..

# 2. Setup Python backend virtual environment
python -m venv backend/.venv
# On Windows:
backend\.venv\Scripts\activate
# On Linux/macOS:
source backend/.venv/bin/activate

# 3. Install backend dependencies
pip install -r backend/requirements.txt

# 4. Start production server (Waitress on Windows, Gunicorn on Linux)
python backend/wsgi.py
```
Open `http://localhost:5000` in your browser. Flask serves both the React SPA and API.

#### Option B: Dual Development Mode (with Hot Reloading)
```bash
# Terminal 1: Backend API
python backend/run.py

# Terminal 2: Vite Frontend Dev Server
cd frontend && npm run dev
```
Open `http://localhost:5173` in your browser.

---

### 6. Containerized Deployment (Docker)

```bash
# Build and run unified multi-stage container
docker compose up -d --build

# Verify container health
docker ps --filter "name=usas_platform"
```
The entire application runs at `http://localhost:5000`.

---

### 7. Automated Verification & Testing

USAS includes a comprehensive automated test suite verifying scoring contracts, indicator boundaries, RAG retrieval, password hashing, protected routes, and PDF generation:

```bash
# Run all 31 unit tests:
python -m unittest discover -s tests -v
```
**Test Results:**
```
Ran 31 tests in ~20s — OK (100% Pass Rate)
- test_unauthenticated_requests_are_rejected (401 Unauthorized enforced)
- test_role_based_access_control (Administrator vs Urban Planner privileges)
- test_pdf_report_generation_endpoint (Valid application/pdf binary export)
- test_auth_login_valid_and_invalid_credentials
- test_auth_me_and_session_token
- test_assessment_payload_has_coverage_and_indicators
- test_min_max_score_respects_direction_and_missing_values
- test_weights_are_renormalized_for_available_indicators
```
