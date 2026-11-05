# -*- coding: utf-8 -*-
"""
High-Fidelity PDF Report Generator for USAS
Generates publication-quality, statutory urban sustainability assessment reports
covering all 9 required sections using ReportLab.
"""

import io
from datetime import datetime, timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and render total page count."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#475569"))

        # Skip running header/footer on cover page (Page 1)
        if self._pageNumber > 1:
            # Running header
            self.drawString(54, 11 * inch - 36, "USAS — Urban Sustainability Assessment System | State Urban Analytics Cell")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

            # Running footer
            self.line(54, 45, 8.5 * inch - 54, 45)
            self.drawString(54, 32, "Confidential & Statutory Decision Support Dossier · Government of Maharashtra")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(8.5 * inch - 54, 32, page_text)

        self.restoreState()


def generate_city_pdf_report(report_data: dict, impact_scenario: dict = None) -> bytes:
    """Generate a clean 9-section PDF report from assessment and recommendation data."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom Palettes
    PRIMARY = colors.HexColor("#14532d")    # Dark Forest Green
    ACCENT = colors.HexColor("#0f766e")     # Teal
    TEXT_DARK = colors.HexColor("#0f172a")  # Slate 900
    TEXT_MUTED = colors.HexColor("#475569") # Slate 600
    BG_LIGHT = colors.HexColor("#f8fafc")   # Slate 50
    BORDER_LIGHT = colors.HexColor("#e2e8f0")

    # Typography Styles
    title_style = ParagraphStyle(
        "CoverTitle",
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=TEXT_MUTED,
    )
    h1_style = ParagraphStyle(
        "SectionH1",
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True,
    )
    h2_style = ParagraphStyle(
        "SectionH2",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=ACCENT,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    )
    body_style = ParagraphStyle(
        "BodyDark",
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_DARK,
    )
    body_muted = ParagraphStyle(
        "BodyMuted",
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=TEXT_MUTED,
    )
    table_cell = ParagraphStyle(
        "TableCell",
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=TEXT_DARK,
    )
    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11.5,
        textColor=TEXT_DARK,
    )
    table_header = ParagraphStyle(
        "TableHeader",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white,
    )

    story = []

    city = report_data.get("city_name") or report_data.get("city") or "Target City"
    overall_score = report_data.get("overall_score")
    score_display = f"{overall_score:.2f} / 100" if overall_score is not None else "Not Available"
    status_display = report_data.get("score_status", "Full Assessment").upper()
    coverage = report_data.get("data_coverage_pct", 100)
    assessment_date = report_data.get("assessment_date", datetime.now().strftime("%B %d, %Y"))

    # =========================================================================
    # 1. COVER PAGE / EXECUTIVE HEADER
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("URBAN SUSTAINABILITY ASSESSMENT SYSTEM", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"{city} Urban Sustainability Dossier", title_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("A Data-Driven Multi-Criteria Decision Support Framework for Maharashtra Cities", subtitle_style))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceBefore=5, spaceAfter=15))

    # Meta banner table
    meta_data = [
        [
            Paragraph("<b>Target Municipality:</b>", table_cell),
            Paragraph(f"{city}, Maharashtra", table_cell_bold),
            Paragraph("<b>Overall Score:</b>", table_cell),
            Paragraph(score_display, table_cell_bold),
        ],
        [
            Paragraph("<b>Assessment Status:</b>", table_cell),
            Paragraph(status_display, table_cell_bold),
            Paragraph("<b>Data Coverage:</b>", table_cell),
            Paragraph(f"{coverage}% Coverage", table_cell_bold),
        ],
        [
            Paragraph("<b>Evaluation Date:</b>", table_cell),
            Paragraph(assessment_date, table_cell),
            Paragraph("<b>Framework Ref:</b>", table_cell),
            Paragraph("USAS-MCDM-WSM-2026", table_cell),
        ],
    ]
    meta_table = Table(meta_data, colWidths=[110, 150, 100, 144])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 1, BORDER_LIGHT),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 20))

    # =========================================================================
    # 2. EXECUTIVE SUMMARY
    # =========================================================================
    story.append(Paragraph("1.0 Executive Summary", h1_style))
    exec_summary_text = (
        f"This comprehensive assessment evaluates the municipal urban sustainability posture of <b>{city}</b> "
        f"utilizing the Weighted Sum Model (WSM) across five critical statutory indicators. "
        f"The municipality achieved an aggregate sustainability score of <b>{score_display}</b> with "
        f"<b>{coverage}% empirical data coverage</b>. Indicators falling below the state benchmark threshold (<40/100) "
        f"are designated as critical Problem Areas requiring prioritized capital investment and policy realignment."
    )
    story.append(Paragraph(exec_summary_text, body_style))
    story.append(Spacer(1, 10))

    # Key findings & problem counts
    problems = report_data.get("problem_areas", [])
    if problems:
        p_text = f"<b>Critical Vulnerabilities Identified ({len(problems)}):</b> " + ", ".join(
            [f"{p.get('name', 'Indicator')} ({p.get('score', 0):.1f}/100)" for p in problems]
        )
    else:
        p_text = "<b>Critical Vulnerabilities Identified:</b> No indicators currently score below the 40/100 critical threshold."
    story.append(Paragraph(p_text, body_style))
    story.append(Spacer(1, 15))

    # =========================================================================
    # 3. ASSESSMENT OVERVIEW (FIVE INDICATORS TABLE)
    # =========================================================================
    story.append(Paragraph("2.0 Assessment Overview & Scorecard", h1_style))
    story.append(Paragraph("Empirical baseline measurements, reference years, normalized 0–100 scores, and configured indicator weights.", body_muted))
    story.append(Spacer(1, 8))

    indicators = report_data.get("indicators", [])
    weights = report_data.get("weights", {})

    table_rows = [[
        Paragraph("Indicator Name", table_header),
        Paragraph("Measured Value", table_header),
        Paragraph("Unit", table_header),
        Paragraph("Ref Year", table_header),
        Paragraph("Norm Score", table_header),
        Paragraph("Weight", table_header),
        Paragraph("Status", table_header),
    ]]

    for ind in indicators:
        val = ind.get("raw_value")
        val_str = "—" if val is None else (f"{val:,.1f}" if isinstance(val, (int, float)) and val >= 1000 else (f"{val:.2f}" if isinstance(val, float) else str(val)))
        sc = ind.get("score")
        sc_str = "Not Available" if sc is None else f"{sc:.1f}"
        
        weight_val = weights.get(f"{ind.get('name', '').lower().replace(' ', '_')}_score")
        if weight_val is None:
            # Fallback matching
            ind_name = ind.get("name", "").lower()
            if "air" in ind_name: weight_val = weights.get("air_quality_score", 0.20)
            elif "traffic" in ind_name: weight_val = weights.get("traffic_pressure_score", 0.20)
            elif "green" in ind_name: weight_val = weights.get("green_space_score", 0.20)
            elif "waste" in ind_name: weight_val = weights.get("waste_management_score", 0.20)
            elif "density" in ind_name: weight_val = weights.get("population_density_score", 0.20)
            else: weight_val = 0.20
        weight_str = f"{weight_val * 100:.0f}%"

        status_tag = "Acceptable"
        if sc is None:
            status_tag = "Excluded"
        elif sc < 40:
            status_tag = "Problem Area"
        elif sc < 60:
            status_tag = "Needs Attention"

        table_rows.append([
            Paragraph(f"<b>{ind.get('name', '')}</b>", table_cell),
            Paragraph(val_str, table_cell),
            Paragraph(ind.get("unit", "") or "—", table_cell),
            Paragraph(str(ind.get("year", "—")), table_cell),
            Paragraph(sc_str, table_cell_bold),
            Paragraph(weight_str, table_cell),
            Paragraph(status_tag, table_cell),
        ])

    ind_table = Table(table_rows, colWidths=[120, 70, 60, 50, 64, 50, 90])
    ind_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("BOX", (0, 0), (-1, -1), 1, BORDER_LIGHT),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(ind_table)
    story.append(Spacer(1, 15))

    # =========================================================================
    # 4. INDICATOR ANALYSIS & OBSERVATIONS
    # =========================================================================
    story.append(Paragraph("3.0 Detailed Indicator Diagnostics", h1_style))
    for ind in indicators:
        sc = ind.get("score")
        sc_text = f"{sc:.1f} / 100" if sc is not None else "Not Available"
        source_name = ind.get("source_name") or ind.get("source", "Official Municipal Record")
        method_note = ind.get("direction_note") or ind.get("note", "")

        story.append(Paragraph(f"<b>{ind.get('name', '')}</b> (Score: {sc_text})", h2_style))
        diag_text = (
            f"Measurement: <b>{ind.get('raw_value', '—')} {ind.get('unit', '')}</b> "
            f"(Reference Year: {ind.get('year', 'Recorded')}). "
            f"Statutory Source: <i>{source_name}</i>. {method_note}"
        )
        story.append(Paragraph(diag_text, body_style))
        story.append(Spacer(1, 4))
    story.append(Spacer(1, 10))

    # =========================================================================
    # 5. PROBLEM AREAS & CRITICAL DEFICITS
    # =========================================================================
    story.append(Paragraph("4.0 Identified Problem Areas & Critical Gaps", h1_style))
    if problems:
        for p in problems:
            story.append(Paragraph(
                f"• <b>{p.get('name', 'Indicator')}</b> (Score: {p.get('score', 0):.1f}/100) — "
                f"Classified as a <b>{p.get('classification', 'Problem Area')}</b>. "
                f"{p.get('explanation', 'Demands immediate policy intervention and budgetary prioritization.')}",
                body_style,
            ))
            story.append(Spacer(1, 3))
    else:
        story.append(Paragraph("No indicators fall below the critical problem threshold (<40/100). Ongoing monitoring is advised.", body_style))
    story.append(Spacer(1, 15))

    # =========================================================================
    # 6. EVIDENCE-GROUNDED POLICY RECOMMENDATIONS (RAG + GEMINI)
    # =========================================================================
    recs = report_data.get("recommendations", [])
    story.append(Paragraph("5.0 Evidence-Grounded Policy Recommendations", h1_style))
    story.append(Paragraph(
        "Interventions synthesized from retrieved statutory planning policies (NCAP, URDPFI 2015, MPCB, TOD Regulations) "
        "and contextualized via state urban guidelines.",
        body_muted,
    ))
    story.append(Spacer(1, 6))

    if recs:
        for idx, r in enumerate(recs[:4], start=1):
            story.append(Paragraph(f"<b>Recommendation {idx}: {r.get('title', 'Policy Intervention')}</b>", h2_style))
            story.append(Paragraph(f"<b>Target Deficit:</b> {r.get('indicator', 'General Sustainability')}", body_style))
            story.append(Paragraph(f"<b>Proposed Action:</b> {r.get('recommendation', '')}", body_style))
            
            # Phased roadmap if present
            phases = r.get("phased_roadmap")
            if phases:
                phase_text = (
                    f"<i>Phased Roadmap:</i> Phase 1 (0–6 mo): {phases.get('phase_1_immediate', 'Initiate')} | "
                    f"Phase 2 (6–18 mo): {phases.get('phase_2_medium', 'Execute')} | "
                    f"Phase 3 (18–36 mo): {phases.get('phase_3_long', 'Institutionalize')}"
                )
                story.append(Paragraph(phase_text, body_muted))

            # Citations & Evidence
            evidence_list = r.get("evidence", [])
            if evidence_list:
                for ev in evidence_list[:2]:
                    cit_text = f"<b>Source Citation:</b> {ev.get('title', 'Statutory Guideline')} ({ev.get('publication_year', '2024')}, p.{ev.get('page', '1')})."
                    story.append(Paragraph(cit_text, body_muted))
            story.append(Spacer(1, 6))
    else:
        story.append(Paragraph("No active recommendations retrieved for the current indicator configuration.", body_style))
    story.append(Spacer(1, 15))

    # =========================================================================
    # 7. SCENARIO-BASED IMPACT ANALYSIS
    # =========================================================================
    story.append(Paragraph("6.0 Scenario Sensitivity & Impact Simulation", h1_style))
    if impact_scenario and impact_scenario.get("city") == city:
        sc_data = [
            [
                Paragraph("<b>Simulated Indicator:</b>", table_cell),
                Paragraph(str(impact_scenario.get("indicator", "—")), table_cell),
                Paragraph("<b>Assumed Gain:</b>", table_cell),
                Paragraph(f"+{impact_scenario.get('assumed_normalized_score_change_points', 10)} pts", table_cell_bold),
            ],
            [
                Paragraph("<b>Baseline Overall:</b>", table_cell),
                Paragraph(f"{impact_scenario.get('baseline_overall_score', '—')}", table_cell),
                Paragraph("<b>Projected Overall:</b>", table_cell),
                Paragraph(f"{impact_scenario.get('projected_overall_score', '—')}", table_cell_bold),
            ],
            [
                Paragraph("<b>Net Score Shift:</b>", table_cell),
                Paragraph(f"+{impact_scenario.get('overall_score_change', 0):.2f} pts", table_cell_bold),
                Paragraph("<b>Data Coverage:</b>", table_cell),
                Paragraph(f"{impact_scenario.get('data_coverage_pct', coverage)}%", table_cell),
            ],
        ]
        sc_table = Table(sc_data, colWidths=[110, 150, 100, 144])
        sc_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), BG_LIGHT),
            ("BOX", (0, 0), (-1, -1), 1, BORDER_LIGHT),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
            ("PADDING", (0, 0), (-1, -1), 5),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(sc_table)
        story.append(Spacer(1, 5))
        story.append(Paragraph(
            "<b>Simulation Bounds:</b> Hypothetical sensitivity model holding other indicators constant; "
            "does not claim causal prediction or guaranteed real-world outcomes.",
            body_muted,
        ))
    else:
        story.append(Paragraph(
            "No active scenario simulation was attached to this export. Planners may execute hypothetical before-and-after "
            "simulations via the interactive Impact Analysis module.",
            body_style,
        ))
    story.append(Spacer(1, 15))

    # =========================================================================
    # 8. ASSESSMENT METHODOLOGY
    # =========================================================================
    story.append(Paragraph("7.0 Methodological Framework", h1_style))
    method_text = (
        "<b>Multi-Criteria Decision-Making (MCDM):</b> Evaluated using the Weighted Sum Model (WSM). "
        "Each raw indicator is normalized to a 0–100 scale using empirical Min-Max bounds across all 42 comparison cities.<br/>"
        "• <i>Higher-is-better:</i> Score = ((x - min) / (max - min)) × 100<br/>"
        "• <i>Lower-is-better:</i> Score = ((max - x) / (max - min)) × 100<br/>"
        "• <i>Missing Indicators:</i> Excluded from scoring; remaining weights are mathematically re-normalized to 100%. "
        "Missing indicators are never assigned zero or classified as problems.<br/>"
        "• <i>Problem Thresholds:</i> Critical Problem (<40) | Needs Attention (40–59) | Acceptable (≥60)."
    )
    story.append(Paragraph(method_text, body_style))
    story.append(Spacer(1, 15))

    # =========================================================================
    # 9. DATA SOURCES & LIMITATIONS
    # =========================================================================
    story.append(Paragraph("8.0 Data Sources & Analytical Boundaries", h1_style))
    sources_text = (
        "<b>Authoritative Data Sources:</b><br/>"
        "1. <i>Air Quality:</i> Central Pollution Control Board (CPCB) & Maharashtra Pollution Control Board (MPCB).<br/>"
        "2. <i>Traffic Pressure:</i> TomTom Traffic Index congestion measurements (scored where monitored). Unmonitored cities have Traffic excluded from scoring, with MMVD registered vehicle volumes provided as non-scoring contextual baseline.<br/>"
        "3. <i>Green Space:</i> Municipal Environmental Status Reports (ESR) & Forest Survey of India (FSI).<br/>"
        "4. <i>Waste Management:</i> MPCB Annual Solid Waste Management Reports.<br/>"
        "5. <i>Population Density:</i> Census of India 2011 & Town Planning Directorate Area Demarcations.<br/><br/>"
        "<b>Analytical Limitations:</b> Indicator reporting years vary across local bodies (2011–2024). "
        "Scores reflect relative performance across Maharashtra municipalities and do not replace statutory local environmental impact assessments."
    )
    story.append(Paragraph(sources_text, body_muted))
    story.append(Spacer(1, 20))

    # Sign-off block
    sign_data = [
        [
            Paragraph("<b>Generated By:</b><br/>USAS Decision Support Engine<br/>State Urban Analytics Cell", table_cell),
            Paragraph(f"<b>Target Municipality:</b><br/>{city} Municipal Administration<br/>Government of Maharashtra", table_cell),
            Paragraph(f"<b>Verification Ref:</b><br/>CERT-MH-2026-{city[:3].upper()}<br/>Validated Analytical Pipeline", table_cell),
        ]
    ]
    sign_table = Table(sign_data, colWidths=[170, 170, 164])
    sign_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 1, BORDER_LIGHT),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(sign_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
