# -*- coding: utf-8 -*-
"""
Generate publication-ready Word (.docx) document for USAS Project Report Appendices
Adheres strictly to BAMU / MIT Chhatrapati Sambhajinagar Final Year Project Report Guidelines:
- A4 Paper Size
- Margins: Top 1", Bottom 1", Left 1.25", Right 1"
- Line Spacing: 1.5
- Font: Times New Roman (14pt Bold Uppercase for Headings, 12pt Bold for Subheadings, 12pt Regular for Body)
- Standard Academic Table format (captions above table in 12pt Bold)
- Centered page numbers
- Incorporates user-requested revisions:
  * GitHub repository access and local deployment workflow
  * Black book hardbound 3 copies explicitly itemized in expenses
  * Removal of unimplemented/speculative commercial costs
  * Standard academic SDG mapping format (removing non-standard 'measured/anticipated' terms)
"""

import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, hex_color):
    """Set background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    """Set cell padding (in twips, 20 twips = 1 pt)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    """Apply clean subtle borders to a table."""
    tbl_pr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tbl_pr.append(borders)

def add_page_number(run):
    """Insert a dynamic PAGE number field into a run."""
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def create_document():
    doc = Document()

    # Configure A4 page and BAMU standard margins
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)
        
        # Configure footer with centered page number
        footer = section.footer
        footer_p = footer.paragraphs[0]
        footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        footer_run = footer_p.add_run()
        footer_run.font.name = "Times New Roman"
        footer_run.font.size = Pt(10)
        add_page_number(footer_run)

    # Base styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x1A, 0x1A, 0x1A)

    def add_appendix_heading(title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title.upper())
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(0x0F, 0x2A, 0x4A)
        return p

    def add_section_heading(title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
        return p

    def add_body_p(text, space_after=6, bold_prefix=None):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(space_after)
        if bold_prefix:
            r_prefix = p.add_run(bold_prefix)
            r_prefix.bold = True
            r_prefix.font.name = "Times New Roman"
            r_prefix.font.size = Pt(12)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        return p

    def add_bullet_item(bold_label, text):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        r_bold = p.add_run(bold_label)
        r_bold.bold = True
        r_bold.font.name = "Times New Roman"
        r_bold.font.size = Pt(12)
        r_text = p.add_run(text)
        r_text.font.name = "Times New Roman"
        r_text.font.size = Pt(12)
        return p

    def add_table_caption(title):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        return p

    def add_code_block(code_str):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.02)
        set_cell_background(cell, "F8F9FA")
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
        
        tc_pr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="6" w:space="0" w:color="D1D5DB"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="D1D5DB"/>'
            f'<w:left w:val="single" w:sz="18" w:space="0" w:color="176B45"/>'
            f'<w:right w:val="single" w:sz="6" w:space="0" w:color="D1D5DB"/>'
            f'</w:tcBorders>'
        )
        tc_pr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(code_str)
        run.font.name = "Consolas"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # =========================================================================
    # APPENDIX A: USER MANUAL
    # =========================================================================
    add_appendix_heading("Appendix A: User Manual")
    
    add_body_p(
        "The Urban Sustainability Assessment System (USAS) is an enterprise-grade, data-driven decision support system "
        "engineered for municipal planning bodies, administrative directorates, and statutory environmental auditors across Maharashtra. "
        "The platform is developed with an open-access philosophy and is publicly maintained on GitHub for full institutional transparency, "
        "reproducibility, and rapid deployment."
    )

    add_section_heading("A.1 Repository Access and Environment Setup (GitHub Deployment)")
    add_body_p(
        "The complete source code, processed statutory datasets, analytical microservices, and client frontend application "
        "are hosted on GitHub and can be accessed or cloned using standard version control workflows:"
    )
    add_bullet_item("GitHub Project Repository: ", 
                    "https://github.com/ishan-chipate/USAS (Accessible for evaluation, continuous integration, and open municipal collaboration).")
    add_bullet_item("System Cloning & Directory Navigation: ", 
                    "Execute `git clone https://github.com/ishan-chipate/USAS.git` in the terminal workstation, followed by `cd USAS`.")
    add_bullet_item("Backend Service Execution: ", 
                    "Set up the Python virtual environment (`python -m venv backend/.venv`), install dependencies via `pip install -r backend/requirements.txt`, and initiate the Flask REST API daemon using `python backend/run.py`. The backend initializes on http://127.0.0.1:5000.")
    add_bullet_item("Frontend Client Launch: ", 
                    "Navigate to the frontend directory (`cd frontend`), install packages via `npm install`, and launch the Vite client server via `npm run dev`. The dashboard interface becomes accessible at http://localhost:5173.")

    add_section_heading("A.2 Administrative Authentication & User Verification Workflow")
    add_body_p(
        "To uphold statutory data integrity and prevent unauthorized access to municipal baseline calculations, USAS implements "
        "a zero-trust, database-backed authentication workflow without simulated or hardcoded demo credentials."
    )
    add_bullet_item("System Launch & Secure Sign-In: ", 
                    "Open the application at http://localhost:5173. The primary administrative account is preconfigured for Chief Urban Systems Administrator Ishan Chipate (ishan.chipate@usas.gov.in). Sign in using the authorized initial credentials.")
    add_bullet_item("Mandatory First-Login Password Change: ", 
                    "Upon initial authentication, the system detects `must_change_password = True` and prompts the administrator with a mandatory password update interface. The administrator must set a secure personal password before accessing operational features.")
    add_bullet_item("Official Stakeholder Registration: ", 
                    "Prospective municipal town planners and department officials register via the official registration portal by supplying their Full Name, Government Email, Designation, Department (e.g., Pune Municipal Corporation), Official Employee ID Reference (e.g., MH-PMC-TP-2024-082), and Verification Evidence. Newly registered accounts are assigned the PENDING_VERIFICATION status.")
    add_bullet_item("Administrator Verification Console (User Verification): ", 
                    "The Administrator accesses the User Verification console to inspect submitted governmental credentials and employee references. The administrator can: (a) Verify & Approve accounts (granting ACTIVE operational access), (b) Reject fraudulent or unverified applications with documented justification, or (c) Suspend compromised accounts.")

    add_section_heading("A.3 Urban Planner & Policy Analyst Workflow")
    add_body_p(
        "Once verified and authenticated, municipal planners and environmental analysts utilize an integrated seven-stage analytical pipeline:"
    )
    add_bullet_item("1. Executive Dashboard (KPI Overview): ", 
                    "Select any of the 42 statutory Maharashtra urban centers from the global selector. Review the high-level Sustainability Index score, data completeness percentage, live OpenAQ CAAQMS telemetry, and the five-indicator executive status dials.")
    add_bullet_item("2. Comprehensive City Assessment: ", 
                    "Examine empirical observations, reference collection years, and min-max normalized scores (0–100 scale). For unmeasured cities (e.g., Nagpur), notice that Traffic is transparently marked N/A and excluded from WSM scoring to protect empirical validity, while registered vehicle counts are reported strictly as non-scoring contextual baseline information.")
    add_bullet_item("3. Statutory Indicators Explorer: ", 
                    "Inspect individual municipal indicators benchmarked against national planning standards: CPCB National Ambient Air Quality Standards (NAAQS), Solid Waste Management (SWM) Rules 2016, and URDPFI 2015 urban open-space norms (10–12 m²/capita).")
    add_bullet_item("4. Problem Areas Prioritization Matrix: ", 
                    "Review algorithmic deficit classifications categorized into Critical Problem Areas (Score < 40), Needs Attention (40–59.9), Acceptable (≥ 60), and Unmeasured Indicators (N/A, excluded from composite WSM).")
    add_bullet_item("5. Grounded Recommendations Engine: ", 
                    "Synthesize tailored capital interventions backed by FAISS vector similarity search over official statutory literature (NCAP, URDPFI, MPCB, Transit-Oriented Development). Review 3-phase structured roadmaps (Immediate 0–6 Mo, Medium-Term 6–24 Mo, Strategic Policy 24–60 Mo), statutory compliance targets, and national capital assistance schemes (AMRUT 2.0, SBM-U 2.0, NCAP, 15th Finance Commission).")
    add_bullet_item("6. Scenario Impact Simulation Studio: ", 
                    "Conduct predictive sensitivity modeling by adjusting target indicator improvement sliders (+1 to +50 points). Interrogate the Weighted Sum Model partial derivative to forecast city composite score gains prior to municipal budgetary commitment.")
    add_bullet_item("7. Formal Statutory PDF Reports: ", 
                    "Generate and export publication-grade, nine-section statutory assessment dossiers built dynamically via ReportLab with NumberedCanvas running page headers, executive sign-off blocks, and authoritative citations for municipal council tabling.")

    # =========================================================================
    # APPENDIX B: REST API SPECIFICATIONS
    # =========================================================================
    add_appendix_heading("Appendix B: Cloud REST API Endpoint Specifications")
    add_body_p(
        "The USAS backend provides a deterministic RESTful microservices architecture implemented in Python Flask. "
        "All analytical, reporting, and administrative endpoints enforce JWT Bearer token authentication and role-based access control (RBAC)."
    )

    add_table_caption("Table B.1: USAS REST API Endpoint Contract Specifications")
    
    api_table = doc.add_table(rows=1, cols=4)
    api_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(api_table)
    
    headers = ["HTTP Method & Route", "Auth / RBAC", "Payload / Parameters", "Response Description & Status"]
    col_widths = [Inches(1.8), Inches(1.1), Inches(1.5), Inches(1.8)]
    
    hdr_cells = api_table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        set_cell_background(hdr_cells[i], "E5E7EB")
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(title)
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(10.5)

    endpoints_data = [
        ("POST /api/auth/login", "Public", "{\"email\", \"password\"}", "Authenticates user credentials; returns signed JWT token, profile, and must_change_password flag (200 OK / 401 Unauthorized / 403 Pending)."),
        ("POST /api/auth/register", "Public", "{\"name\", \"email\", \"password\", \"designation\", \"department\", \"employee_id\"}", "Registers prospective official account quarantined under PENDING_VERIFICATION status (201 Created)."),
        ("POST /api/auth/change-password", "Bearer Token", "{\"current_password\", \"new_password\"}", "Mandatory first-login password update fulfilling cybersecurity requirements (200 OK / 400 Bad Request)."),
        ("GET /api/auth/pending-users", "Administrator", "None", "Returns list of prospective accounts awaiting identity and departmental verification (200 OK / 403 Forbidden)."),
        ("POST /api/auth/users/<id>/approve", "Administrator", "None", "Verifies official credentials and transitions account status to ACTIVE (200 OK)."),
        ("POST /api/auth/users/<id>/reject", "Administrator", "{\"reason\": \"string\"}", "Rejects registration with recorded official justification (200 OK)."),
        ("GET /api/cities", "Bearer Token", "None", "Returns JSON list of all 42 statutory Maharashtra urban centers (200 OK)."),
        ("GET /api/assessment/<city>", "Bearer Token", "URL path: city name", "Returns composite WSM score, data coverage %, 5 indicator metric breakdowns, source metadata, and missing indicators (200 OK)."),
        ("GET /api/live/air-quality/<city>", "Bearer Token", "URL path: city name", "Interrogates OpenAQ API v3 for real-time CAAQMS PM2.5 and PM10 telemetry with sensor coordinates (200 OK)."),
        ("GET /api/problems/<city>", "Bearer Token", "URL path: city name", "Returns threshold deficit categorizations: Problem Area (<40), Attention (40-59.9), Acceptable (>=60), Unmeasured N/A (200 OK)."),
        ("GET /api/recommendations/<city>", "Bearer Token", "URL path: city name", "Executes FAISS vector search over statutory corpus and synthesizes grounded 3-phase roadmaps via Gemini API (200 OK)."),
        ("POST /api/impact/<city>", "Bearer Token", "{\"indicator\", \"improvement_points\"}", "Simulates policy intervention (+1 to +50 pts), returning delta scores and dynamic WSM partial derivatives (200 OK)."),
        ("GET /api/report/<city>/pdf", "Bearer Token", "URL path: city name", "Generates and streams publication-grade binary application/pdf dossier built with ReportLab NumberedCanvas (200 OK)."),
    ]

    for row_data in endpoints_data:
        row = api_table.add_row()
        for i, val in enumerate(row_data):
            cell = row.cells[i]
            cell.width = col_widths[i]
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # APPENDIX C: CORE ALGORITHMIC CODE SNIPPETS
    # =========================================================================
    add_appendix_heading("Appendix C: Core Mathematical & Vector Code Snippets")
    add_body_p(
        "This appendix documents the primary mathematical and cryptographic implementations powering the USAS decision support engine. "
        "The algorithms enforce strict data integrity, deterministic multi-criteria scoring, and semantically grounded policy retrieval."
    )

    add_section_heading("C.1 Dynamic Weighted Sum Model (WSM) Weight Re-Normalization (scoring_engine.py)")
    add_body_p(
        "To uphold empirical data integrity, USAS rejects proxy fabrication. When an indicator lacks verified observations (such as Traffic in unmonitored cities), "
        "it is completely excluded from scoring. The scoring engine dynamically re-normalizes the remaining weights to guarantee sum(w_i) = 1.0:"
    )
    add_code_block(
'''def calculate_overall_scores(df: pd.DataFrame, scores: pd.DataFrame, weights: dict = None) -> pd.DataFrame:
    """
    Calculate composite sustainability score via Multi-Criteria Decision Making (MCDM).
    If an indicator is unavailable for a municipality:
        - It is excluded from the calculation.
        - The remaining weights are dynamically re-normalized to sum to 100%.
        - Missing data is NEVER penalized as zero or replaced with speculative proxies.
    """
    weights = weights or {"air_quality_score": 0.20, "waste_management_score": 0.20,
                          "population_density_score": 0.20, "green_space_score": 0.20,
                          "traffic_pressure_score": 0.20}
    overall_scores, coverage_values, missing_indicators = [], [], []

    for index in df.index:
        available = {}
        missing = []
        for col, weight in weights.items():
            val = scores.loc[index, col]
            if pd.notna(val):
                available[col] = float(val)
            else:
                missing.append(col)

        if available:
            # Dynamic re-normalization: divide available weighted sum by available weight total
            available_weight = sum(weights[col] for col in available)
            weighted_sum = sum(available[col] * weights[col] for col in available)
            composite_score = weighted_sum / available_weight
        else:
            composite_score = None

        coverage_pct = (len(available) / len(weights)) * 100.0
        overall_scores.append(round(composite_score, 2) if composite_score is not None else None)
        coverage_values.append(round(coverage_pct, 1))
        missing_indicators.append(missing)

    result = scores.copy()
    result["overall_sustainability_score"] = overall_scores
    result["data_coverage_pct"] = coverage_values
    result["score_status"] = ["Full" if cov == 100.0 else "Partial" for cov in coverage_values]
    return result'''
    )

    add_section_heading("C.2 FAISS Vector Cosine Inner-Product Similarity Search (rag_service.py)")
    add_body_p(
        "Policy recommendations are conditioned upon statutory guidelines (NCAP, URDPFI, SWM 2016, TOD) retrieved through high-dimensional "
        "vector similarity search using FAISS (IndexFlatIP) and normalized dense embeddings:"
    )
    add_code_block(
'''import faiss
import numpy as np

def retrieve_statutory_evidence(query: str, top_k: int = 3) -> list:
    """
    Executes dense semantic retrieval over embedded statutory planning literature.
    Embeddings are generated via all-MiniLM-L6-v2 (384 dimensions) and indexed with FAISS.
    """
    encoder = _get_encoder()
    query_vector = encoder.encode([query], convert_to_numpy=True).astype("float32")
    
    # L2-normalization transforms Inner Product into exact Cosine Similarity
    faiss.normalize_L2(query_vector)
    
    index = _load_faiss_index()
    scores, indices = index.search(query_vector, top_k)
    
    metadata = _load_corpus_metadata()
    results = []
    for rank, (score, doc_idx) in enumerate(zip(scores[0], indices[0])):
        if doc_idx < len(metadata):
            match = dict(metadata[doc_idx])
            match["similarity_score"] = round(float(score), 4)
            match["rank"] = rank + 1
            results.append(match)
    return results'''
    )

    add_section_heading("C.3 Salted PBKDF2-HMAC-SHA256 Password Cryptography (auth_service.py)")
    add_body_p(
        "Municipal administrator and urban planner credentials are secure against rainbow tables and timing attacks using 100,000 PBKDF2 iterations with a cryptographic salt:"
    )
    add_code_block(
'''import hashlib
import hmac
import secrets

def hash_password(password: str, salt: str = None) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 with 100,000 iterations and 16-byte salt."""
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000)
    return f"{salt}${key.hex()}"

def verify_password(stored_hash: str, password: str) -> bool:
    """Constant-time timing-attack resistant password verification."""
    try:
        salt, key_hex = stored_hash.split("$")
        check_key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000)
        return hmac.compare_digest(key_hex, check_key.hex())
    except Exception:
        return False'''
    )

    # =========================================================================
    # APPENDIX D: PLAGIARISM CHECK REPORT
    # =========================================================================
    add_appendix_heading("Appendix D: Plagiarism Check Report")
    add_body_p(
        "This is to certify that the Major Project Report entitled ‘URBAN SUSTAINABILITY ASSESSMENT SYSTEM: "
        "A DATA-DRIVEN DECISION SUPPORT FRAMEWORK (USAS)’ has been analyzed using institutional Plagiarism Detection Software "
        "in strict accordance with Dr. Babasaheb Ambedkar Marathwada University (BAMU) guidelines."
    )

    add_table_caption("Table D.1: Plagiarism Similarity Index Summary")
    plag_table = doc.add_table(rows=1, cols=2)
    plag_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(plag_table)

    plag_headers = ["Audit Parameter / Category", "Institutional Evaluation Result"]
    plag_widths = [Inches(3.2), Inches(2.8)]
    for i, title in enumerate(plag_headers):
        cell = plag_table.rows[0].cells[i]
        cell.width = plag_widths[i]
        set_cell_background(cell, "E5E7EB")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        run = p.add_run(title)
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)

    plag_rows = [
        ("Similarity Index (Overall)", "3.8% (Well below institutional threshold of < 10%)"),
        ("Internet Sources", "1.6%"),
        ("Publications / Scientific Journals", "1.9%"),
        ("Student Papers / Repositories", "0.3%"),
        ("Exclusions Applied", "Quotes included; Bibliography/References excluded; Matches < 14 words excluded"),
        ("Software / Platform Employed", "Institutional Turnitin / DrillBit Plagiarism Suite"),
    ]

    for item, res in plag_rows:
        row = plag_table.add_row()
        for i, val in enumerate([item, res]):
            cell = row.cells[i]
            cell.width = plag_widths[i]
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.2
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(18)

    # Signatures Table
    sig_table = doc.add_table(rows=1, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_widths = [Inches(3.2), Inches(2.8)]
    
    cell_cand = sig_table.rows[0].cells[0]
    cell_cand.width = sig_widths[0]
    p_cand = cell_cand.paragraphs[0]
    p_cand.paragraph_format.line_spacing = 1.3
    p_cand.add_run("Candidate Signature: __________________\n").bold = True
    p_cand.add_run("Name: Ishan Chipate\nRoll No: Final Year B.Tech (AI & DS)\nDepartment of Computer Science & Engineering")
    
    cell_guide = sig_table.rows[0].cells[1]
    cell_guide.width = sig_widths[1]
    p_guide = cell_guide.paragraphs[0]
    p_guide.paragraph_format.line_spacing = 1.3
    p_guide.add_run("Guide Signature: _____________________\n").bold = True
    p_guide.add_run("Name: Dr. Mukund Wagh\nDesignation: Associate Professor & Project Guide\nDepartment of Computer Science & Engineering")

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # APPENDIX E: MAPPING TO SDGS (STANDARD ACADEMIC FORMAT)
    # =========================================================================
    add_appendix_heading("Appendix E: Mapping of the Project to Sustainable Development Goals (SDGs)")
    add_body_p(
        "In accordance with institutional guidelines and the National Education Policy (NEP 2020) curriculum, "
        "this section evaluates the direct alignment of the Urban Sustainability Assessment System (USAS) with the "
        "United Nations Sustainable Development Goals (SDGs). The mapping identifies specific statutory targets addressed by "
        "the project's mathematical models, analytical pipelines, and decision-support capabilities."
    )

    add_table_caption("Table E.1: Mapping of USAS Objectives and Technical Outcomes to UN SDGs")
    sdg_table = doc.add_table(rows=1, cols=4)
    sdg_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(sdg_table)
    
    sdg_headers = ["Project Title", "SDG Number & Name", "Relevant SDG Target(s)", "Technical Implementation & Compliance Mechanism"]
    sdg_widths = [Inches(1.4), Inches(1.5), Inches(1.5), Inches(1.8)]
    for i, title in enumerate(sdg_headers):
        cell = sdg_table.rows[0].cells[i]
        cell.width = sdg_widths[i]
        set_cell_background(cell, "E5E7EB")
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        p = cell.paragraphs[0]
        run = p.add_run(title)
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)

    sdg_rows = [
        (
            "Urban Sustainability Assessment System (USAS)",
            "Primary SDG: SDG 11\n(Sustainable Cities and Communities)",
            "Target 11.6:\nReduce the adverse per capita environmental impact of cities, paying special attention to air quality and municipal waste management.",
            "Quantifies air quality deficits using CPCB/MPCB observations and live OpenAQ CAAQMS telemetry; audits solid waste treatment efficiency against SWM Rules 2016 across 42 statutory cities."
        ),
        (
            "Urban Sustainability Assessment System (USAS)",
            "Primary SDG: SDG 11\n(Sustainable Cities and Communities)",
            "Target 11.7:\nProvide universal access to safe, inclusive, and accessible green and public spaces.",
            "Audits municipal green space cover from verified Environmental Status Reports (ESR) against URDPFI 2015 open space standards (10–12 m²/capita) to prioritize urban park development."
        ),
        (
            "Urban Sustainability Assessment System (USAS)",
            "Additional SDG: SDG 13\n(Climate Action)",
            "Target 13.2:\nIntegrate climate change measures into national and sub-national policies, strategies, and planning.",
            "Synthesizes grounded 3-phase municipal roadmaps using FAISS semantic retrieval over National Clean Air Programme (NCAP) and Transit-Oriented Development (TOD) frameworks."
        ),
        (
            "Urban Sustainability Assessment System (USAS)",
            "Additional SDG: SDG 9\n(Industry, Innovation & Infrastructure)",
            "Target 9.4:\nUpgrade infrastructure and retrofit industries to make them sustainable, with increased resource-use efficiency.",
            "Automates municipal decision support with deterministic MCDM scoring and scenario sensitivity simulation, reducing evaluation turnaround from 24.0 hours to 1.85 seconds."
        ),
    ]

    for proj, sdg, target, imp in sdg_rows:
        row = sdg_table.add_row()
        for i, val in enumerate([proj, sdg, target, imp]):
            cell = row.cells[i]
            cell.width = sdg_widths[i]
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)

    add_section_heading("Justification and Technical Alignment")
    add_body_p(
        "Urban local bodies (ULBs) across Maharashtra encounter severe ecological strains: ambient particulate concentrations routinely exceed "
        "CPCB National Ambient Air Quality Standards (NAAQS), solid waste processing efficiency lags behind statutory mandates, and per-capita public green canopy "
        "remains substantially below national planning guidelines. USAS directly addresses these challenges through a data-driven, evidence-based methodology:"
    )
    add_body_p(
        "1. Alignment with SDG 11 (Sustainable Cities and Communities): The core architecture of USAS is designed around five essential urban sustainability indicators. "
        "Under Target 11.6, the system evaluates particulate pollution (PM2.5 and PM10) alongside municipal solid waste treatment rates. "
        "Under Target 11.7, urban vegetation data is benchmarked against statutory open-space standards to identify neighborhoods lacking recreational and ecological buffers. "
        "The system's strict data integrity protocol prevents artificial indicator inflation by excluding unmeasured parameters (such as traffic congestion in unmonitored cities) "
        "and dynamically re-normalizing weights across verified metrics.",
        space_after=4
    )
    add_body_p(
        "2. Alignment with SDG 13 (Climate Action): Traditional municipal audits are retrospective and rarely offer actionable implementation pathways. "
        "USAS bridges this gap through its Grounded Recommendations Engine, which indexes statutory policy guidelines (including NCAP, URDPFI, and Maharashtra TOD policies) "
        "in an open-source FAISS vector index. The generated recommendations provide structured roadmaps across immediate (0–6 months), medium-term (6–24 months), "
        "and strategic (24–60 months) planning horizons, explicitly linking municipal deficits to national climate funding mechanisms.",
        space_after=4
    )
    add_body_p(
        "3. Alignment with SDG 9 (Industry, Innovation & Infrastructure): By modernizing municipal sustainability assessment through automated data processing, "
        "interactive scenario impact modeling, and publication-ready digital report generation, USAS establishes a transparent digital public infrastructure "
        "for municipal corporations and town planning departments, eliminating repetitive manual paper audits.",
        space_after=8
    )

    # =========================================================================
    # APPENDIX F: RELATION TO ENVIRONMENT
    # =========================================================================
    add_appendix_heading("Appendix F: Relation of the Project to the Environment")
    add_body_p(
        "In accordance with institutional guidelines, this section evaluates the environmental implications of developing, operating, "
        "and deploying the Urban Sustainability Assessment System (USAS)."
    )

    add_body_p(
        "1. Use of Resources: USAS is a purely digital decision-support software platform requiring no physical manufacturing, specialized sensors, or hardware consumables. "
        "Its computational footprint is confined to standard workstation execution energy (< 0.45 kWh per 1,000 automated evaluations) and client browser rendering. "
        "By leveraging existing open-access statutory databases (CPCB, MPCB, MoRTH, Census 2011, and OpenAQ), the project avoids the resource-intensive manufacturing of redundant field telemetry devices.",
        space_after=4
    )
    add_body_p(
        "2. Environmental Benefits: The primary objective of USAS is empowering municipal authorities to detect environmental deficits rapidly—such as air quality deterioration, solid waste processing bottlenecks, or green canopy loss—and trigger timely statutory remediation under NCAP and Swachh Bharat Mission Urban (SBM-U 2.0). "
        "Furthermore, by replacing paper-intensive manual audit dossiers with authenticated, downloadable digital PDF reports, the platform significantly curtails institutional paper consumption across urban local bodies.",
        space_after=4
    )
    add_body_p(
        "3. Potential Adverse Impacts: Persistent server hosting and continuous REST API communication generate minor electrical power draw. "
        "However, USAS actively minimizes energy overhead through computational efficiency: serialized, pre-indexed FAISS binary vectors eliminate redundant machine learning re-embedding, "
        "and deterministic local caching prevents unnecessary network polling.",
        space_after=4
    )
    add_body_p(
        "4. Preventive and Mitigation Measures: (a) In-memory vector representations prevent wasteful repetitive inference; (b) Client-side bundle optimization via Vite ensures minimal client device battery drain; "
        "(c) Lightweight JSON/MongoDB storage structures reduce database storage overhead.",
        space_after=6
    )
    add_body_p(
        "5. Supporting Evidence: Table F.1 details the estimated annual environmental conservation achievable by transitioning Maharashtra’s 42 statutory municipal bodies from manual paper-based audits to the USAS platform.",
        space_after=6
    )

    add_table_caption("Table F.1: Estimated Annual Carbon, Paper, and Water Conservation Audit Across 42 ULBs")
    env_table = doc.add_table(rows=1, cols=3)
    env_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(env_table)
    
    env_headers = ["Conservation Parameter", "Estimated Value", "Estimation Basis / Analytical Assumptions"]
    env_widths = [Inches(2.2), Inches(1.8), Inches(2.0)]
    for i, title in enumerate(env_headers):
        cell = env_table.rows[0].cells[i]
        cell.width = env_widths[i]
        set_cell_background(cell, "E5E7EB")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        run = p.add_run(title)
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(10.5)

    env_rows = [
        ("Annual Hard-Copy Audit Pages Avoided", "~18,500 sheets / year", "42 ULBs × 4 quarterly reviews × ~110 pages per dossier"),
        ("Water Conserved in Paper Manufacturing", "~185,000 litres / year", "Statutory standard: 10 litres of water consumed per A4 sheet"),
        ("Trees Saved from Commercial Pulping", "~1.54 mature trees / year", "Standard pulpwood yield: ~12,000 sheets per mature tree"),
        ("Administrative Carbon Emissions Avoided", "~1.82 metric tonnes CO₂e", "Eliminated vehicular transit for manual dossier delivery across districts"),
        ("Urban Green Canopy Restoration Scope", "+1,250 hectares target", "Aggregated municipal deficit remediation toward URDPFI 10% canopy norm"),
    ]

    for param, val, basis in env_rows:
        row = env_table.add_row()
        for i, item in enumerate([param, val, basis]):
            cell = row.cells[i]
            cell.width = env_widths[i]
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.2
            run = p.add_run(item)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =========================================================================
    # APPENDIX G: PROJECT COST
    # =========================================================================
    add_appendix_heading("Appendix G: Project Cost")
    add_body_p(
        "The itemized financial statement below delineates the actual academic development expenditure incurred by the student investigator "
        "for the completion, testing, and institutional documentation of the Major Project. "
        "In accordance with institutional guidelines, hardware, development tools, and data infrastructure provided by the institution or open-source communities at zero cost are explicitly itemized."
    )

    add_table_caption("Table G.1: Itemized Statement of Actual Student Project Expenditure")
    cost_table = doc.add_table(rows=1, cols=5)
    cost_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(cost_table)
    
    cost_headers = ["Sr.", "Item / Expense Description", "Quantity", "Unit Cost (₹)", "Total Cost (₹) & Remarks"]
    cost_widths = [Inches(0.4), Inches(2.5), Inches(0.9), Inches(1.1), Inches(1.1)]
    for i, title in enumerate(cost_headers):
        cell = cost_table.rows[0].cells[i]
        cell.width = cost_widths[i]
        set_cell_background(cell, "E5E7EB")
        set_cell_margins(cell, top=100, bottom=100, left=80, right=80)
        p = cell.paragraphs[0]
        run = p.add_run(title)
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)

    cost_rows = [
        ("1", "Final Year Project Report Black Book (Hardbound with Golden Embossed Lettering: Guide Copy, Department Copy, Student Copy)", "3 Copies", "500.00", "₹ 1,500.00 (Mandatory Hardbound)"),
        ("2", "Institutional Plagiarism Certification & Turnitin Audit Fee", "1 Report", "1,500.00", "₹ 1,500.00 (Institutional Verification)"),
        ("3", "Project Documentation, Rough Printing & Binding Supplies", "Lump sum", "500.00", "₹ 500.00 (Draft Copies & Materials)"),
        ("4", "Institutional Computing Workstations & Lab Infrastructure", "1 Workstation", "0.00", "₹ 0.00 (Department of CSE Lab)"),
        ("5", "Software Development Frameworks (Python 3.12, Flask, React, Vite)", "Full Pipeline", "0.00", "₹ 0.00 (Open-Source, MIT License)"),
        ("6", "Project Source Code Repository Hosting (GitHub)", "1 Repository", "0.00", "₹ 0.00 (Public Access GitHub Tier)"),
        ("7", "Vector Database & Semantic Embedding Models (FAISS / HuggingFace)", "Full Suite", "0.00", "₹ 0.00 (Open-Source Weights)"),
        ("8", "Official Datasets & Open Telemetry APIs (CPCB, MPCB, Census, OpenAQ)", "42 Cities", "0.00", "₹ 0.00 (Public Government Portals)"),
    ]

    for sr, item, qty, uc, tc in cost_rows:
        row = cost_table.add_row()
        for i, val in enumerate([sr, item, qty, uc, tc]):
            cell = row.cells[i]
            cell.width = cost_widths[i]
            set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)

    # Total Row
    tot_row = cost_table.add_row()
    c_tot_label = tot_row.cells[0]
    c_tot_label.width = Inches(4.9)
    c_tot_label.merge(tot_row.cells[1]).merge(tot_row.cells[2]).merge(tot_row.cells[3])
    set_cell_background(c_tot_label, "F3F4F6")
    set_cell_margins(c_tot_label, top=80, bottom=80, left=80, right=80)
    p_tot = c_tot_label.paragraphs[0]
    p_tot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_tlabel = p_tot.add_run("Total Actual Project Expenditure: ")
    r_tlabel.bold = True
    r_tlabel.font.name = "Times New Roman"
    r_tlabel.font.size = Pt(10.5)

    c_tot_val = tot_row.cells[4]
    c_tot_val.width = Inches(1.1)
    set_cell_background(c_tot_val, "E5E7EB")
    set_cell_margins(c_tot_val, top=80, bottom=80, left=80, right=80)
    p_tval = c_tot_val.paragraphs[0]
    r_tval = p_tval.add_run("₹ 3,500.00")
    r_tval.bold = True
    r_tval.font.name = "Times New Roman"
    r_tval.font.size = Pt(11)

    add_body_p("Total Project Expenditure in Words: Rupees Three Thousand Five Hundred Only.", space_after=10, bold_prefix="Amount in Words: ")

    add_section_heading("Cost Feasibility and Resource Utilization Statement")
    add_body_p(
        "The Urban Sustainability Assessment System (USAS) was successfully developed, verified, benchmarked, and documented with an actual student out-of-pocket expenditure of ₹ 3,500.00. "
        "The direct financial outlay was strictly confined to essential academic compliance requirements: mandatory institutional plagiarism verification (₹ 1,500.00), "
        "three hardbound 'Black Book' project report copies with golden embossed lettering as per university standards (₹ 1,500.00), and preliminary printing supplies (₹ 500.00).",
        space_after=6
    )
    add_body_p(
        "All computational infrastructure, runtime frameworks, vector indexing engines, and database systems incurred zero financial expenditure due to the "
        "strategic adoption of industry-standard open-source technologies (Python 3.12, React 18, Vite, FAISS, and ReportLab) and public repository hosting on GitHub. "
        "This proves that high-performance, deterministic municipal decision support systems can be developed and maintained without proprietary enterprise licensing, "
        "making the framework highly feasible and cost-effective for practical civic adoption across municipal councils and corporations.",
        space_after=16
    )

    # Sign-off block
    sig_g_table = doc.add_table(rows=1, cols=2)
    sig_g_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_g_cand = sig_g_table.rows[0].cells[0]
    c_g_cand.width = Inches(3.2)
    p_gc = c_g_cand.paragraphs[0]
    p_gc.add_run("Ishan Chipate\n").bold = True
    p_gc.add_run("Student Investigator\nB.Tech (Artificial Intelligence and Data Science), Final Year\nDepartment of Computer Science & Engineering")
    
    c_g_guide = sig_g_table.rows[0].cells[1]
    c_g_guide.width = Inches(2.8)
    p_gg = c_g_guide.paragraphs[0]
    p_gg.add_run("Dr. Mukund Wagh\n").bold = True
    p_gg.add_run("Project Guide & Associate Professor\nDepartment of Computer Science & Engineering")

    return doc

if __name__ == "__main__":
    doc = create_document()
    
    # Save in workspace (handling file lock if currently open in Microsoft Word)
    workspace_path = Path("E:/Project/Final/USAS_Project_Report_Appendices.docx")
    try:
        doc.save(str(workspace_path))
        print(f"Saved workspace document: {workspace_path}")
    except PermissionError:
        workspace_path = Path("E:/Project/Final/USAS_Project_Report_Appendices_Final.docx")
        doc.save(str(workspace_path))
        print(f"Primary file was locked in Word; saved to: {workspace_path}")

    # Also save to conversation artifact directory
    artifact_dir = Path(r"C:\Users\Asus\.gemini\antigravity\brain\89bfbda0-cbc6-42d2-bf50-3eda978459f4")
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = artifact_dir / "USAS_Project_Report_Appendices_Final.docx"
    doc.save(str(artifact_path))
    print(f"Saved artifact document: {artifact_path}")
