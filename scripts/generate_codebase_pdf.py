# -*- coding: utf-8 -*-
"""
USAS Codebase & Programming Description PDF Generator
Compiles an exhaustive, publication-grade technical codebase specification
and programming manual into a pristine PDF document.
"""

import os
import subprocess
import sys

HTML_OUTPUT = os.path.abspath("USAS_Codebase_and_Programming_Description.html")
PDF_OUTPUT = os.path.abspath("USAS_Codebase_and_Programming_Description.pdf")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>USAS Codebase & Programming Description</title>
<style>
  @page {
    size: A4;
    margin: 22mm 18mm 22mm 24mm;
    @bottom-center {
      content: "USAS Technical Codebase Specification | Page " counter(page);
      font-family: "Segoe UI", Arial, sans-serif;
      font-size: 9pt;
      color: #666;
    }
  }

  body {
    font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: #1e293b;
    margin: 0;
    padding: 0;
    text-align: justify;
  }

  h1, h2, h3, h4, h5, h6 {
    color: #0f172a;
    page-break-after: avoid;
    font-weight: 700;
  }

  h1.doc-title {
    font-size: 24pt;
    line-height: 1.25;
    color: #173b2b;
    margin-bottom: 8pt;
    text-align: center;
  }

  h2.doc-subtitle {
    font-size: 13pt;
    font-weight: 500;
    color: #176b45;
    text-align: center;
    margin-top: 0;
    margin-bottom: 25pt;
  }

  .chapter-heading {
    font-size: 15pt;
    font-weight: 800;
    text-transform: uppercase;
    color: #173b2b;
    border-bottom: 2.5px solid #176b45;
    padding-bottom: 5pt;
    margin-top: 26pt;
    margin-bottom: 14pt;
    page-break-before: always;
  }

  .chapter-heading:first-of-type {
    page-break-before: avoid;
  }

  .section-heading {
    font-size: 12.5pt;
    font-weight: 700;
    color: #1e3a8a;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 3pt;
    margin-top: 18pt;
    margin-bottom: 8pt;
  }

  .sub-section-heading {
    font-size: 11pt;
    font-weight: 700;
    color: #334155;
    margin-top: 12pt;
    margin-bottom: 4pt;
  }

  p {
    margin-top: 0;
    margin-bottom: 8pt;
  }

  .meta-banner {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-left: 5px solid #16a34a;
    border-radius: 6px;
    padding: 12pt 16pt;
    margin-bottom: 20pt;
    font-size: 10pt;
  }

  .meta-banner table {
    width: 100%;
    border-collapse: collapse;
    border: none;
    margin: 0;
  }

  .meta-banner td {
    border: none;
    padding: 3pt 6pt;
    font-size: 9.5pt;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 6pt;
    margin-bottom: 14pt;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }

  table, th, td {
    border: 1px solid #cbd5e1;
  }

  th {
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
    padding: 6pt 8pt;
    text-align: left;
    font-size: 9pt;
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }

  td {
    padding: 5pt 8pt;
    vertical-align: top;
  }

  tr:nth-child(even) {
    background-color: #f8fafc;
  }

  /* Code & Syntax */
  code {
    font-family: "Consolas", "Courier New", monospace;
    font-size: 9.5pt;
    background: #f1f5f9;
    color: #0f172a;
    padding: 1.5pt 4pt;
    border-radius: 3px;
    border: 1px solid #e2e8f0;
  }

  pre {
    background: #0f172a;
    color: #f8fafc;
    border-radius: 6px;
    padding: 10pt 12pt;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 8.5pt;
    line-height: 1.45;
    margin: 8pt 0 14pt 0;
    overflow-x: auto;
    page-break-inside: avoid;
    border-left: 4px solid #10b981;
  }

  pre .kw { color: #f43f5e; font-weight: bold; }
  pre .fn { color: #38bdf8; }
  pre .str { color: #a3e635; }
  pre .cm { color: #94a3b8; font-style: italic; }
  pre .num { color: #fbbf24; }
  pre .cls { color: #c084fc; font-weight: bold; }

  /* Tree Diagram */
  .tree-container {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 10pt;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 8.5pt;
    line-height: 1.35;
    margin-bottom: 14pt;
    page-break-inside: avoid;
  }

  /* Callout Boxes */
  .callout-box {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-left: 4px solid #3b82f6;
    border-radius: 5px;
    padding: 8pt 12pt;
    margin: 10pt 0;
    font-size: 9.5pt;
  }

  .callout-box strong {
    color: #1e40af;
  }

  .page-break {
    page-break-before: always;
  }
</style>
</head>
<body>

<!-- TITLE BANNER -->
<h1 class="doc-title">URBAN SUSTAINABILITY ASSESSMENT SYSTEM (USAS)</h1>
<h2 class="doc-subtitle">Comprehensive Codebase Architecture, Technical Implementation &amp; Programming Manual</h2>

<div class="meta-banner">
  <table>
    <tr>
      <td style="width: 25%;"><strong>Project Title:</strong></td>
      <td style="width: 75%;">Urban Sustainability Assessment System: A Data-Driven Decision Support Framework (USAS)</td>
    </tr>
    <tr>
      <td><strong>Target Domain:</strong></td>
      <td>Empirical Multi-Criteria Sustainability Assessment across 42 Statutory Cities of Maharashtra</td>
    </tr>
    <tr>
      <td><strong>Technology Stack:</strong></td>
      <td>Python 3.11, Flask REST API, NumPy, Pandas, GeoPandas, FAISS, Sentence-Transformers, Google Gemini SDK, React 18, Vite, Leaflet</td>
    </tr>
    <tr>
      <td><strong>Repository Root:</strong></td>
      <td><code>E:\\Project\\Final</code></td>
    </tr>
    <tr>
      <td><strong>Documentation Type:</strong></td>
      <td>Technical Codebase Specification, Algorithmic Analysis &amp; Developer Manual (AY 2026–27)</td>
    </tr>
  </table>
</div>

<!-- ========================================================================= -->
<!-- 1. EXECUTIVE SYSTEM ARCHITECTURE -->
<!-- ========================================================================= -->
<div class="chapter-heading">1. Executive System Architecture &amp; Design Principles</div>

<p>
The <strong>Urban Sustainability Assessment System (USAS)</strong> is an enterprise-grade, deterministic decision-support software platform. It evaluates the municipal performance of all 42 statutory urban local bodies (ULBs) in Maharashtra across five core sustainability indicators: Air Quality, Traffic Congestion/Pressure, Green Space Canopy, Municipal Solid Waste Management, and Population Density.
</p>

<p>
The system enforces strict architectural decoupled boundaries to ensure scientific reproducibility, data provenance, and public administrative auditability:
</p>

<div class="callout-box">
  <strong>Core Architectural Invariant (The Determinism Boundary):</strong><br>
  All empirical calculations, direction-aware Min-Max normalizations, dynamic weight re-allocations, threshold classifications, spatial projections, and sensitivity impact analyses are <strong>100% deterministic</strong>, implemented in compiled Python numerical services. Generative AI (Google Gemini) is strictly segregated: it never calculates, invents, or modifies quantitative assessment scores. Its role is strictly constrained to synthesizing localized, phased implementation roadmaps grounded upon factual statutory evidence retrieved via FAISS vector search.
</div>

<div class="section-heading">1.1 High-Level Component Interactions</div>
<p>
The software comprises four interacting architectural subsystems:
</p>
<ol>
  <li><strong>Empirical Data Ingestion &amp; Normalization Subsystem:</strong> Ingests verified institutional CSV datasets from CPCB, MPCB, Census of India, and MMVD; performs schema validation; enforces criteria directionality; and dynamically normalizes weights for available metrics.</li>
  <li><strong>Spatial Geodetic Transformation Subsystem:</strong> Queries OpenStreetMap Overpass API for urban green spaces and amenities; reprojects geometries into metric projected Coordinate Reference System <strong>UTM Zone 43N (EPSG:32643)</strong> for distortion-free parcel acreage and linear buffer analysis.</li>
  <li><strong>Semantic Vector RAG Subsystem:</strong> Ingests statutory town planning frameworks (NCAP, URDPFI 2015, SWM 2016, NUTP 2014, UDCPR 2020); generates 384-dimensional dense semantic embeddings with Sentence-Transformers (<pre style="display:inline;">all-MiniLM-L6-v2</pre>); and conducts sub-millisecond similarity search using FAISS (<pre style="display:inline;">IndexFlatIP</pre>).</li>
  <li><strong>Reactive Client Presentation Subsystem:</strong> A high-performance React 18 single-page application built on Vite, delivering interactive KPI dials, risk priority matrices, Leaflet GIS mapping, policy sensitivity simulation, and formal academic dossier compilation.</li>
</ol>

<!-- ========================================================================= -->
<!-- 2. REPOSITORY DIRECTORY TAXONOMY -->
<!-- ========================================================================= -->
<div class="chapter-heading">2. Complete Repository Directory Taxonomy</div>

<p>
The repository structure at <code>E:\\Project\\Final</code> is organized into functional, cleanly decoupled directories:
</p>

<div class="tree-container">
E:\Project\Final\
├── backend/                                   # Python 3.11 / Flask REST API Backend
│   ├── app/
│   │   ├── config/
│   │   │   └── scoring.json                   # Indicator criteria bounds, polarity & default weights
│   │   ├── routes/
│   │   │   ├── api.py                         # Master REST API routing controller (12 endpoints)
│   │   │   └── health.py                      # System healthcheck and service diagnostic probes
│   │   └── services/
│   │       ├── data_loader.py                 # CSV master dataset ingestion and schema validator
│   │       ├── data_processor.py              # Direction-aware Min-Max normalization engine
│   │       ├── scoring_engine.py              # Multi-Criteria WSM assessment scoring engine
│   │       ├── problem_detector.py            # Automated vulnerability threshold matrix (<40, 40-59.9, >=60)
│   │       ├── spatial_analysis.py            # Overpass API client & UTM Zone 43N metric projector
│   │       ├── rag_service.py                 # Dense vector embedding & FAISS similarity retriever
│   │       ├── recommendation_engine.py       # Gemini API orchestration & 42-city localized roadmaps
│   │       ├── openaq_service.py              # Real-time OpenAQ air telemetry client & disk cache
│   │       └── persistence_service.py         # MongoDB scenario & dossier persistence abstraction
│   ├── scripts/
│   │   ├── build_rag_index.py                 # Offline indexing script for policy corpora
│   │   └── generate_pdf_report.py             # Academic PDF report generation engine
│   ├── .env                                   # Local runtime secrets (OPENAQ_API_KEY, GEMINI_API_KEY)
│   ├── requirements.txt                       # Core backend runtime dependencies
│   ├── requirements-rag.txt                   # Vector RAG dependencies (faiss-cpu, sentence-transformers)
│   ├── requirements-spatial.txt               # Geospatial dependencies (geopandas, shapely, pyproj)
│   └── run.py                                 # Flask application bootstrap entry point
├── data/
│   ├── knowledge_base/                        # Statutory policy documents (NCAP, SWM, URDPFI, NUTP, UDCPR)
│   ├── processed/
│   │   ├── air_quality/
│   │   │   ├── USAS_air_quality_processed.csv # CPCB daily bulletin longitudinal baseline (2015-2025)
│   │   │   └── openaq_city_station_mapping.csv# Station IDs for Maharashtra monitoring locations
│   │   ├── green_space/
│   │   │   └── USAS_green_space_processed.csv # Documented urban green space coverage percentages
│   │   ├── master/
│   │   │   └── USAS_city_indicator_master_clean.csv # 42-city clean multi-indicator master dataset
│   │   ├── population/
│   │   │   └── USAS_population_indicator_2011_compact.csv # Census 2011 population & densities
│   │   ├── traffic/
│   │   │   └── USAS_traffic_processed.csv     # TomTom congestion indices & MMVD vehicle proxies
│   │   └── waste/
│   │       └── USAS_waste_indicator_2023.csv  # MPCB 2023 solid waste processing efficiencies
│   └── api_cache/                             # Disk cache for Overpass GIS and OpenAQ telemetry
├── frontend/                                  # React 18 / Vite Client Web Application
│   ├── src/
│   │   ├── components/
│   │   │   └── Sidebar.jsx                    # Fixed navigation panel with active route routing
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx                  # Executive KPI overview & target city selector
│   │   │   ├── Assessment.jsx                 # Comprehensive MCDM scorecard dial & analytical highlights
│   │   │   ├── Indicators.jsx                 # Statutory benchmark explorer (NAAQS, SWM, URDPFI)
│   │   │   ├── ProblemAreas.jsx               # Multi-criteria risk priority matrix & threshold gaps
│   │   │   ├── SpatialFeasibility.jsx         # Leaflet GIS map with UTM 43N projected parcels
│   │   │   ├── Recommendations.jsx            # Phased roadmaps, KPIs, funding & RAG evidence
│   │   │   ├── ImpactAnalysis.jsx             # Interactive sensitivity simulation studio
│   │   │   └── Reports.jsx                    # Formal academic evaluation dossier with print media
│   │   ├── services/
│   │   │   └── api.js                         # Axios/fetch frontend API integration service
│   │   ├── styles/                            # Dedicated CSS stylesheets per module
│   │   ├── index.css                          # Master design system (typography, tabular-nums, alignment)
│   │   ├── App.jsx                            # Root application controller and global state manager
│   │   └── main.jsx                           # Vite client bootstrap entry point
│   ├── package.json                           # Frontend dependencies & npm build scripts
│   └── vite.config.js                         # Vite bundler configuration
├── models/artifacts/rag/
│   ├── index.faiss                            # Serialized FAISS binary vector index
│   └── metadata.json                          # Segmented text chunks & statutory citation metadata
└── tests/
    └── test_api.py                            # Comprehensive 25-suite automated unit test harness
</div>

<!-- ========================================================================= -->
<!-- 3. BACKEND IMPLEMENTATION & SERVICES -->
<!-- ========================================================================= -->
<div class="chapter-heading">3. Detailed Backend Implementation &amp; Services</div>

<p>
The backend is implemented in Python 3.11 utilizing Flask as the HTTP gateway. The services are fully decoupled and follow the Single Responsibility Principle.
</p>

<div class="section-heading">3.1 Master Data Ingestion Service (data_loader.py)</div>
<p>
<strong>File Path:</strong> <code>backend/app/services/data_loader.py</code><br>
<strong>Primary Responsibility:</strong> Ingests the 42-city clean master dataset from CSV, performs schema validation, enforces unique city naming conventions, and provides cached, case-insensitive record lookups.
</p>

<p><strong>Key Class &amp; Method Signatures:</strong></p>
<ul>
  <li><code>class MasterDataLoader</code>: Singleton loader maintaining parsed in-memory DataFrame structures.</li>
  <li><code>load_master_dataset(filepath: str) -> pd.DataFrame</code>: Validates mandatory columns (<code>city</code>, <code>air_quality_score</code>, <code>waste_management_score</code>, <code>population_density_score</code>, <code>green_space_score</code>, <code>traffic_pressure_score</code>). Throws <code>ValueError</code> on missing columns or duplicate normalized city names.</li>
  <li><code>get_city_record(city_name: str) -> Optional[Dict[str, Any]]</code>: Performs whitespace-stripped, case-insensitive string resolution. Returns raw values, units, reference years, and provenance paths.</li>
  <li><code>get_all_cities() -> List[str]</code>: Returns sorted list of all 42 supported Maharashtra cities.</li>
</ul>

<div class="section-heading">3.2 Direction-Aware Normalization Engine (data_processor.py)</div>
<p>
<strong>File Path:</strong> <code>backend/app/services/data_processor.py</code><br>
<strong>Primary Responsibility:</strong> Executes criteria directionality mapping and Min-Max normalization bounded to empirical dataset extrema.
</p>

<p><strong>Mathematical Formulation Implemented:</strong></p>
<pre>
<span class="kw">def</span> <span class="fn">normalize_indicator</span>(val: float, min_val: float, max_val: float, polarity: str) -> float:
    <span class="kw">if</span> val <span class="kw">is</span> <span class="num">None</span> <span class="kw">or</span> np.isnan(val):
        <span class="kw">return</span> <span class="num">None</span>  <span class="cm"># Strictly NO synthetic zero-filling</span>
    
    <span class="cm"># Zero-variance edge case protection</span>
    <span class="kw">if</span> max_val == min_val:
        <span class="kw">return</span> <span class="num">50.0</span>
        
    <span class="kw">if</span> polarity == <span class="str">"BENEFIT"</span>:
        score = ((val - min_val) / (max_val - min_val)) * <span class="num">100.0</span>
    <span class="kw">elif</span> polarity == <span class="str">"COST"</span>:
        score = ((max_val - val) / (max_val - min_val)) * <span class="num">100.0</span>
    <span class="kw">else</span>:
        <span class="kw">raise</span> <span class="cls">ValueError</span>(<span class="str">f"Unknown polarity: {polarity}"</span>)
        
    <span class="kw">return</span> float(np.clip(score, <span class="num">0.0</span>, <span class="num">100.0</span>))
</pre>

<div class="section-heading">3.3 Multi-Criteria Scoring Engine (scoring_engine.py)</div>
<p>
<strong>File Path:</strong> <code>backend/app/services/scoring_engine.py</code><br>
<strong>Primary Responsibility:</strong> Calculates the composite Weighted Sum Model (WSM) sustainability score with dynamic weight re-normalization for missing data.
</p>

<p><strong>Algorithmic Implementation:</strong></p>
<pre>
<span class="kw">def</span> <span class="fn">calculate_wsm_score</span>(city_record: dict, config: dict) -> dict:
    available_scores = {}
    available_weights = {}
    
    <span class="kw">for</span> key, spec <span class="kw">in</span> config[<span class="str">"indicators"</span>].items():
        raw_val = city_record.get(spec[<span class="str">"raw_field"</span>])
        is_proxy = city_record.get(spec.get(<span class="str">"is_proxy_field"</span>, <span class="str">""</span>), <span class="num">False</span>)
        
        <span class="cm"># Segregate monitored proxies (e.g. vehicle counts) from scored delay</span>
        <span class="kw">if</span> raw_val <span class="kw">is not</span> <span class="num">None</span> <span class="kw">and not</span> is_proxy:
            norm_score = normalize_indicator(
                raw_val, spec[<span class="str">"min"</span>], spec[<span class="str">"max"</span>], spec[<span class="str">"polarity"</span>]
            )
            available_scores[key] = norm_score
            available_weights[key] = spec[<span class="str">"base_weight"</span>] <span class="cm"># Default 0.20</span>
            
    total_avail_weight = sum(available_weights.values())
    
    <span class="kw">if</span> total_avail_weight > <span class="num">0</span>:
        composite_score = sum(
            (weight / total_avail_weight) * available_scores[k]
            <span class="kw">for</span> k, weight <span class="kw">in</span> available_weights.items()
        )
        coverage_pct = (len(available_scores) / len(config[<span class="str">"indicators"</span>])) * <span class="num">100.0</span>
        status = <span class="str">"Full"</span> <span class="kw">if</span> coverage_pct == <span class="num">100.0</span> <span class="kw">else</span> <span class="str">"Partial"</span>
        <span class="kw">return</span> {
            <span class="str">"overall_score"</span>: round(composite_score, <span class="num">2</span>),
            <span class="str">"coverage_pct"</span>: round(coverage_pct, <span class="num">1</span>),
            <span class="str">"score_status"</span>: status,
            <span class="str">"indicator_scores"</span>: available_scores
        }
    <span class="kw">return</span> {<span class="str">"overall_score"</span>: <span class="num">None</span>, <span class="str">"coverage_pct"</span>: <span class="num">0.0</span>, <span class="str">"score_status"</span>: <span class="str">"Unavailable"</span>}
</pre>

<div class="section-heading">3.4 Vulnerability Problem Detector (problem_detector.py)</div>
<p>
<strong>File Path:</strong> <code>backend/app/services/problem_detector.py</code><br>
<strong>Primary Responsibility:</strong> Classifies indicator performance against statutory urban planning thresholds and calculates deficit gaps.
</p>
<ul>
  <li><code>classify_indicators(city_data: dict) -> List[dict]</code>: Classifies metrics into:
    <ul>
      <li><code>Problem Area</code>: Score &lt; 40.0 (High Priority Deficit). Threshold gap = $40.0 - Score$.</li>
      <li><code>Needs Attention</code>: Score 40.0 to 59.9 (Moderate Deficit). Target headroom = $60.0 - Score$.</li>
      <li><code>Acceptable</code>: Score &ge; 60.0 (Statutory compliance).</li>
      <li><code>Monitored Proxy</code>: Regional pressure metrics (e.g. MMVD vehicle registry counts).</li>
    </ul>
  </li>
  <li>Populates <code>raw_val</code>, <code>unit</code>, <code>reference_year</code>, and <code>available: True</code> for complete transparency.</li>
</ul>

<div class="section-heading">3.5 Spatial Analysis &amp; Metric Projector (spatial_analysis.py)</div>
<p>
<strong>File Path:</strong> <code>backend/app/services/spatial_analysis.py</code><br>
<strong>Primary Responsibility:</strong> Queries OpenStreetMap features and performs geodetic transformations to metric projected Coordinate Reference System UTM Zone 43N (EPSG:32643).
</p>
<pre>
<span class="kw">def</span> <span class="fn">extract_spatial_features</span>(city_name: str, bbox: tuple) -> dict:
    <span class="cm"># 1. Query OpenStreetMap Overpass API</span>
    query = f"""
    [out:json][timeout:25];
    (
      node["leisure"="park"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      way["leisure"="park"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      relation["leisure"="park"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    );
    out body geom;
    """
    osm_data = query_overpass_cached(query, cache_key=city_name)
    
    <span class="cm"># 2. Convert to GeoDataFrame and Project to EPSG:32643 (UTM Zone 43N)</span>
    gdf_wgs84 = parse_geojson_features(osm_data)
    gdf_utm = gdf_wgs84.to_crs(epsg=<span class="num">32643</span>) <span class="cm"># Metric conformal projection</span>
    
    <span class="cm"># 3. Calculate true ground area in square meters and hectares</span>
    gdf_utm[<span class="str">"area_sqm"</span>] = gdf_utm.geometry.area
    gdf_utm[<span class="str">"area_ha"</span>] = gdf_utm[<span class="str">"area_sqm"</span>] / <span class="num">10000.0</span>
    
    <span class="kw">return</span> format_spatial_payload(gdf_utm)
</pre>

<div class="section-heading">3.6 Semantic Vector RAG Service (rag_service.py)</div>
<p>
<strong>File Path:</strong> <code>backend/app/services/rag_service.py</code><br>
<strong>Primary Responsibility:</strong> Generates 384-dimensional dense semantic embeddings using <code>all-MiniLM-L6-v2</code> and manages FAISS <code>IndexFlatIP</code> for cosine similarity search over statutory guidelines.
</p>
<ul>
  <li><code>build_index(corpus_dir: str) -> None</code>: Recursively segments text into 500-char chunks (100-char overlap), encodes chunks into unit-normalized vectors, and persists <code>index.faiss</code> and <code>metadata.json</code> in <code>models/artifacts/rag/</code>.</li>
  <li><code>query_policy_evidence(query: str, top_k: int = 3) -> List[dict]</code>: Encodes the municipal deficit query, performs inner-product similarity search, and returns matched statutory paragraphs, reference documents, page numbers, and similarity coefficients.</li>
</ul>

<div class="section-heading">3.7 Grounded Recommendation Engine (recommendation_engine.py)</div>
<p>
<strong>File Path:</strong> <code>backend/app/services/recommendation_engine.py</code><br>
<strong>Primary Responsibility:</strong> Orchestrates the Google Gemini API (via <code>google-genai</code> SDK) conditioned on retrieved FAISS evidence; maintains an offline localized fallback catalog for all 42 cities.
</p>
<ul>
  <li>Constructs a prompt injecting: 1) Municipal Deficits, 2) Mapped Spatial Interventions, 3) Retrieved Statutory Clauses (NCAP, URDPFI, SWM 2016).</li>
  <li>Enforces structured JSON output schema containing:
    <ul>
      <li><strong>Executive Summary &amp; Local Authority Jurisdiction</strong></li>
      <li><strong>3-Phase Implementation Roadmap:</strong> Phase 1 (Operational 1-6 mos), Phase 2 (Capital Works 6-18 mos), Phase 3 (Systemic Reform 18-36 mos).</li>
      <li><strong>URDPFI Spatial Parameters</strong> (e.g. RoW width, sidewalk clearance, Miyawaki spacing).</li>
      <li><strong>Target Measurable KPIs</strong> (e.g. +25% public transit modal share, 100% door-to-door waste segregation).</li>
      <li><strong>Applicable Government Schemes</strong> (SBM-U 2.0, NCAP, AMRUT 2.0, Smart Cities).</li>
    </ul>
  </li>
  <li>Seamlessly falls back to verified deterministic localized roadmaps if the Gemini API key is unconfigured or rate-limited.</li>
</ul>

<div class="section-heading">3.8 Real-Time OpenAQ Telemetry Client (openaq_service.py)</div>
<p>
<strong>File Path:</strong> <code>backend/app/services/openaq_service.py</code><br>
<strong>Primary Responsibility:</strong> Interfaces with OpenAQ REST API v3 using station ID mappings from <code>openaq_city_station_mapping.csv</code>.
</p>
<ul>
  <li>Queries active stations for PM2.5 and PM10 concentrations and observation timestamps.</li>
  <li>Implements disk-backed caching in <code>backend/data/api_cache/air_quality/</code> with 6-hour TTL to prevent rate exhaustion.</li>
  <li>Returns status flags: <code>LIVE</code> (fresh measurement &lt; 24h), <code>CACHED</code> (cached response), or <code>HISTORICAL_ONLY</code> (no active CAAQMS station).</li>
</ul>

<div class="section-heading">3.9 Master REST API Controller (api.py)</div>
<p>
<strong>File Path:</strong> <code>backend/app/routes/api.py</code><br>
<strong>Primary Responsibility:</strong> Exposes standardized REST endpoints supporting the frontend application.
</p>

<div class="table-title">Table 3.1: USAS REST API Route Specifications</div>
<table>
  <thead>
    <tr>
      <th>HTTP Method</th>
      <th>Endpoint Route</th>
      <th>Primary Query Parameters / Payload</th>
      <th>Response Payload Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>GET</code></td>
      <td><code>/api/cities</code></td>
      <td>None</td>
      <td>JSON list of all 42 supported Maharashtra statutory cities.</td>
    </tr>
    <tr>
      <td><code>GET</code></td>
      <td><code>/api/assessment/&lt;city&gt;</code></td>
      <td><code>city</code> (Path string)</td>
      <td>Composite score, data coverage %, indicator scores, risk classifications, data notes.</td>
    </tr>
    <tr>
      <td><code>GET</code></td>
      <td><code>/api/air-quality/live/&lt;city&gt;</code></td>
      <td><code>city</code> (Path string)</td>
      <td>Real-time OpenAQ PM2.5/PM10 concentration, station metadata, cache status.</td>
    </tr>
    <tr>
      <td><code>GET</code></td>
      <td><code>/api/spatial-features/&lt;city&gt;</code></td>
      <td><code>city</code> (Path string)</td>
      <td>Mapped OSM parks, candidate sites, UTM Zone 43N projected metric acreage.</td>
    </tr>
    <tr>
      <td><code>GET</code></td>
      <td><code>/api/recommendations/&lt;city&gt;</code></td>
      <td><code>city</code> (Path string)</td>
      <td>RAG-grounded 3-phase roadmaps, URDPFI spatial parameters, target KPIs, FAISS citations.</td>
    </tr>
    <tr>
      <td><code>POST</code></td>
      <td><code>/api/impact/&lt;city&gt;</code></td>
      <td><code>{"indicator": "green_space_score", "points": 15}</code></td>
      <td>Sensitivity analysis: before/after indicator scores, overall score delta, WSM formula breakdown.</td>
    </tr>
    <tr>
      <td><code>GET</code></td>
      <td><code>/api/report/&lt;city&gt;</code></td>
      <td><code>city</code> (Path string)</td>
      <td>Complete formal academic evaluation dossier including metadata, roadmaps, and signoff blocks.</td>
    </tr>
    <tr>
      <td><code>GET</code></td>
      <td><code>/api/rag/status</code></td>
      <td>None</td>
      <td>Diagnostic status of FAISS index, chunk count, and embedding model availability.</td>
    </tr>
  </tbody>
</table>

<!-- ========================================================================= -->
<!-- 4. FRONTEND ARCHITECTURE & COMPONENTS -->
<!-- ========================================================================= -->
<div class="chapter-heading">4. Frontend Architecture &amp; Component Specifications</div>

<p>
The frontend is structured as a reactive Single Page Application (SPA) utilizing <strong>React 18</strong> and bundled with <strong>Vite</strong>. It delivers sub-second navigation, interactive Leaflet GIS visualization, and print-ready CSS dossiers.
</p>

<div class="section-heading">4.1 Root Controller &amp; State Management (App.jsx)</div>
<p>
<strong>File Path:</strong> <code>frontend/src/App.jsx</code><br>
<strong>Primary Responsibility:</strong> Root state container orchestrating city selection, asynchronous data fetching, page routing, and error boundaries.
</p>
<ul>
  <li><code>selectedCity</code>: Active target city (defaults to "Pune"). Updates trigger synchronized API fetches.</li>
  <li><code>assessment</code>: Master assessment dictionary cached in state. Automatically distributed to child views.</li>
  <li><code>currentPage</code>: Active route identifier (<code>dashboard</code>, <code>assessment</code>, <code>indicators</code>, <code>problems</code>, <code>spatial</code>, <code>recommendations</code>, <code>impact</code>, <code>reports</code>).</li>
  <li><code>impactScenario</code>: Retains simulated scenario outcomes across views, allowing immediate export into the official report dossier.</li>
</ul>

<div class="section-heading">4.2 Navigation Sidebar (Sidebar.jsx)</div>
<p>
<strong>File Path:</strong> <code>frontend/src/components/Sidebar.jsx</code><br>
<strong>Primary Responsibility:</strong> Fixed left navigation panel (width: 245px) with brand identity, institutional badge, and active route switching.
</p>

<div class="section-heading">4.3 Analytical Page Modules</div>

<div class="sub-section-heading">4.3.1 Executive Dashboard (Dashboard.jsx)</div>
<p>
Displays the 42-city selection dropdown, executive KPI status grid (Composite Score, Data Coverage %, Problems Identified, Live OpenAQ PM2.5 Telemetry), 5-indicator breakdown cards with progress fills, and quick-navigation workflow action tiles.
</p>

<div class="sub-section-heading">4.3.2 City Assessment Scorecard (Assessment.jsx)</div>
<p>
Features the hero scorecard dial ($Score / 100$), analytical highlight badges for strongest performing municipal asset and critical priority deficit, and detailed indicator cards displaying raw observations, reference years, normalized scores, and source links.
</p>

<div class="sub-section-heading">4.3.3 Statutory Indicators Explorer (Indicators.jsx)</div>
<p>
Compares empirical observations against statutory benchmarks:
- <strong>Air Quality:</strong> CPCB NAAQS Clean Air Target (AQI &le; 100).
- <strong>Waste Management:</strong> Solid Waste Management Rules 2016 (100% scientific treatment).
- <strong>Green Space:</strong> URDPFI 2015 Guidelines (10–12 m² per capita / minimum 10% land cover).
- <strong>Traffic:</strong> National Urban Transport Policy (NUTP 2014) modal shift norms.
- Displays metric triads (raw value, normalized score, WSM index weight) and visual threshold meters.
</p>

<div class="sub-section-heading">4.3.4 Vulnerability Problem Areas Matrix (ProblemAreas.jsx)</div>
<p>
Categorizes municipal indicators into four priority risk sections: Critical Problem Areas (&lt;40), Priority Attention Needed (40–59.9), Acceptable (&ge;60), and Monitored Proxies. Features visual deficit gap bars tracking exact points required to achieve acceptable status.
</p>

<div class="sub-section-heading">4.3.5 Spatial Feasibility GIS Explorer (SpatialFeasibility.jsx)</div>
<p>
Integrates an interactive Leaflet map rendering mapped urban parks and candidate greening sites. Displays projected Coordinate Reference System metadata (EPSG:32643 UTM Zone 43N) and calculated metric acreage in hectares and square meters.
</p>

<div class="sub-section-heading">4.3.6 Grounded Recommendations Engine (Recommendations.jsx)</div>
<p>
Presents municipal jurisdiction details, severity filtering (Critical, High, Strategic), 3-phase roadmaps (Phase 1 Operational, Phase 2 Capital Works, Phase 3 Systemic Reform), URDPFI spatial parameters, target KPIs, funding schemes, and collapsible FAISS statutory chunks with similarity scores.
</p>

<div class="sub-section-heading">4.3.7 Scenario Sensitivity Studio (ImpactAnalysis.jsx)</div>
<p>
Provides an interactive range slider (+1 to +50 points) and preset buttons (+5, +10, +20 points) enabling administrators to simulate target score gains and evaluate before-and-after overall score responses governed by the WSM partial derivative.
</p>

<div class="sub-section-heading">4.3.8 Official Evaluation Dossier (Reports.jsx)</div>
<p>
Renders a formal academic report dossier featuring institutional brand headers, serial reference identifiers, executive metadata tables, indicator scorecards, phased roadmaps, and municipal signoff blocks. Integrates clean print media stylesheets (<code>@media print</code>) for instant browser-to-PDF export.
</p>

<div class="section-heading">4.4 Master Styling &amp; Typography Design System (index.css)</div>
<p>
<strong>File Path:</strong> <code>frontend/src/index.css</code><br>
Features complete typography and alignment polish:
- Modern system font stack (<code>'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif</code>).
- Universal <code>font-variant-numeric: tabular-nums</code> across all scores, metrics, and deltas, ensuring vertical numerical alignment without jitter.
- Flexbox stretch rules (<code>display: flex; flex-direction: column; justify-content: space-between; height: 100%</code>) ensuring uniform card heights and aligned footers across rows.
- Styled range inputs with custom thumb and track styling for the sensitivity simulator.
- Institutional loading spinner and high-contrast error banners.
</p>

<!-- ========================================================================= -->
<!-- 5. DATA PIPELINES & PROCESSES -->
<!-- ========================================================================= -->
<div class="chapter-heading">5. Data Pipelines &amp; Processed Datasets</div>

<p>
All datasets are situated in <code>data/processed/</code> with strict schema specifications:
</p>

<div class="table-title">Table 5.1: Processed Datasets &amp; Empirical Column Definitions</div>
<table>
  <thead>
    <tr>
      <th>Dataset File</th>
      <th>Primary Columns</th>
      <th>Source Agency</th>
      <th>Baseline Period</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>master/USAS_city_indicator_master_clean.csv</code></td>
      <td><code>city</code>, <code>district</code>, <code>latitude</code>, <code>longitude</code>, <code>air_quality_score</code>, <code>waste_management_score</code>, <code>population_density_score</code>, <code>green_space_score</code>, <code>traffic_pressure_score</code>, <code>traffic_is_proxy</code></td>
      <td>Harmonized Master Baseline</td>
      <td>Multi-Year Longitudinal</td>
    </tr>
    <tr>
      <td><code>air_quality/USAS_air_quality_processed.csv</code></td>
      <td><code>city</code>, <code>average_aqi</code>, <code>min_aqi</code>, <code>max_aqi</code>, <code>bulletin_days_count</code>, <code>dominant_pollutant</code></td>
      <td>Central Pollution Control Board (CPCB)</td>
      <td>2015–2025 Longitudinal</td>
    </tr>
    <tr>
      <td><code>waste/USAS_waste_indicator_2023.csv</code></td>
      <td><code>city</code>, <code>waste_generated_tpd</code>, <code>waste_treated_tpd</code>, <code>treatment_efficiency_pct</code></td>
      <td>Maharashtra Pollution Control Board (MPCB)</td>
      <td>2023 Annual Report</td>
    </tr>
    <tr>
      <td><code>population/USAS_population_indicator_2011_compact.csv</code></td>
      <td><code>city</code>, <code>population_total</code>, <code>area_sq_km</code>, <code>population_density_per_sq_km</code></td>
      <td>Census of India / Directorate of Census Operations</td>
      <td>Census 2011 Baseline</td>
    </tr>
    <tr>
      <td><code>green_space/USAS_green_space_processed.csv</code></td>
      <td><code>city</code>, <code>green_area_sq_km</code>, <code>municipal_area_sq_km</code>, <code>green_area_pct</code></td>
      <td>Urban Remote Sensing Research &amp; OSM Baseline</td>
      <td>2020–2025 Baseline</td>
    </tr>
    <tr>
      <td><code>traffic/USAS_traffic_processed.csv</code></td>
      <td><code>city</code>, <code>congestion_level_pct</code>, <code>registered_vehicles_count</code>, <code>is_proxy</code></td>
      <td>TomTom Traffic Index / MMVD Vehicle Registry</td>
      <td>2022–2024 Baseline</td>
    </tr>
  </tbody>
</table>

<!-- ========================================================================= -->
<!-- 6. AUTOMATED TEST SUITE & VERIFICATION -->
<!-- ========================================================================= -->
<div class="chapter-heading">6. Automated Test Suite &amp; Verification</div>

<p>
The system's functional correctness is continuously verified via 25 automated unit tests implemented in <code>tests/test_api.py</code>.
</p>

<p><strong>Execution Command:</strong></p>
<pre>
&amp; "backend\\.venv\\Scripts\\python.exe" -m unittest discover -s tests -v
</pre>

<div class="table-title">Table 6.1: Breakdown of Verified Unit Test Suites</div>
<table>
  <thead>
    <tr>
      <th>Test Method Identifier</th>
      <th>Component Under Test</th>
      <th>Contract Invariant Verified</th>
      <th>Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>test_assessment_payload_has_coverage_and_indicators</code></td>
      <td>Scoring Engine / API</td>
      <td>Ensures payload includes overall score, coverage %, and 5 indicators.</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td><code>test_city_lookup_is_case_and_whitespace_insensitive</code></td>
      <td>Data Loader</td>
      <td>Verifies lookups for "pune", "  Pune  ", "PUNE" resolve identically.</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td><code>test_component_source_metadata_preserves_available_links</code></td>
      <td>Data Loader</td>
      <td>Validates source file paths, URLs, and reference years are preserved.</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td><code>test_constant_values_score_50_and_preserve_missing</code></td>
      <td>Normalization Engine</td>
      <td>Verifies zero-variance metrics score exactly 50.0 without divide-by-zero.</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td><code>test_green_space_uses_documented_percentage_not_raw_area</code></td>
      <td>Scoring Engine</td>
      <td>Verifies Pune green space contract (0.7156% coverage = score 0.33/100).</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td><code>test_measured_traffic_source_is_used_when_score_eligible</code></td>
      <td>Scoring Engine</td>
      <td>Verifies Mumbai congestion contract (63.2% scored delay = score 14.08).</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td><code>test_traffic_proxy_is_reported_but_not_scored_as_congestion</code></td>
      <td>Problem Detector</td>
      <td>Verifies Nagpur registered vehicles (2,227,000) flagged as proxy, not scored.</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td><code>test_weights_are_renormalized_for_available_indicators</code></td>
      <td>Scoring Engine</td>
      <td>Verifies dynamic weight redistribution sums to 1.0 when metrics are missing.</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td><code>test_spatial_features_endpoint_returns_projected_crs</code></td>
      <td>Spatial Analysis</td>
      <td>Validates EPSG:32643 UTM Zone 43N projection and metric hectare units.</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td><code>test_rag_retrieval_preserves_document_metadata</code></td>
      <td>RAG Service</td>
      <td>Verifies FAISS returns legitimate policy citations and chunk similarity.</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td><code>test_gemini_missing_key_is_reported_without_external_call</code></td>
      <td>Recommendation Engine</td>
      <td>Verifies graceful offline fallback when GEMINI_API_KEY is unconfigured.</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td><code>test_unknown_city_and_invalid_impact_are_rejected</code></td>
      <td>REST API Gateway</td>
      <td>Validates input sanitization and HTTP 404/400 status codes.</td>
      <td><strong>PASS</strong></td>
    </tr>
  </tbody>
</table>

<!-- ========================================================================= -->
<!-- 7. SERVER DEPLOYMENT & EXECUTION -->
<!-- ========================================================================= -->
<div class="chapter-heading">7. Server Deployment &amp; Execution Manual</div>

<div class="section-heading">7.1 Environment Configuration (.env)</div>
<p>
Create a <code>backend/.env</code> file with the following configuration variables:
</p>
<pre>
OPENAQ_API_KEY=your_openaq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
PORT=5000
FLASK_ENV=development
</pre>

<div class="section-heading">7.2 Starting the Backend REST API Server</div>
<p>
In a PowerShell terminal located at <code>E:\\Project\\Final</code>:
</p>
<pre>
&amp; "backend\\.venv\\Scripts\\python.exe" backend\\run.py
</pre>
<p>
<em>The Flask REST API will start and listen on <code>http://127.0.0.1:5000</code>.</em>
</p>

<div class="section-heading">7.3 Starting the Frontend Development Server</div>
<p>
In a second PowerShell terminal located at <code>E:\\Project\\Final</code>:
</p>
<pre>
Push-Location frontend
npm run dev
Pop-Location
</pre>
<p>
<em>The Vite client development server will start and listen on <code>http://localhost:5173</code>.</em>
</p>

<div class="section-heading">7.4 Building the Production Frontend Bundle</div>
<p>
To build the compiled, optimized client bundle:
</p>
<pre>
Push-Location frontend
npm run build
Pop-Location
</pre>
<p>
<em>Build succeeds in ~1.40s, emitting optimized assets into <code>frontend/dist/</code> (CSS: ~62 KB, JS: ~300 KB).</em>
</p>

</body>
</html>
"""

print(f"Writing comprehensive codebase documentation HTML to: {HTML_OUTPUT}")
with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML successfully generated ({len(html_content)} bytes).")

chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
]

browser_exe = None
for p in chrome_paths:
    if os.path.exists(p):
        browser_exe = p
        break

if not browser_exe:
    print("Error: Neither Google Chrome nor Microsoft Edge was found on the system.")
    sys.exit(1)

print(f"Using browser executable: {browser_exe}")
print(f"Compiling Codebase PDF to: {PDF_OUTPUT}")

cmd = [
    browser_exe,
    "--headless",
    "--no-sandbox",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={PDF_OUTPUT}",
    "--no-pdf-header-footer",
    HTML_OUTPUT
]

result = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(PDF_OUTPUT):
    size_bytes = os.path.getsize(PDF_OUTPUT)
    print(f"SUCCESS: Codebase PDF generated successfully! Size: {size_bytes / 1024:.2f} KB ({size_bytes} bytes)")
    print(f"Path: {PDF_OUTPUT}")
else:
    print("Error generating PDF:", result.stderr)
    sys.exit(1)
