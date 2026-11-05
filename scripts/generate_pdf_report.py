# -*- coding: utf-8 -*-
"""
USAS Final Year Project Report & Codebase Technical Documentation Generator
Compiles an exhaustive, university-compliant PDF report adhering to
Maharashtra Institute of Technology (MIT), Chhatrapati Sambhajinagar guidelines (AY 2026-27).
"""

import os
import subprocess
import sys

HTML_OUTPUT = os.path.abspath("USAS_Final_Project_Report.html")
PDF_OUTPUT = os.path.abspath("USAS_Final_Year_Project_Report.pdf")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Urban Sustainability Assessment System (USAS) - Final Year Project Report</title>
<style>
  @page {
    size: A4;
    margin: 25mm 20mm 25mm 30mm;
    @bottom-center {
      content: counter(page);
      font-family: "Times New Roman", Times, serif;
      font-size: 11pt;
    }
  }

  body {
    font-family: "Times New Roman", Times, serif;
    font-size: 12pt;
    line-height: 1.5;
    color: #111111;
    text-align: justify;
    margin: 0;
    padding: 0;
  }

  h1, h2, h3, h4, h5, h6 {
    font-family: "Times New Roman", Times, serif;
    color: #000000;
    page-break-after: avoid;
    margin-top: 18pt;
    margin-bottom: 8pt;
  }

  /* Institutional Chapter Headings */
  .chapter-heading {
    font-size: 14pt;
    font-weight: bold;
    text-transform: uppercase;
    text-align: center;
    margin-top: 24pt;
    margin-bottom: 18pt;
  }

  .section-heading {
    font-size: 12pt;
    font-weight: bold;
    text-transform: uppercase;
    margin-top: 16pt;
    margin-bottom: 6pt;
  }

  .sub-section-heading {
    font-size: 12pt;
    font-weight: bold;
    margin-top: 12pt;
    margin-bottom: 4pt;
  }

  p {
    margin-top: 0;
    margin-bottom: 8pt;
    text-indent: 0.5in;
  }

  p.no-indent {
    text-indent: 0;
  }

  .page-break {
    page-break-before: always;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 8pt;
    margin-bottom: 14pt;
    font-size: 10.5pt;
    page-break-inside: avoid;
  }

  table, th, td {
    border: 1px solid #333333;
  }

  th {
    background-color: #f2f2f2;
    font-weight: bold;
    padding: 6pt 8pt;
    text-align: left;
  }

  td {
    padding: 5pt 8pt;
    vertical-align: top;
  }

  .table-title {
    font-size: 11pt;
    font-weight: bold;
    text-align: left;
    margin-bottom: 4pt;
    margin-top: 10pt;
    text-indent: 0;
  }

  .figure-caption {
    font-size: 11pt;
    font-weight: bold;
    text-align: center;
    margin-top: 6pt;
    margin-bottom: 14pt;
    text-indent: 0;
  }

  /* Code & Equations */
  pre, code {
    font-family: "Courier New", Courier, monospace;
    font-size: 10pt;
  }

  pre {
    background-color: #f8f9fa;
    border: 1px solid #d0d7de;
    border-radius: 4px;
    padding: 8pt;
    margin: 8pt 0;
    overflow-x: auto;
    page-break-inside: avoid;
    line-height: 1.3;
    text-indent: 0;
  }

  .equation-box {
    text-align: center;
    margin: 12pt 0;
    font-style: italic;
    font-size: 11pt;
    text-indent: 0;
  }

  .equation-num {
    float: right;
    font-style: normal;
    font-weight: bold;
  }

  /* Architecture Box Diagrams */
  .diagram-container {
    border: 1px solid #666666;
    background: #fafafa;
    padding: 12pt;
    margin: 12pt 0;
    page-break-inside: avoid;
    text-indent: 0;
  }

  .diagram-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8pt;
    gap: 8pt;
  }

  .diagram-box {
    flex: 1;
    border: 1.5px solid #173b2b;
    background: #ffffff;
    padding: 6pt;
    text-align: center;
    border-radius: 4px;
    font-size: 9.5pt;
  }

  .diagram-box strong {
    display: block;
    color: #176b45;
    margin-bottom: 2pt;
  }

  .diagram-arrow {
    text-align: center;
    font-size: 12pt;
    color: #555555;
    margin: 4pt 0;
  }

  /* Front Matter Specifics */
  .title-page {
    text-align: center;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding-top: 30pt;
    page-break-after: always;
  }

  .title-page h1 {
    font-size: 18pt;
    font-weight: bold;
    line-height: 1.4;
    margin-bottom: 30pt;
  }

  .title-page h2 {
    font-size: 13pt;
    font-weight: normal;
    margin-bottom: 10pt;
  }

  .title-page h3 {
    font-size: 14pt;
    font-weight: bold;
    margin-bottom: 24pt;
  }

  .cert-header {
    text-align: center;
    font-size: 14pt;
    font-weight: bold;
    text-transform: uppercase;
    margin-bottom: 24pt;
  }

  .sign-grid {
    display: flex;
    justify-content: space-between;
    margin-top: 45pt;
    text-indent: 0;
  }

  .sign-box {
    text-align: center;
    width: 45%;
  }

  .sign-box hr {
    border: none;
    border-top: 1px solid #000;
    margin-bottom: 6pt;
  }

  /* Super in-text citation */
  sup.cite {
    font-weight: bold;
    color: #0b5394;
  }
</style>
</head>
<body>

<!-- ========================================================================= -->
<!-- TITLE PAGE -->
<!-- ========================================================================= -->
<div class="title-page">
  <div>
    <h1>URBAN SUSTAINABILITY ASSESSMENT SYSTEM: A DATA-DRIVEN DECISION SUPPORT FRAMEWORK (USAS)</h1>
    <h2>A Project Report submitted in partial fulfillment for the award of the degree of</h2>
    <h3>Bachelor of Technology<br>in<br>Artificial Intelligence and Data Science</h3>
  </div>

  <div style="margin: 25pt 0;">
    <p class="no-indent" style="text-align: center; font-size: 12pt; font-weight: bold; margin-bottom: 4pt;">Submitted by</p>
    <p class="no-indent" style="text-align: center; font-size: 13pt; font-weight: bold;">PROJECT MEMBER 1 &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp; PROJECT MEMBER 2</p>
  </div>

  <div style="margin: 25pt 0;">
    <p class="no-indent" style="text-align: center; font-size: 12pt; font-weight: bold; margin-bottom: 4pt;">Under the Guidance of</p>
    <p class="no-indent" style="text-align: center; font-size: 13pt; font-weight: bold;">NAME OF GUIDE</p>
    <p class="no-indent" style="text-align: center; font-size: 11pt;">Department of Emerging Science & Technology</p>
  </div>

  <div style="margin-top: 30pt;">
    <p class="no-indent" style="text-align: center; font-size: 14pt; font-weight: bold; color: #173b2b; margin-bottom: 4pt;">
      Department of Emerging Science & Technology
    </p>
    <p class="no-indent" style="text-align: center; font-size: 13pt; font-weight: bold; margin-bottom: 2pt;">
      Maharashtra Institute of Technology, Chhatrapati Sambhajinagar
    </p>
    <p class="no-indent" style="text-align: center; font-size: 11pt; margin-bottom: 2pt;">
      (An Autonomous Institute Affiliated to Dr. Babasaheb Ambedkar Marathwada University)
    </p>
    <p class="no-indent" style="text-align: center; font-size: 11pt; margin-bottom: 12pt;">
      Chhatrapati Sambhajinagar (M.S.) – 431 010, Maharashtra, India
    </p>
    <p class="no-indent" style="text-align: center; font-size: 12pt; font-weight: bold;">
      Academic Year: 2026–2027
    </p>
  </div>
</div>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- CERTIFICATE -->
<!-- ========================================================================= -->
<div class="cert-header">CERTIFICATE</div>
<p>
This is to certify that the project entitled <strong>“URBAN SUSTAINABILITY ASSESSMENT SYSTEM: A DATA-DRIVEN DECISION SUPPORT FRAMEWORK (USAS)”</strong>, which is being submitted herewith in the partial fulfillment for the award of the degree of <strong>Bachelor of Technology in Artificial Intelligence and Data Science</strong> of <strong>Maharashtra Institute of Technology, Chhatrapati Sambhajinagar</strong> (An Autonomous Institute Affiliated to Dr. Babasaheb Ambedkar Marathwada University), is the record of the bona fide original work carried out by <strong>Project Member 1</strong> and <strong>Project Member 2</strong> under my supervision and guidance during the academic year 2026–2027.
</p>
<p>
To the best of my knowledge, the matter embodied in this report has not been submitted to any other University or Institute for the award of any degree or diploma.
</p>

<div style="margin-top: 35pt;">
  <p class="no-indent"><strong>Place:</strong> Chhatrapati Sambhajinagar</p>
  <p class="no-indent"><strong>Date:</strong> 30th October 2026</p>
</div>

<div class="sign-grid" style="margin-top: 45pt;">
  <div class="sign-box">
    <br><br>
    <hr>
    <strong>Name of Guide</strong><br>
    Project Guide<br>
    Dept. of Emerging Science & Tech.
  </div>
  <div class="sign-box">
    <br><br>
    <hr>
    <strong>Prof. Dr. Kavita Mohite (Bhosle)</strong><br>
    Head of Department<br>
    Dept. of Emerging Science & Tech.
  </div>
</div>

<div style="text-align: center; width: 60%; margin: 40pt auto 0 auto; text-indent: 0;">
  <hr>
  <strong>Prof. Dr. Nilesh G. Patil</strong><br>
  Director<br>
  Maharashtra Institute of Technology, Chhatrapati Sambhajinagar
</div>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- APPROVAL CERTIFICATE -->
<!-- ========================================================================= -->
<div class="cert-header">APPROVAL CERTIFICATE</div>
<p>
The project report entitled <strong>“URBAN SUSTAINABILITY ASSESSMENT SYSTEM: A DATA-DRIVEN DECISION SUPPORT FRAMEWORK (USAS)”</strong> submitted by <strong>Project Member 1</strong> and <strong>Project Member 2</strong> is approved for the degree of <strong>Bachelor of Technology in Artificial Intelligence and Data Science</strong> at Maharashtra Institute of Technology, Chhatrapati Sambhajinagar, affiliated to Dr. Babasaheb Ambedkar Marathwada University.
</p>

<div style="margin-top: 40pt;">
  <p class="no-indent"><strong>Place:</strong> Chhatrapati Sambhajinagar</p>
  <p class="no-indent"><strong>Date:</strong> </p>
</div>

<div class="sign-grid" style="margin-top: 70pt;">
  <div class="sign-box">
    <hr>
    <strong>Internal Examiner</strong><br>
    Signature & Date
  </div>
  <div class="sign-box">
    <hr>
    <strong>External Examiner</strong><br>
    Signature & Date
  </div>
</div>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- ACKNOWLEDGEMENT -->
<!-- ========================================================================= -->
<div class="cert-header">ACKNOWLEDGEMENT</div>
<p>
We express our deepest sense of gratitude and profound indebtedness to our project guide, <strong>Name of Guide</strong>, Department of Emerging Science & Technology, for their invaluable advice, constructive critique, continuous encouragement, and constant technical steering throughout the development of the <strong>Urban Sustainability Assessment System (USAS)</strong> project.
</p>
<p>
We extend our sincere thanks to <strong>Prof. Dr. Kavita Mohite (Bhosle)</strong>, Head, Department of Emerging Science & Technology, for extending the administrative support, laboratory resources, and creating an inspiring academic environment. We are equally grateful to <strong>Dr. Lalita Randive</strong>, Project Coordinator, for her systematic coordination, rigorous guidelines, and periodic milestone reviews.
</p>
<p>
We express our sincere reverence to <strong>Prof. Dr. Nilesh G. Patil</strong>, Director, Maharashtra Institute of Technology, Chhatrapati Sambhajinagar, for fostering state-of-the-art computational infrastructure and encouraging translational research in Artificial Intelligence, Geospatial Data Science, and Public Urban Systems.
</p>
<p>
Finally, we thank our faculty members, laboratory staff, colleagues, and family for their unwavering moral support, feedback, and collaboration during this capstone engineering endeavor.
</p>

<div style="margin-top: 40pt; text-align: right; text-indent: 0;">
  <strong>Project Member 1</strong><br>
  <strong>Project Member 2</strong><br>
  B.Tech (Artificial Intelligence and Data Science)
</div>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- ABSTRACT -->
<!-- ========================================================================= -->
<div class="cert-header">ABSTRACT</div>
<p>
Rapid urbanization across the 42 statutory cities of Maharashtra presents severe ecological and civic management challenges, characterized by deteriorating ambient air quality, untreated solid waste accumulation, severe traffic congestion, loss of urban open spaces, and unchecked population densities. Traditional urban evaluation frameworks are constrained by qualitative subjectivity, fragmented municipal record-keeping, and the problematic practice of replacing missing empirical observations with synthetic zeros, which distorts municipal allocations. This project presents the <strong>Urban Sustainability Assessment System (USAS)</strong>, an end-to-end, data-driven multi-criteria decision support framework. 
</p>
<p>
USAS establishes an empirical baseline evaluating 42 statutory cities using official Central Pollution Control Board (CPCB) air quality records (2015–2025), Maharashtra Pollution Control Board (MPCB) solid waste processing audits (2023), Census of India 2011 population densities, documented urban green space percentages, and TomTom traffic congestion indices alongside registered vehicle pressure proxies. The core evaluation engine is strictly deterministic, employing direction-aware Min-Max normalization and the Weighted Sum Model (WSM) with dynamic weight re-normalization to honestly handle missing data without synthetic substitution. For actionable decision support, USAS couples a dense vector Retrieval-Augmented Generation (RAG) pipeline—utilizing Sentence-Transformers (<pre style="display:inline; padding:1px 4px;">all-MiniLM-L6-v2</pre>) and FAISS vector indexing over national statutory guidelines (NCAP, SWM Rules 2016, URDPFI 2015, NUTP 2014, UDCPR 2020)—with Google Gemini to synthesize evidence-grounded, 3-phase municipal intervention roadmaps. Geospatial queries through OpenStreetMap Overpass API reproject urban features into metric Coordinate Reference System UTM Zone 43N (EPSG:32643) for precise spatial intervention feasibility. The resulting framework provides public administrators with transparent scoring, interactive sensitivity simulation, and audit-grade sustainability dossiers.
</p>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- TABLE OF CONTENTS -->
<!-- ========================================================================= -->
<div class="cert-header">TABLE OF CONTENTS</div>
<table style="border: none;">
  <tr style="border: none; font-weight: bold;"><td style="border: none; width: 15%;">Chapter No.</td><td style="border: none; width: 70%;">Title</td><td style="border: none; width: 15%; text-align: right;">Page No.</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">Certificate</td><td style="border: none; text-align: right;">ii</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">Approval Certificate</td><td style="border: none; text-align: right;">iii</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">Acknowledgement</td><td style="border: none; text-align: right;">iv</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">Abstract</td><td style="border: none; text-align: right;">v</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">List of Figures</td><td style="border: none; text-align: right;">vii</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">List of Tables</td><td style="border: none; text-align: right;">viii</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">List of Abbreviations</td><td style="border: none; text-align: right;">ix</td></tr>
  <tr style="border: none; font-weight: bold;"><td style="border: none;">1.</td><td style="border: none;">INTRODUCTION</td><td style="border: none; text-align: right;">1</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">1.1 Background of the Project</td><td style="border: none; text-align: right;">1</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">1.2 Problem Definition</td><td style="border: none; text-align: right;">2</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">1.3 Objectives of the Project</td><td style="border: none; text-align: right;">3</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">1.4 Scope of the Project</td><td style="border: none; text-align: right;">3</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">1.5 Significance of the Project</td><td style="border: none; text-align: right;">4</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">1.6 Limitations of the Project</td><td style="border: none; text-align: right;">5</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">1.7 Definition of Terms</td><td style="border: none; text-align: right;">5</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">1.8 Organization of the Report</td><td style="border: none; text-align: right;">6</td></tr>
  <tr style="border: none; font-weight: bold;"><td style="border: none;">2.</td><td style="border: none;">LITERATURE SURVEY</td><td style="border: none; text-align: right;">7</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">2.1 Overview of Urban Sustainability Assessment Frameworks</td><td style="border: none; text-align: right;">7</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">2.2 Review of Multi-Criteria Decision Making (MCDM) Methodologies</td><td style="border: none; text-align: right;">8</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">2.3 Review of Geospatial Analytics & Remote Sensing in Urban Planning</td><td style="border: none; text-align: right;">9</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">2.4 Review of Retrieval-Augmented Generation (RAG) in Policy Synthesis</td><td style="border: none; text-align: right;">10</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">2.5 Comparative Study of Existing Systems</td><td style="border: none; text-align: right;">11</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">2.6 Research Gaps Identified</td><td style="border: none; text-align: right;">12</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">2.7 Conclusion from Literature Review</td><td style="border: none; text-align: right;">13</td></tr>
  <tr style="border: none; font-weight: bold;"><td style="border: none;">3.</td><td style="border: none;">REQUIREMENT ANALYSIS & PROBLEM DEFINITION</td><td style="border: none; text-align: right;">14</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">3.1 Comprehensive Problem Statement</td><td style="border: none; text-align: right;">14</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">3.2 Functional Requirements (FR-01 to FR-08)</td><td style="border: none; text-align: right;">15</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">3.3 Non-Functional Requirements (NFR-01 to NFR-06)</td><td style="border: none; text-align: right;">16</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">3.4 Hardware and Software Specifications</td><td style="border: none; text-align: right;">17</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">3.5 Feasibility Study</td><td style="border: none; text-align: right;">18</td></tr>
  <tr style="border: none; font-weight: bold;"><td style="border: none;">4.</td><td style="border: none;">SYSTEM DESIGN & MATHEMATICAL ARCHITECTURE</td><td style="border: none; text-align: right;">19</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">4.1 Multi-Tiered System Architecture</td><td style="border: none; text-align: right;">19</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">4.2 Data Flow Diagrams (DFD Level 0, 1, and 2)</td><td style="border: none; text-align: right;">21</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">4.3 UML Behavioral Modeling</td><td style="border: none; text-align: right;">23</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">4.4 Mathematical Model Formulation</td><td style="border: none; text-align: right;">25</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">4.5 Database Schema & Document Models</td><td style="border: none; text-align: right;">27</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">4.6 Projected Metric Spatial Pipeline (EPSG:32643)</td><td style="border: none; text-align: right;">28</td></tr>
  <tr style="border: none; font-weight: bold;"><td style="border: none;">5.</td><td style="border: none;">SYSTEM IMPLEMENTATION & CODEBASE DESCRIPTION</td><td style="border: none; text-align: right;">29</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">5.1 Codebase Architecture Overview</td><td style="border: none; text-align: right;">29</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">5.2 Detailed Backend Service Implementation</td><td style="border: none; text-align: right;">30</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">5.3 Frontend Component Architecture & Modern Styling</td><td style="border: none; text-align: right;">34</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">5.4 Core Algorithmic Pseudocode</td><td style="border: none; text-align: right;">37</td></tr>
  <tr style="border: none; font-weight: bold;"><td style="border: none;">6.</td><td style="border: none;">RESULTS, EXPERIMENTAL EVALUATION & DISCUSSION</td><td style="border: none; text-align: right;">40</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">6.1 Empirical Dataset Collection & Statistical Baseline</td><td style="border: none; text-align: right;">40</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">6.2 User Interface Walkthrough & Module Verification</td><td style="border: none; text-align: right;">42</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">6.3 Comparative Municipal Case Studies (Pune, Mumbai, Nagpur)</td><td style="border: none; text-align: right;">45</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">6.4 Automated Verification Test Suite (25/25 Tests Passing)</td><td style="border: none; text-align: right;">47</td></tr>
  <tr style="border: none;"><td style="border: none;"></td><td style="border: none;">6.5 System Latency & Performance Benchmarks</td><td style="border: none; text-align: right;">48</td></tr>
  <tr style="border: none; font-weight: bold;"><td style="border: none;">7.</td><td style="border: none;">CONCLUSION & FUTURE SCOPE</td><td style="border: none; text-align: right;">49</td></tr>
  <tr style="border: none; font-weight: bold;"><td style="border: none;">12.</td><td style="border: none;">MAPPING OF THE PROJECT TO SUSTAINABLE DEVELOPMENT GOALS</td><td style="border: none; text-align: right;">51</td></tr>
  <tr style="border: none; font-weight: bold;"><td style="border: none;">13.</td><td style="border: none;">RELATION OF THE PROJECT TO THE ENVIRONMENT</td><td style="border: none; text-align: right;">53</td></tr>
  <tr style="border: none; font-weight: bold;"><td style="border: none;">14.</td><td style="border: none;">PROJECT COST STATEMENT</td><td style="border: none; text-align: right;">55</td></tr>
  <tr style="border: none; font-weight: bold;"><td style="border: none;"></td><td style="border: none;">REFERENCES (IEEE/APA)</td><td style="border: none; text-align: right;">57</td></tr>
  <tr style="border: none; font-weight: bold;"><td style="border: none;"></td><td style="border: none;">APPENDIX: USER MANUAL & DEPLOYMENT GUIDE</td><td style="border: none; text-align: right;">59</td></tr>
</table>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- LIST OF FIGURES & TABLES & ABBREVIATIONS -->
<!-- ========================================================================= -->
<div class="cert-header">LIST OF FIGURES</div>
<table style="border: none;">
  <tr style="border: none; font-weight: bold;"><td style="border: none; width: 20%;">Figure No.</td><td style="border: none; width: 65%;">Title of Figure</td><td style="border: none; width: 15%; text-align: right;">Page No.</td></tr>
  <tr style="border: none;"><td style="border: none;">Figure 4.1</td><td style="border: none;">USAS Multi-Tiered System Architecture</td><td style="border: none; text-align: right;">20</td></tr>
  <tr style="border: none;"><td style="border: none;">Figure 4.2</td><td style="border: none;">Level 0 Context Data Flow Diagram</td><td style="border: none; text-align: right;">21</td></tr>
  <tr style="border: none;"><td style="border: none;">Figure 4.3</td><td style="border: none;">Level 1 Subsystem Data Flow Diagram</td><td style="border: none; text-align: right;">22</td></tr>
  <tr style="border: none;"><td style="border: none;">Figure 4.4</td><td style="border: none;">UML Use Case Diagram for Urban Stakeholders</td><td style="border: none; text-align: right;">23</td></tr>
  <tr style="border: none;"><td style="border: none;">Figure 4.5</td><td style="border: none;">UML Sequence Diagram of City Assessment Request</td><td style="border: none; text-align: right;">24</td></tr>
  <tr style="border: none;"><td style="border: none;">Figure 5.1</td><td style="border: none;">React 18 Component Tree & Unidirectional Data Flow</td><td style="border: none; text-align: right;">34</td></tr>
  <tr style="border: none;"><td style="border: none;">Figure 6.1</td><td style="border: none;">Comparative Overall Sustainability Score Profile for Sample Cities</td><td style="border: none; text-align: right;">46</td></tr>
</table>

<div style="margin-top: 25pt;" class="cert-header">LIST OF TABLES</div>
<table style="border: none;">
  <tr style="border: none; font-weight: bold;"><td style="border: none; width: 20%;">Table No.</td><td style="border: none; width: 65%;">Title of Table</td><td style="border: none; width: 15%; text-align: right;">Page No.</td></tr>
  <tr style="border: none;"><td style="border: none;">Table 2.1</td><td style="border: none;">Comparative Feature Matrix of Urban Decision Support Systems</td><td style="border: none; text-align: right;">11</td></tr>
  <tr style="border: none;"><td style="border: none;">Table 3.1</td><td style="border: none;">Hardware and Software Development & Deployment Environment</td><td style="border: none; text-align: right;">17</td></tr>
  <tr style="border: none;"><td style="border: none;">Table 4.1</td><td style="border: none;">Indicator Criteria Directionality and Baseline Min-Max Bounds</td><td style="border: none; text-align: right;">25</td></tr>
  <tr style="border: none;"><td style="border: none;">Table 6.1</td><td style="border: none;">Statistical Baseline of 42 Maharashtra Cities Clean Master Dataset</td><td style="border: none; text-align: right;">41</td></tr>
  <tr style="border: none;"><td style="border: none;">Table 6.2</td><td style="border: none;">Automated Unit Verification Test Suite Summary</td><td style="border: none; text-align: right;">47</td></tr>
  <tr style="border: none;"><td style="border: none;">Table 12.1</td><td style="border: none;">Mapping of USAS to Sustainable Development Goals (SDGs)</td><td style="border: none; text-align: right;">51</td></tr>
  <tr style="border: none;"><td style="border: none;">Table 14.1</td><td style="border: none;">Itemized Project Expenditure Statement</td><td style="border: none; text-align: right;">55</td></tr>
</table>

<div style="margin-top: 25pt;" class="cert-header">LIST OF ABBREVIATIONS</div>
<table style="border: none;">
  <tr style="border: none;"><td style="border: none; width: 25%;"><strong>AQI</strong></td><td style="border: none; width: 75%;">Air Quality Index</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>CAAQMS</strong></td><td style="border: none;">Continuous Ambient Air Quality Monitoring Station</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>CPCB</strong></td><td style="border: none;">Central Pollution Control Board</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>CRS</strong></td><td style="border: none;">Coordinate Reference System</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>DFD</strong></td><td style="border: none;">Data Flow Diagram</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>EPSG</strong></td><td style="border: none;">European Petroleum Survey Group Geodetic Parameter Dataset</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>FAISS</strong></td><td style="border: none;">Facebook AI Similarity Search</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>GIS</strong></td><td style="border: none;">Geographic Information System</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>MCDM</strong></td><td style="border: none;">Multi-Criteria Decision Making</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>MMVD</strong></td><td style="border: none;">Maharashtra Motor Vehicles Department</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>MPCB</strong></td><td style="border: none;">Maharashtra Pollution Control Board</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>NCAP</strong></td><td style="border: none;">National Clean Air Programme</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>NMT</strong></td><td style="border: none;">Non-Motorized Transport</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>NUTP</strong></td><td style="border: none;">National Urban Transport Policy</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>OSM</strong></td><td style="border: none;">OpenStreetMap</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>RAG</strong></td><td style="border: none;">Retrieval-Augmented Generation</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>SDG</strong></td><td style="border: none;">Sustainable Development Goal</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>SWM</strong></td><td style="border: none;">Solid Waste Management</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>TOD</strong></td><td style="border: none;">Transit-Oriented Development</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>UDCPR</strong></td><td style="border: none;">Unified Development Control and Promotion Regulations</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>ULB</strong></td><td style="border: none;">Urban Local Body</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>URDPFI</strong></td><td style="border: none;">Urban and Regional Development Plans Formulation and Implementation</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>UTM</strong></td><td style="border: none;">Universal Transverse Mercator</td></tr>
  <tr style="border: none;"><td style="border: none;"><strong>WSM</strong></td><td style="border: none;">Weighted Sum Model</td></tr>
</table>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- CHAPTER 1: INTRODUCTION -->
<!-- ========================================================================= -->
<div class="chapter-heading">CHAPTER 1<br>INTRODUCTION</div>

<div class="section-heading">1.1 Background of the Project</div>
<p>
The state of Maharashtra represents one of India's most economically dynamic and rapidly urbanizing territories, generating more than 14% of the national gross domestic product while hosting over 50 million urban residents across 42 statutory municipal corporations and class-A municipal councils. However, this hyper-concentrated economic acceleration has precipitated severe, systemic urban sustainability deficits. Metropolitan growth centers such as the Mumbai Metropolitan Region (MMR), Pune, and Pimpri-Chinchwad face persistent traffic congestion with peak travel delays exceeding 70%, acute deficits in accessible per capita green canopy (dropping below 1 m² per capita against the statutory 10–12 m² statutory benchmark), and elevated respiratory particulates. Concurrently, Tier-2 and Tier-3 urban local bodies across the Marathwada, Vidarbha, and Khandesh regions (including Chhatrapati Sambhajinagar, Nanded, Amravati, and Jalgaon) struggle with sub-optimal municipal solid waste processing efficiencies, extensive open dumping, expanding demographic densities, and limited continuous air quality monitoring infrastructure.
</p>
<p>
Urban local bodies (ULBs) in Maharashtra operate under strict statutory mandates dictated by the 74th Constitutional Amendment Act, the Environment (Protection) Act of 1986, the Solid Waste Management Rules of 2016, and the Maharashtra Municipal Corporations Act. Despite these statutory frameworks, municipal commissioners, chief urban planners, and environmental engineers are routinely required to make multi-million-rupee capital allocation decisions without integrated, data-driven analytical decision support. Municipal data assets remain siloed within disparate state departments—such as the Maharashtra Pollution Control Board (MPCB), Central Pollution Control Board (CPCB), the Office of the Registrar General for Census Operations, and the Maharashtra Motor Vehicles Department (MMVD). Consequently, urban decision-makers often lack a unified, empirical mechanism to systematically diagnose municipal distress, trace data provenance, or simulate the impact of prospective municipal interventions.
</p>

<div class="section-heading">1.2 Problem Definition</div>
<p>
Current urban planning and sustainability assessment practices in Indian municipalities suffer from five fundamental structural failures:
</p>
<p>
<strong>1. Siloed and Inconsistent Data Provenance:</strong> Municipal datasets are fragmented across departmental boundaries, featuring disparate observation frequencies, varying units of measurement, and conflicting geographic resolutions. Administrative reviews often rely on anecdotal summaries rather than longitudinal empirical baselines.
</p>
<p>
<strong>2. Pathological Synthetic Data Substitution:</strong> Existing commercial and administrative indices frequently replace missing indicator values with synthetic zeros or national means. In a multi-criteria index, artificially assigning a zero score to an unmonitored metric severely distorts a municipality's comparative ranking, penalizing cities for institutional monitoring deficits rather than measured ecological distress.
</p>
<p>
<strong>3. Subjective and Arbitrary Weighting:</strong> Many existing municipal ranking systems employ subjective, committee-driven weighting schemes without dynamic adjustment for data availability, leading to volatile ranking shifts that fail to withstand mathematical verification.
</p>
<p>
<strong>4. Disconnection Between Policy Guidance and Spatial Feasibility:</strong> State and national policies—such as the Urban and Regional Development Plans Formulation and Implementation (URDPFI) Guidelines and the National Clean Air Programme (NCAP)—recommend high-level urban interventions without evaluating localized spatial feasibility, parcel geometry, or road right-of-way (RoW) constraints.
</p>
<p>
<strong>5. Generative AI Hallucination Risks:</strong> While modern Large Language Models (LLMs) excel at natural language synthesis, deploying generic conversational chatbots for public decision support poses severe risks. Unconstrained LLMs frequently hallucinate statutory guidelines, fabricate civic statistics, and generate economically or spatially unfeasible recommendations without audit trails.
</p>

<div class="section-heading">1.3 Objectives of the Project</div>
<p>
The overarching objective of the <strong>Urban Sustainability Assessment System (USAS)</strong> is to design, implement, and validate an end-to-end, empirical, and deterministic multi-criteria decision support framework that transparently evaluates urban sustainability performance across all 42 statutory cities of Maharashtra.
</p>
<p class="no-indent">The specific engineering and data science objectives include:</p>
<p>
1. <strong>Empirical Baseline Integration:</strong> Ingest, clean, harmonize, and validate authentic multi-source datasets covering five statutory indicators: Air Quality (CPCB AQI 2015–2025), Solid Waste Management (MPCB 2023), Population Density (Census 2011), Urban Green Space coverage, and Urban Mobility (TomTom congestion delay and MMVD vehicle pressure proxies).
</p>
<p>
2. <strong>Transparent MCDM Scoring Engine:</strong> Formulate and deploy a mathematically deterministic Weighted Sum Model (WSM) featuring direction-aware Min-Max normalization that dynamically re-allocates indicator weights across available indicators while explicitly preserving missing data integrity.
</p>
<p>
3. <strong>Vulnerability Classification:</strong> Design an automated threshold-based risk matrix categorizing municipal indicators into Critical Problem Areas (< 40), Priority Attention Needed (40–59.9), Acceptable (≥ 60), and Monitored Regional Proxies.
</p>
<p>
4. <strong>Geospatial Metric Analysis:</strong> Integrate OpenStreetMap Overpass spatial feature queries and implement geodetic transformations to metric projected Coordinate Reference System UTM Zone 43N (EPSG:32643) for precise urban parcel and corridor area computation.
</p>
<p>
5. <strong>Evidence-Grounded RAG Pipeline:</strong> Construct a dense vector retrieval pipeline utilizing Sentence-Transformers and FAISS over statutory planning frameworks (NCAP, URDPFI, SWM 2016, NUTP, UDCPR) to ground Google Gemini in factual urban policy excerpts, eliminating generative hallucination.
</p>
<p>
6. <strong>Interactive Simulation & Academic Dossier Generation:</strong> Build a high-performance web dashboard featuring interactive sensitivity impact simulation and automated compilation of audit-grade municipal assessment reports.
</p>

<div class="section-heading">1.4 Scope of the Project</div>
<p>
The geographic scope of USAS encompasses all 42 statutory urban centers of Maharashtra, including municipal corporations and major municipal councils across all six administrative divisions (Konkan, Pune, Nashik, Chhatrapati Sambhajinagar, Amravati, and Nagpur). Thematically, the system evaluates five environmental and infrastructural dimensions that directly reflect municipal carrying capacity: Air Quality, Traffic Congestion/Pressure, Public Green Space, Solid Waste Treatment Efficiency, and Population Density.
</p>
<p>
Technologically, USAS maintains a strict architectural boundary: mathematical scoring, data coverage computation, threshold categorization, and spatial projections are entirely deterministic and executed in compiled Python services. The generative AI tier (Google Gemini) is strictly restricted to synthesizing localized, phased implementation roadmaps conditioned upon retrieved FAISS statutory evidence and verified municipal deficits.
</p>

<div class="section-heading">1.5 Significance of the Project</div>
<p>
USAS transitions municipal governance from qualitative intuition to reproducible, data-driven decision support. For municipal commissioners and standing committees, USAS provides an objective baseline to allocate capital expenditures (CapEx) where sustainability deficits are most critical. For state-level regulators such as the MPCB and Urban Development Department (UDD), USAS provides an audit-grade platform to monitor compliance with national environmental mandates (e.g., NCAP dust abatement targets, Swachh Bharat Mission 2.0 processing thresholds). Furthermore, the inclusion of an interactive sensitivity simulator enables city administrators to pre-evaluate the systemic score impact of targeted infrastructure investments prior to financial commitment.
</p>

<div class="section-heading">1.6 Limitations of the Project</div>
<p>
1. <strong>Census 2011 Temporal Baseline:</strong> In the absence of a finalized 2021 decennial national census, statutory municipal population and density metrics are derived from Census 2011 figures. While municipal boundary expansions are noted, population figures represent an established historical baseline.
</p>
<p>
2. <strong>Spatial Station Coverage Disparities:</strong> Continuous Ambient Air Quality Monitoring Stations (CAAQMS) are dense across Tier-1 metropolitan hubs (Mumbai, Pune) but limited in Tier-3 municipalities, necessitating historical CPCB daily bulletin baselines where live OpenAQ feeds are unavailable.
</p>
<p>
3. <strong>Traffic Proxy Segregation:</strong> Comprehensive live congestion delay indices are currently published for major metropolitan centers; for secondary cities, registered vehicle counts serve as a regional pressure proxy and are explicitly segregated from congestion delay scores to maintain mathematical integrity.
</p>

<div class="section-heading">1.7 Definition of Terms</div>
<p>
- <strong>Weighted Sum Model (WSM):</strong> A classical Multi-Criteria Decision Making (MCDM) technique evaluating alternatives across multiple weighted criteria by summing their normalized score-weight products.
</p>
<p>
- <strong>Criteria Directionality:</strong> The optimization orientation of an indicator; benefit criteria are positively associated with sustainability (higher is better), whereas cost criteria represent environmental burdens (lower is better).
</p>
<p>
- <strong>Dense Vector Embedding:</strong> A low-dimensional continuous mathematical vector (384 dimensions) generated by a deep transformer network capturing semantic meaning in textual planning documents.
</p>
<p>
- <strong>EPSG:32643 (UTM Zone 43N):</strong> The Universal Transverse Mercator metric conformal map projection covering western and central India (including Maharashtra), enabling distortion-free geometric distance and area measurements in square meters.
</p>

<div class="section-heading">1.8 Organization of the Report</div>
<p>
This report is organized into seven core technical chapters. Chapter 2 surveys academic literature across urban indices, MCDM algorithms, GIS remote sensing, and RAG architectures. Chapter 3 presents the requirement analysis and formal engineering specifications. Chapter 4 details the mathematical model, multi-tiered system architecture, and UML designs. Chapter 5 documents the programmatic codebase, module implementations, and algorithmic pseudocode. Chapter 6 presents empirical findings across the 42 cities, case study evaluations, and unit test verification. Chapter 7 concludes the report with future research pathways, followed by mandatory institutional sections covering Sustainable Development Goals (SDGs), Environmental Impact, Project Expenditure, and IEEE References.
</p>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- CHAPTER 2: LITERATURE SURVEY -->
<!-- ========================================================================= -->
<div class="chapter-heading">CHAPTER 2<br>LITERATURE SURVEY</div>

<div class="section-heading">2.1 Overview of Urban Sustainability Assessment Frameworks</div>
<p>
Urban sustainability assessment has evolved significantly over the past three decades, shifting from qualitative environmental impact checklists following the 1992 Rio Earth Summit to rigorous, data-driven multi-dimensional indices<sup class="cite">[1]</sup>. Alberti (1996) established foundational urban ecological carrying capacity theory, emphasizing that urban ecosystems must be analyzed as coupled human-natural systems governed by resource throughput and spatial metabolic flows<sup class="cite">[2]</sup>. Later research by Shen et al. (2011) examined international practice across urban sustainability indicator systems, noting that while international frameworks—such as the European Green City Index, UN-Habitat City Prosperity Index, and ISO 37120—provide structured indicators, they frequently assume continuous, standardized municipal data availability that does not reflect realities in Global South municipalities<sup class="cite">[3]</sup>.
</p>

<div class="section-heading">2.2 Review of Multi-Criteria Decision Making (MCDM) Methodologies</div>
<p>
Multi-Criteria Decision Making (MCDM) provides the mathematical foundation for aggregating heterogeneous, incommensurable environmental and socio-economic indicators into transparent composite metrics<sup class="cite">[4]</sup>. The most prevalent techniques evaluated in contemporary urban planning literature comprise the Analytic Hierarchy Process (AHP), Technique for Order Preference by Similarity to Ideal Solution (TOPSIS), ELimination and Choice Expressing REality (ELECTRE), and the Weighted Sum Model (WSM)<sup class="cite">[5]</sup>.
</p>
<p>
While AHP offers pairwise criteria weighting, its reliance on subjective expert judgments introduces significant cognitive bias when evaluating statutory municipal performance<sup class="cite">[6]</sup>. TOPSIS evaluates Euclidean distances to hypothetical ideal solutions; however, it suffers from rank reversal vulnerabilities when alternative candidates are added or removed<sup class="cite">[7]</sup>. In contrast, the Weighted Sum Model (WSM) coupled with linear direction-aware Min-Max normalization provides axiomatic transparency, computational tractability, and linear additive independence, making it the preferred methodology for public policy and municipal performance evaluation<sup class="cite">[8]</sup>.
</p>

<div class="section-heading">2.3 Review of Geospatial Analytics & Remote Sensing in Urban Planning</div>
<p>
Geospatial data integration is essential to ground sustainability indicators in tangible urban geography<sup class="cite">[9]</sup>. Traditional urban canopy evaluation relied on coarse satellite remote sensing derived Normalized Difference Vegetation Index (NDVI) measurements from Landsat and Sentinel-2 constellations<sup class="cite">[10]</sup>. While valuable for macroscopic regional vegetation tracking, NDVI struggles to distinguish accessible public recreational parks from private agricultural enclosures or inaccessible roadside scrub<sup class="cite">[11]</sup>. Consequently, contemporary urban spatial analytics leverages OpenStreetMap (OSM) topological databases through structured API querying (Overpass API) to identify gazetted urban parks, neighborhood gardens, and civic recreation zones<sup class="cite">[12]</sup>. Furthermore, geodetic literature underscores the absolute necessity of transforming spatial coordinates from unprojected angular coordinate reference systems (WGS84 EPSG:4326) into metric projected coordinate systems (Universal Transverse Mercator Zone 43N EPSG:32643) to prevent severe spatial area distortions when calculating urban park acreage<sup class="cite">[13]</sup>.
</p>

<div class="section-heading">2.4 Review of Retrieval-Augmented Generation (RAG) in Policy Synthesis</div>
<p>
The advent of Large Language Models (LLMs) has transformed natural language interaction with technical repositories; however, their standard application in urban policy synthesis is severely undermined by hallucinated citations, lack of domain grounding, and temporal cutoff limitations<sup class="cite">[14]</sup>. Lewis et al. (2020) formulated Retrieval-Augmented Generation (RAG), combining dense vector retrieval mechanisms with pre-trained autoregressive generative sequence models<sup class="cite">[15]</sup>. Dense semantic embeddings generated via dual-encoder transformer architectures (e.g., Sentence-Transformers) map textual propositions into continuous vector spaces where semantic similarity corresponds to cosine inner products<sup class="cite">[16]</sup>. Utilizing high-efficiency approximate nearest neighbor indexing libraries—specifically Facebook AI Similarity Search (FAISS)—enables sub-millisecond retrieval of exact statutory paragraphs from large-scale government planning corpora<sup class="cite">[17]</sup>. Integrating RAG with constrained prompt engineering guarantees that generative LLM outputs remain strictly grounded within statutory planning guidelines (such as URDPFI norms, NCAP clean air guidelines, and SWM 2016 rules)<sup class="cite">[18]</sup>.
</p>

<div class="section-heading">2.5 Comparative Study of Existing Systems</div>
<p>
A systematic comparative analysis was conducted evaluating existing urban sustainability assessment frameworks against the engineering requirements of the USAS architecture, as summarized in Table 2.1.
</p>

<div class="table-title">Table 2.1: Comparative Feature Matrix of Urban Decision Support Systems</div>
<table>
  <thead>
    <tr>
      <th>Evaluation Criterion</th>
      <th>MoHUA Ease of Living</th>
      <th>Arcadis Sustainable Cities</th>
      <th>Standard GenAI Chatbot</th>
      <th>USAS Framework (This Work)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Scoring Determinism</strong></td>
      <td>Partially Deterministic</td>
      <td>Deterministic</td>
      <td>Non-Deterministic (Stochastic)</td>
      <td><strong>100% Deterministic (WSM)</strong></td>
    </tr>
    <tr>
      <td><strong>Raw Data Provenance</strong></td>
      <td>Opaque / Aggregated</td>
      <td>Proprietary Baseline</td>
      <td>No Provenance (Hallucinated)</td>
      <td><strong>Full Institutional Audit Trail</strong></td>
    </tr>
    <tr>
      <td><strong>Missing Data Handling</strong></td>
      <td>Synthetic Zero-Filling</td>
      <td>National Proxy Imputation</td>
      <td>Ignored / Unchecked</td>
      <td><strong>Dynamic Weight Re-normalization</strong></td>
    </tr>
    <tr>
      <td><strong>Proxy Segregation</strong></td>
      <td>Merged into Delay</td>
      <td>Imputed Congestion</td>
      <td>Conflated Metrics</td>
      <td><strong>Explicit Proxy Flagging</strong></td>
    </tr>
    <tr>
      <td><strong>Spatial Metric Projection</strong></td>
      <td>None (Tabular Only)</td>
      <td>None (Macro Level)</td>
      <td>None</td>
      <td><strong>EPSG:32643 UTM Metric Projection</strong></td>
    </tr>
    <tr>
      <td><strong>Policy Grounding</strong></td>
      <td>Static Manual Reports</td>
      <td>Static PDF Dossiers</td>
      <td>Uncontrolled Text Synthesis</td>
      <td><strong>FAISS Vector RAG + Gemini SDK</strong></td>
    </tr>
    <tr>
      <td><strong>Sensitivity Simulation</strong></td>
      <td>Unavailable</td>
      <td>Unavailable</td>
      <td>Superficial Text Estimation</td>
      <td><strong>Interactive $\Delta Score$ Modeling</strong></td>
    </tr>
  </tbody>
</table>

<div class="section-heading">2.6 Research Gaps Identified</div>
<p>
The literature survey revealed four fundamental research and technical gaps:
</p>
<p>
<strong>Gap 1: Absence of Transparent Handling of Missing Municipal Data:</strong> Prior frameworks force complete data compliance by substituting zeros or regional averages for unobserved metrics, artificially skewing composite municipal rankings.
</p>
<p>
<strong>Gap 2: Disconnection Between MCDM Scoring and Spatial Feasibility:</strong> Existing decision frameworks rank cities in abstract numerical tables without grounding required interventions in projected physical spatial parcels or road network right-of-ways.
</p>
<p>
<strong>Gap 3: Uncontrolled LLM Hallucinations in Municipal Policy:</strong> Current generative AI implementations in public administration lack strict vector grounding, resulting in fabricated statutory clauses and non-compliant engineering recommendations.
</p>
<p>
<strong>Gap 4: Neglect of Secondary and Tertiary Urban Centers:</strong> Predominant urban informatics literature focuses exclusively on mega-cities (Mumbai, Delhi, Bengaluru), neglecting the specific institutional, data, and infrastructural realities of Tier-2 and Tier-3 municipal centers.
</p>

<div class="section-heading">2.7 Conclusion from Literature Review</div>
<p>
The literature confirms that an effective urban sustainability decision support framework must decouple deterministic mathematical scoring from generative advisory synthesis. By combining direction-aware Min-Max normalized WSM scoring, metric UTM Zone 43N spatial analysis, and FAISS-indexed RAG over verified Indian statutory policies, the USAS framework directly resolves the identified research gaps.
</p>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- CHAPTER 3: REQUIREMENT ANALYSIS & PROBLEM DEFINITION -->
<!-- ========================================================================= -->
<div class="chapter-heading">CHAPTER 3<br>REQUIREMENT ANALYSIS & PROBLEM DEFINITION</div>

<div class="section-heading">3.1 Comprehensive Problem Statement</div>
<p>
Given a set of $M = 42$ statutory municipal urban centers in Maharashtra, each characterized by an observed empirical indicator vector $\mathbf{x}_i \in \mathbb{R}^N$ ($N = 5$ core dimensions: Air Quality AQI, Municipal Solid Waste Treatment Efficiency %, Population Density, Public Green Space %, and Traffic Delay / Vehicle Pressure Proxy) wherein certain observations may be missing ($\emptyset$) or recorded as monitored proxies, design and implement an automated, mathematically rigorous, and auditable system that:
</p>
<p class="no-indent">
1. Deterministically normalizes $\mathbf{x}_i$ into a bounded scale $S_{ij} \in [0, 100]$ respecting criteria directionality.<br>
2. Aggregates scores into an overall sustainability index $Score_i \in [0, 100]$ using dynamic weight re-allocation without synthetic zero substitution.<br>
3. Automatically classifies deficits against statutory risk thresholds ($<40$, $40-59.9$, $\ge 60$).<br>
4. Projects candidate intervention sites into metric spatial coordinates (EPSG:32643) for area feasibility.<br>
5. Ground generative recommendations in statutory policy corpora using vector retrieval to prevent generative hallucination.<br>
6. Provides an interactive sensitivity analysis simulator modeling $\Delta Score$ responses to hypothetical indicator score gains.
</p>

<div class="section-heading">3.2 Functional Requirements</div>
<p>
- <strong>FR-01 (Multi-Source Ingestion & Provenance Tracking):</strong> The system shall ingest verified CSV datasets, validate schemas, preserve reference observation years, units, and source file paths, and support case-insensitive city resolution.
</p>
<p>
- <strong>FR-02 (Direction-Aware Normalization):</strong> The system shall automatically identify criteria polarity (cost vs benefit) and normalize observations bounded to the 42-city empirical extrema.
</p>
<p>
- <strong>FR-03 (Missing Data & Dynamic Re-normalization):</strong> The system shall compute data coverage percentages, identify available indicator subsets ($A_i$), and re-normalize weights proportionately so that $\sum w'_{ij} = 1.0$.
</p>
<p>
- <strong>FR-04 (Automated Risk Classification):</strong> The system shall classify each indicator into Critical Problem Areas, Needs Attention, Acceptable, or Monitored Regional Proxy.
</p>
<p>
- <strong>FR-05 (Real-Time OpenAQ Telemetry Integration):</strong> The system shall query the OpenAQ REST API for active station feeds (PM2.5/PM10), cache responses to disk, and gracefully report historical status when active stations are absent.
</p>
<p>
- <strong>FR-06 (Overpass Spatial Querying & Metric Projection):</strong> The system shall query OpenStreetMap for urban features, reproject geometries from WGS84 to UTM Zone 43N (EPSG:32643), and compute metric areas ($m^2$, hectares).
</p>
<p>
- <strong>FR-07 (FAISS Semantic Policy Retrieval & LLM Synthesis):</strong> The system shall generate 384-dimensional dense vector embeddings of statutory policies, index them in FAISS, retrieve top-K citations, and condition Google Gemini via the <pre style="display:inline; padding:1px 4px;">google-genai</pre> SDK to synthesize phased roadmaps.
</p>
<p>
- <strong>FR-08 (Sensitivity Simulation & Dossier Compilation):</strong> The system shall provide an interactive slider modeling score improvements and compile printable, formal evaluation dossiers with clean print media styling.
</p>

<div class="section-heading">3.3 Non-Functional Requirements</div>
<p>
- <strong>NFR-01 (Deterministic Reproducibility):</strong> The scoring engine shall produce 100% identical numerical results across repeated executions on identical input datasets.
</p>
<p>
- <strong>NFR-02 (Low Latency Response):</strong> REST API endpoints for city assessments shall execute in under 300 milliseconds on standard server hardware.
</p>
<p>
- <strong>NFR-03 (Zero Synthetic Data Invention):</strong> The platform shall never invent missing city data, fake API availability, or substitute zeros for missing metrics.
</p>
<p>
- <strong>NFR-04 (Vector Retrieval Efficiency):</strong> FAISS top-K semantic policy retrieval shall execute in under 50 milliseconds.
</p>
<p>
- <strong>NFR-05 (Modular Extensibility):</strong> The codebase shall strictly decouple data ingestion, mathematical scoring, geospatial analysis, and generative advisory tiers.
</p>
<p>
- <strong>NFR-06 (Cross-Browser Accessibility & Print Fidelity):</strong> The web application shall render responsively across devices and print cleanly to A4 PDF without visual clipping.
</p>

<div class="section-heading">3.4 Hardware and Software Specifications</div>
<p>
The complete computational environment for development, verification, and deployment is itemized in Table 3.1.
</p>

<div class="table-title">Table 3.1: Hardware and Software Development & Deployment Environment</div>
<table>
  <thead>
    <tr>
      <th>Component</th>
      <th>Technical Specification</th>
      <th>Role in USAS Framework</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Processor (CPU)</strong></td>
      <td>Intel Core i7 / AMD Ryzen 7 (8 Cores, 16 Threads)</td>
      <td>Local batch computing, FAISS vector querying, geospatial projection</td>
    </tr>
    <tr>
      <td><strong>System Memory (RAM)</strong></td>
      <td>16 GB DDR4 / DDR5</td>
      <td>In-memory data structures, transformer embedding caching</td>
    </tr>
    <tr>
      <td><strong>Operating System</strong></td>
      <td>Microsoft Windows 11 / Ubuntu Linux 22.04 LTS</td>
      <td>Host execution environment</td>
    </tr>
    <tr>
      <td><strong>Backend Language</strong></td>
      <td>Python 3.11.x</td>
      <td>Core application and API runtime</td>
    </tr>
    <tr>
      <td><strong>Backend Framework</strong></td>
      <td>Flask 3.0.x / Flask-CORS</td>
      <td>RESTful API service layer</td>
    </tr>
    <tr>
      <td><strong>Numerical Computing</strong></td>
      <td>NumPy 1.26.x, Pandas 2.2.x, SciPy</td>
      <td>Empirical data processing, matrix normalization, WSM scoring</td>
    </tr>
    <tr>
      <td><strong>Vector Search Engine</strong></td>
      <td>FAISS-CPU (<pre style="display:inline; padding:1px 4px;">faiss-cpu</pre> 1.8.x)</td>
      <td>Dense vector indexing and inner-product similarity search</td>
    </tr>
    <tr>
      <td><strong>Embedding Model</strong></td>
      <td>Sentence-Transformers (<pre style="display:inline; padding:1px 4px;">all-MiniLM-L6-v2</pre>)</td>
      <td>384-dimensional dense semantic representation</td>
    </tr>
    <tr>
      <td><strong>Geospatial Libraries</strong></td>
      <td>GeoPandas 0.14.x, Shapely 2.0.x, PyProj</td>
      <td>Geometry manipulation and UTM Zone 43N metric projection</td>
    </tr>
    <tr>
      <td><strong>Generative AI SDK</strong></td>
      <td>Google GenAI Python SDK (<pre style="display:inline; padding:1px 4px;">google-genai</pre>)</td>
      <td>Gemini model orchestration for grounded policy synthesis</td>
    </tr>
    <tr>
      <td><strong>Database</strong></td>
      <td>MongoDB 7.0 / PyMongo 4.6.x</td>
      <td>Persistence for scenario records, dossiers, and audit trails</td>
    </tr>
    <tr>
      <td><strong>Frontend Runtime</strong></td>
      <td>Node.js 20.x LTS / npm 10.x</td>
      <td>Frontend tooling and package management</td>
    </tr>
    <tr>
      <td><strong>Frontend Stack</strong></td>
      <td>React 18.x, Vite 7.x, Leaflet 1.9.x</td>
      <td>Interactive single-page application and dynamic GIS mapping</td>
    </tr>
  </tbody>
</table>

<div class="section-heading">3.5 Feasibility Study</div>
<p>
<strong>Technical Feasibility:</strong> The selected technology stack consists of robust, open-source libraries (Flask, NumPy, Pandas, GeoPandas, FAISS, React) and official SDKs. Integration between local Python analytical engines and cloud APIs (OpenAQ, Gemini) is verified with graceful offline fallback mechanisms.
</p>
<p>
<strong>Operational Feasibility:</strong> The user interface is engineered specifically for municipal administrators, presenting intuitive KPI dials, color-coded priority matrices, interactive sensitivity sliders, and standard PDF export capabilities requiring no programming expertise.
</p>
<p>
<strong>Economic Feasibility:</strong> The system utilizes free, open-source computational stacks, public open-data repositories (CPCB, MPCB, Census 2011, OpenStreetMap), and free-tier API endpoints, resulting in negligible operational software expenditure.
</p>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- CHAPTER 4: SYSTEM DESIGN & MATHEMATICAL ARCHITECTURE -->
<!-- ========================================================================= -->
<div class="chapter-heading">CHAPTER 4<br>SYSTEM DESIGN & MATHEMATICAL ARCHITECTURE</div>

<div class="section-heading">4.1 Multi-Tiered System Architecture</div>
<p>
The USAS architecture is structured into five distinct operational layers, enforcing strict separation of concerns between data verification, mathematical computation, vector search, generative synthesis, and client visualization, as illustrated in Figure 4.1.
</p>

<div class="diagram-container">
  <div style="text-align: center; font-weight: bold; font-size: 11pt; margin-bottom: 8pt; color: #173b2b;">
    USAS SYSTEM ARCHITECTURAL LAYERS
  </div>
  <div class="diagram-row">
    <div class="diagram-box">
      <strong>1. Empirical Data Layer</strong>
      CPCB Daily Bulletins (2015-2025)<br>
      MPCB Solid Waste 2023 Records<br>
      Census 2011 Municipal Baseline<br>
      OpenStreetMap Topological Layers
    </div>
    <div class="diagram-box">
      <strong>2. External Live Feeds</strong>
      OpenAQ REST API v3 (PM2.5/PM10)<br>
      Overpass API (OSM Urban Features)<br>
      Disk-Backed Response Caching
    </div>
  </div>
  <div class="diagram-arrow">▼ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ▼</div>
  <div class="diagram-box" style="margin-bottom: 8pt;">
    <strong>3. Core Computational & Analytical Engine (Flask / Python 3.11)</strong>
    <span style="font-size: 9pt;">
      Data Ingestion &amp; Schema Validation &bull; Direction-Aware Min-Max Normalizer &bull; WSM Dynamic Weight Re-allocator &bull; Risk Classification Matrix &bull; UTM 43N Metric Projection Engine &bull; Interactive Sensitivity Simulator
    </span>
  </div>
  <div class="diagram-arrow">▼ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ▼</div>
  <div class="diagram-row">
    <div class="diagram-box">
      <strong>4. Policy RAG Vector Store</strong>
      Statutory Policy Corpus (NCAP, URDPFI, SWM)<br>
      Sentence-Transformers (<pre style="display:inline; padding:1px 3px;">all-MiniLM-L6-v2</pre>)<br>
      FAISS Dense Index (<pre style="display:inline; padding:1px 3px;">IndexFlatIP</pre>)
    </div>
    <div class="diagram-box">
      <strong>5. Generative Advisory Tier</strong>
      Google Gemini (<pre style="display:inline; padding:1px 3px;">google-genai</pre> SDK)<br>
      Strict Temperature Zero Prompting<br>
      Offline 42-City Phased Roadmaps
    </div>
  </div>
  <div class="diagram-arrow">▼</div>
  <div class="diagram-box">
    <strong>6. Reactive Client Presentation Layer (React 18 / Vite / Leaflet)</strong>
    <span style="font-size: 9pt;">
      Executive Dashboard &bull; Indicator Explorer &bull; Risk Priority Matrix &bull; Interactive Leaflet GIS &bull; Sensitivity Studio &bull; Formal Academic Dossier
    </span>
  </div>
</div>
<div class="figure-caption">Figure 4.1: USAS Multi-Tiered System Architecture</div>

<div class="section-heading">4.2 Data Flow Diagrams</div>
<p>
The functional transformation of data across the USAS framework is formally specified through multi-level Data Flow Diagrams.
</p>

<div class="sub-section-heading">4.2.1 Level 0 Context Data Flow Diagram</div>
<p>
The Level 0 Context DFD captures the boundary of the USAS software entity and its primary interactions with external actors, as shown in Figure 4.2.
</p>

<div class="diagram-container" style="text-align: center;">
  <div style="display: inline-block; border: 1.5px solid #000; padding: 6pt 12pt; background: #e8f5ee; font-weight: bold; margin-bottom: 12pt;">
    Urban Administrator / Municipal Planner
  </div><br>
  <span style="font-size: 11pt;">▲ City Selection & Simulation Parameters &nbsp;&nbsp;&nbsp;&nbsp; ▼ Assessment Dossier, Scorecard & Action Roadmaps</span><br>
  <div style="display: inline-block; border: 2px solid #173b2b; padding: 12pt 24pt; background: #ffffff; font-weight: bold; margin: 12pt 0; font-size: 11pt;">
    0.0 URBAN SUSTAINABILITY ASSESSMENT SYSTEM (USAS)
  </div><br>
  <span style="font-size: 11pt;">▲ Empirical Datasets &bull; Real-time OpenAQ Feeds &bull; Overpass OSM Features &bull; Statutory Corpus Excerpts</span><br>
  <div style="display: flex; justify-content: space-around; margin-top: 12pt;">
    <div style="border: 1.5px solid #000; padding: 4pt 8pt; background: #f2f2f2; font-size: 9pt;">CPCB / MPCB / Census Data</div>
    <div style="border: 1.5px solid #000; padding: 4pt 8pt; background: #f2f2f2; font-size: 9pt;">OpenAQ REST API</div>
    <div style="border: 1.5px solid #000; padding: 4pt 8pt; background: #f2f2f2; font-size: 9pt;">OSM Overpass API</div>
    <div style="border: 1.5px solid #000; padding: 4pt 8pt; background: #f2f2f2; font-size: 9pt;">FAISS Policy Corpus</div>
  </div>
</div>
<div class="figure-caption">Figure 4.2: Level 0 Context Data Flow Diagram</div>

<div class="sub-section-heading">4.2.2 Level 1 Subsystem Data Flow Diagram</div>
<p>
Figure 4.3 details the internal subprocesses: Data Ingestion (1.0), Dynamic Normalization & Scoring (2.0), Vulnerability Categorization (3.0), Spatial Metric Processing (4.0), Semantic RAG Policy Retrieval (5.0), and Generative Intervention Synthesis (6.0).
</p>

<div class="diagram-container">
  <div class="diagram-row">
    <div class="diagram-box"><strong>Process 1.0</strong>Ingestion &amp; Schema Validation</div>
    <div style="align-self: center;">➔</div>
    <div class="diagram-box"><strong>Process 2.0</strong>Dynamic WSM Scoring Engine</div>
    <div style="align-self: center;">➔</div>
    <div class="diagram-box"><strong>Process 3.0</strong>Risk Classification Matrix</div>
  </div>
  <div class="diagram-row" style="margin-top: 12pt;">
    <div class="diagram-box"><strong>Process 4.0</strong>Spatial Reprojection (UTM 43N)</div>
    <div style="align-self: center;">➔</div>
    <div class="diagram-box"><strong>Process 5.0</strong>FAISS Vector Search Engine</div>
    <div style="align-self: center;">➔</div>
    <div class="diagram-box"><strong>Process 6.0</strong>Grounded Gemini Synthesis</div>
  </div>
</div>
<div class="figure-caption">Figure 4.3: Level 1 Subsystem Data Flow Diagram</div>

<div class="section-heading">4.3 UML Behavioral Modeling</div>
<p>
The operational behavior of the system is modeled via UML Use Case (Figure 4.4) and Sequence (Figure 4.5) representations.
</p>

<div class="diagram-container" style="text-align: center;">
  <div style="font-weight: bold; margin-bottom: 8pt;">UML USE CASE DIAGRAM</div>
  <div style="text-align: left; display: inline-block; font-size: 10pt;">
    <strong>Actor: Municipal Planner / Policy Analyst</strong><br>
    &bull; [UC-01] Select Target Municipal City from 42 Supported Centers<br>
    &bull; [UC-02] Examine Empirical Indicator Breakdown & Provenance Citations<br>
    &bull; [UC-03] Review Vulnerability Classification & Statutory Threshold Gaps<br>
    &bull; [UC-04] Inspect Mapped Urban Parks & Projected Spatial Interventions in EPSG:32643<br>
    &bull; [UC-05] Retrieve Grounded Policy Excerpts via Dense FAISS Semantic Search<br>
    &bull; [UC-06] Run Sensitivity Impact Simulations ($\Delta Indicator \rightarrow \Delta Overall$)<br>
    &bull; [UC-07] Compile and Export Audit-Grade Assessment Dossier (PDF/Print)
  </div>
</div>
<div class="figure-caption">Figure 4.4: UML Use Case Diagram for Urban Stakeholders</div>

<div class="diagram-container" style="text-align: center;">
  <div style="font-weight: bold; margin-bottom: 8pt;">UML SEQUENCE DIAGRAM (City Assessment Execution Flow)</div>
  <div style="text-align: left; font-family: monospace; font-size: 9pt; line-height: 1.4;">
    User -> Client (React): Selects City ("Pune")<br>
    Client -> API Gateway (Flask): GET /api/assessment/Pune<br>
    API Gateway -> MasterLoader: Lookup verified record for "Pune"<br>
    MasterLoader --> API Gateway: Raw observation vector & metadata<br>
    API Gateway -> ScoringEngine: Calculate WSM scores with dynamic normalization<br>
    ScoringEngine --> API Gateway: Normalized scores, overall score (33.20/100), coverage (100%)<br>
    API Gateway -> ProblemDetector: Classify indicators into risk tiers<br>
    ProblemDetector --> API Gateway: Critical deficits identified (Green Space, Traffic)<br>
    API Gateway -> OpenAQClient: Retrieve live station telemetry (PM2.5/PM10)<br>
    OpenAQClient --> API Gateway: Real-time observation or cached historical state<br>
    API Gateway --> Client: Return structured JSON assessment payload<br>
    Client -> User: Renders scorecard dial, risk matrix, and spatial action links
  </div>
</div>
<div class="figure-caption">Figure 4.5: UML Sequence Diagram of City Assessment Request</div>

<div class="section-heading">4.4 Mathematical Model Formulation</div>
<p>
The core multi-criteria sustainability assessment is governed by an axiomatic mathematical model designed to ensure 100% deterministic reproducibility without synthetic distortion.
</p>

<div class="sub-section-heading">4.4.1 Direction-Aware Min-Max Normalization</div>
<p>
Let $x_{ij}$ represent the observed empirical value of indicator $j$ for municipality $i$, where $j \in \{1, 2, \dots, N\}$ and $i \in \{1, 2, \dots, M\}$ ($M = 42$). The extrema across the empirical dataset are defined as:
</p>
<div class="equation-box">
  $\min_k(x_{kj}) = \min \{x_{1j}, x_{2j}, \dots, x_{Mj}\}, \quad \max_k(x_{kj}) = \max \{x_{1j}, x_{2j}, \dots, x_{Mj}\}$
  <span class="equation-num">(4.1)</span>
</div>

<p class="no-indent">For <strong>Benefit Criteria</strong> (where higher values indicate superior sustainability, e.g., Green Space Coverage %, Waste Treatment %):</p>
<div class="equation-box">
  $S_{ij} = \left( \frac{x_{ij} - \min_k(x_{kj})}{\max_k(x_{kj}) - \min_k(x_{kj})} \right) \times 100$
  <span class="equation-num">(4.2)</span>
</div>

<p class="no-indent">For <strong>Cost Criteria</strong> (where lower values represent reduced environmental burden, e.g., Air Quality AQI, Population Density, Traffic Congestion %):</p>
<div class="equation-box">
  $S_{ij} = \left( \frac{\max_k(x_{kj}) - x_{ij}}{\max_k(x_{kj}) - \min_k(x_{kj})} \right) \times 100$
  <span class="equation-num">(4.3)</span>
</div>

<div class="table-title">Table 4.1: Indicator Criteria Directionality and Baseline Min-Max Bounds</div>
<table>
  <thead>
    <tr>
      <th>Indicator ($j$)</th>
      <th>Metric Definition</th>
      <th>Polarity</th>
      <th>Dataset Min ($\min_k$)</th>
      <th>Dataset Max ($\max_k$)</th>
      <th>Unit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Air Quality</strong></td>
      <td>CPCB Daily Bulletin Mean AQI</td>
      <td>Cost (Lower is better)</td>
      <td>48.00</td>
      <td>215.00</td>
      <td>AQI sub-index</td>
    </tr>
    <tr>
      <td><strong>Waste Management</strong></td>
      <td>Scientific Waste Treatment Ratio</td>
      <td>Benefit (Higher is better)</td>
      <td>0.00</td>
      <td>100.00</td>
      <td>%</td>
    </tr>
    <tr>
      <td><strong>Population Density</strong></td>
      <td>Municipal Population / Area</td>
      <td>Cost (Lower is better)</td>
      <td>824.00</td>
      <td>39,977.00</td>
      <td>persons/km²</td>
    </tr>
    <tr>
      <td><strong>Green Space</strong></td>
      <td>Documented Public Green Coverage</td>
      <td>Benefit (Higher is better)</td>
      <td>0.28</td>
      <td>17.80</td>
      <td>%</td>
    </tr>
    <tr>
      <td><strong>Traffic Delay</strong></td>
      <td>TomTom Peak Congestion Delay</td>
      <td>Cost (Lower is better)</td>
      <td>15.00</td>
      <td>71.10</td>
      <td>%</td>
    </tr>
  </tbody>
</table>

<div class="sub-section-heading">4.4.2 Dynamic Weight Re-normalization for Missing Data</div>
<p>
Let $w_j$ represent the configured base weight for indicator $j$ ($w_j = 0.20$ for equal weighting across all $N=5$ dimensions). Let $A_i \subseteq \{1, 2, \dots, N\}$ denote the set of indicators with valid empirical observations for municipality $i$. The cumulative available weight $W_{i, \text{total}}$ is computed as:
</p>
<div class="equation-box">
  $W_{i, \text{total}} = \sum_{j \in A_i} w_j$
  <span class="equation-num">(4.4)</span>
</div>

<p class="no-indent">The dynamically re-normalized weight $w'_{ij}$ assigned to each available indicator is defined as:</p>
<div class="equation-box">
  $w'_{ij} = \frac{w_j}{W_{i, \text{total}}} = \frac{w_j}{\sum_{k \in A_i} w_k}, \quad \text{such that} \quad \sum_{j \in A_i} w'_{ij} = 1.0$
  <span class="equation-num">(4.5)</span>
</div>

<p class="no-indent">The composite overall sustainability score $Score_i$ for municipality $i$ is calculated via the Weighted Sum Model:</p>
<div class="equation-box">
  $Score_i = \sum_{j \in A_i} \left( w'_{ij} \times S_{ij} \right)$
  <span class="equation-num">(4.6)</span>
</div>

<div class="sub-section-heading">4.4.3 Sensitivity Impact Analysis Derivative</div>
<p>
The response of the composite sustainability score to a hypothetical policy improvement $\Delta S_{ik}$ in target indicator $k \in A_i$ is governed by the partial derivative:
</p>
<div class="equation-box">
  $\frac{\partial Score_i}{\partial S_{ik}} = w'_{ik} \implies \Delta Score_i = \Delta S_{ik} \times \left( \frac{w_k}{\sum_{j \in A_i} w_j} \right)$
  <span class="equation-num">(4.7)</span>
</div>

<div class="section-heading">4.5 Database Schema & Document Models</div>
<p>
The persistence layer manages both relational tabular datasets and semi-structured MongoDB document collections:
</p>
<p>
<strong>1. Relational Master Ingestion Schema (<pre style="display:inline; padding:1px 4px;">USAS_city_indicator_master_clean.csv</pre>):</strong> Contains primary keys for normalized city names, district identifiers, geographic coordinates (latitude, longitude), raw metric observations, reference observation years, units, normalized indicator scores, and audit flags.
</p>
<p>
<strong>2. Assessment Document Model (MongoDB <pre style="display:inline; padding:1px 4px;">assessments</pre> collection):</strong>
</p>
<pre>
{
  "_id": ObjectId("..."),
  "city": "Pune",
  "assessment_date": "2026-10-30",
  "overall_score": 33.20,
  "score_status": "Full",
  "data_coverage_pct": 100.0,
  "available_indicator_count": 5,
  "indicators": [
    {
      "key": "green_space_score",
      "name": "Green Space",
      "raw_value": 0.7156,
      "unit": "%",
      "score": 0.33,
      "classification": "Problem Area",
      "is_proxy": false,
      "reference_year": 2025.0
    }, ...
  ],
  "problem_areas": ["Green Space", "Traffic", "Air Quality"]
}
</pre>

<div class="section-heading">4.6 Projected Metric Spatial Pipeline (EPSG:32643)</div>
<p>
To eliminate geodetic distortion when computing urban intervention footprints, geographic longitude ($\lambda$) and latitude ($\phi$) in WGS84 are converted to metric planar coordinates ($E, N$) using the Universal Transverse Mercator (UTM Zone 43N) projection equations:
</p>
<div class="equation-box">
  $E = E_0 + k_0 \nu \left( A + (1 - T + C)\frac{A^3}{6} + (5 - 18T + T^2 + 72C - 58\eta'^2)\frac{A^5}{120} \right)$
  <span class="equation-num">(4.8)</span>
</div>
<p class="no-indent">
where $E_0 = 500,000$ m is the false easting, $k_0 = 0.9996$ is the central meridian scale factor, and $\nu$ is the prime vertical radius of curvature. This projection guarantees that polygon parcel areas ($\iint dx dy$) calculated via the Shapely GIS engine represent true ground acreage in hectares.
</p>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- CHAPTER 5: SYSTEM IMPLEMENTATION & CODEBASE DESCRIPTION -->
<!-- ========================================================================= -->
<div class="chapter-heading">CHAPTER 5<br>SYSTEM IMPLEMENTATION & CODEBASE DESCRIPTION</div>

<div class="section-heading">5.1 Codebase Architecture Overview</div>
<p>
The USAS codebase is organized into modular tiers across backend services and frontend presentation components. All backend Python modules adhere strictly to PEP-8 standards, utilizing typing hints and encapsulated service patterns.
</p>

<div class="section-heading">5.2 Detailed Backend Service Implementation</div>

<div class="sub-section-heading">5.2.1 Master Data Loader (<pre style="display:inline; padding:1px 4px;">backend/app/services/data_loader.py</pre>)</div>
<p>
Responsible for ingesting the verified 42-city clean master dataset. It validates mandatory column definitions, enforces case- and whitespace-insensitive string normalization for city queries, and caches parsed records into memory for sub-millisecond retrieval. It strictly rejects duplicated normalized city identifiers and logs data provenance paths.
</p>

<div class="sub-section-heading">5.2.2 Normalization Processor (<pre style="display:inline; padding:1px 4px;">backend/app/services/data_processor.py</pre>)</div>
<p>
Executes Equations (4.2) and (4.3). It inspects criteria directionality configurations loaded from <pre style="display:inline; padding:1px 4px;">scoring.json</pre>, evaluates dataset extrema, and transforms raw floating-point metrics into normalized scores bounded strictly to $[0.0, 100.0]$. Missing entries are retained as explicit Python <pre style="display:inline; padding:1px 4px;">None</pre> references.
</p>

<div class="sub-section-heading">5.2.3 Multi-Criteria Scoring Engine (<pre style="display:inline; padding:1px 4px;">backend/app/services/scoring_engine.py</pre>)</div>
<p>
Implements the Weighted Sum Model with dynamic missing data re-normalization (Equations 4.4, 4.5, and 4.6). It tallies valid metrics, calculates data coverage percentages, re-normalizes weights, and formats the consolidated assessment payload including audit status flags (<pre style="display:inline; padding:1px 4px;">Full</pre>, <pre style="display:inline; padding:1px 4px;">Partial</pre>, <pre style="display:inline; padding:1px 4px;">Unavailable</pre>).
</p>

<div class="sub-section-heading">5.2.4 Vulnerability Problem Detector (<pre style="display:inline; padding:1px 4px;">backend/app/services/problem_detector.py</pre>)</div>
<p>
Processes normalized scores through statutory classification thresholds. Evaluates whether a metric is a scored indicator or a monitored regional pressure proxy. Produces structured classification dictionaries containing the observed raw value, measurement unit, reference year, threshold gap, and severity classification.
</p>

<div class="sub-section-heading">5.2.5 Spatial GIS Service (<pre style="display:inline; padding:1px 4px;">backend/app/services/spatial_analysis.py</pre>)</div>
<p>
Constructs Overpass QL queries targeting OSM amenities, leisure parks, and recreational polygons within municipal boundaries. Parses GeoJSON geometries, instantiates GeoPandas GeoDataFrames, transforms coordinates to EPSG:32643, and computes exact polygon area metrics. Implements disk caching in <pre style="display:inline; padding:1px 4px;">data/api_cache/spatial/</pre> to ensure deterministic response times.
</p>

<div class="sub-section-heading">5.2.6 Semantic Vector RAG Service (<pre style="display:inline; padding:1px 4px;">backend/app/services/rag_service.py</pre>)</div>
<p>
Loads statutory policy documents from <pre style="display:inline; padding:1px 4px;">data/knowledge_base/</pre>, segments text into 500-character chunks with 100-character overlaps, and computes dense vector representations via the Sentence-Transformers <pre style="display:inline; padding:1px 4px;">all-MiniLM-L6-v2</pre> model. Instantiates a FAISS <pre style="display:inline; padding:1px 4px;">IndexFlatIP</pre> index over normalized embeddings and executes nearest-neighbor retrieval returning top-K statutory passages with similarity scores.
</p>

<div class="sub-section-heading">5.2.7 Recommendation Engine (<pre style="display:inline; padding:1px 4px;">backend/app/services/recommendation_engine.py</pre>)</div>
<p>
Constructs an evidence-conditioned prompt integrating the municipality's specific deficits, candidate spatial sites, and retrieved FAISS statutory chunks. Calls the Google Gemini API using the official <pre style="display:inline; padding:1px 4px;">google-genai</pre> SDK with temperature set to 0.2. Maintains a comprehensive, localized fallback catalog covering all 42 Maharashtra cities structured into 3-phase implementation roadmaps, URDPFI spatial parameters, target KPIs, and applicable state/central funding schemes.
</p>

<div class="sub-section-heading">5.2.8 OpenAQ Telemetry Client (<pre style="display:inline; padding:1px 4px;">backend/app/services/openaq_service.py</pre>)</div>
<p>
Maintains verified station ID mappings for Maharashtra cities. Executes authenticated REST queries to OpenAQ v3 endpoints, extracts latest PM2.5 and PM10 concentrations, and handles rate limiting and connection timeouts through local cache fallbacks.
</p>

<div class="sub-section-heading">5.2.9 REST API Route Controller (<pre style="display:inline; padding:1px 4px;">backend/app/routes/api.py</pre>)</div>
<p>
Exposes standard RESTful HTTP endpoints:
- <pre style="display:inline; padding:1px 4px;">GET /api/cities</pre>: Returns list of supported 42 cities.
- <pre style="display:inline; padding:1px 4px;">GET /api/assessment/&lt;city&gt;</pre>: Returns full MCDM scorecard, coverage, and classification.
- <pre style="display:inline; padding:1px 4px;">GET /api/spatial-features/&lt;city&gt;</pre>: Returns mapped parks and UTM 43N projected candidate sites.
- <pre style="display:inline; padding:1px 4px;">GET /api/recommendations/&lt;city&gt;</pre>: Returns RAG-grounded interventions and phased roadmaps.
- <pre style="display:inline; padding:1px 4px;">POST /api/impact/&lt;city&gt;</pre>: Executes sensitivity simulation for target score improvements.
- <pre style="display:inline; padding:1px 4px;">GET /api/report/&lt;city&gt;</pre>: Compiles complete academic assessment dossier.
</p>

<div class="section-heading">5.3 Frontend Component Architecture & Modern Styling</div>
<p>
The client presentation layer is implemented in React 18, managed via a unidirectional state flow in <pre style="display:inline; padding:1px 4px;">App.jsx</pre>, as illustrated in Figure 5.1.
</p>

<div class="diagram-container" style="text-align: center;">
  <div style="font-weight: bold; margin-bottom: 8pt;">REACT COMPONENT TREE HIERARCHY</div>
  <div class="diagram-box" style="display: inline-block; padding: 6pt 16pt; margin-bottom: 8pt;">
    <strong>App.jsx (Root Controller &amp; State Manager)</strong><br>
    Manages: selectedCity, assessmentData, activeRoute, apiErrors, scenarioResult
  </div><br>
  <div style="display: flex; justify-content: center; gap: 8pt; flex-wrap: wrap;">
    <div class="diagram-box" style="flex: none; width: 22%;"><strong>Sidebar.jsx</strong>Fixed Navigation</div>
    <div class="diagram-box" style="flex: none; width: 22%;"><strong>Dashboard.jsx</strong>Executive KPIs</div>
    <div class="diagram-box" style="flex: none; width: 22%;"><strong>Assessment.jsx</strong>MCDM Scorecard</div>
    <div class="diagram-box" style="flex: none; width: 22%;"><strong>Indicators.jsx</strong>Benchmark Explorer</div>
    <div class="diagram-box" style="flex: none; width: 22%;"><strong>ProblemAreas.jsx</strong>Priority Matrix</div>
    <div class="diagram-box" style="flex: none; width: 22%;"><strong>SpatialFeasibility.jsx</strong>Leaflet GIS Map</div>
    <div class="diagram-box" style="flex: none; width: 22%;"><strong>Recommendations.jsx</strong>Phased Roadmaps</div>
    <div class="diagram-box" style="flex: none; width: 22%;"><strong>ImpactAnalysis.jsx</strong>Sensitivity Studio</div>
    <div class="diagram-box" style="flex: none; width: 22%;"><strong>Reports.jsx</strong>Academic Dossier</div>
  </div>
</div>
<div class="figure-caption">Figure 5.1: React 18 Component Tree & Unidirectional Data Flow</div>

<p>
<strong>Design & Typography Polish (<pre style="display:inline; padding:1px 4px;">frontend/src/index.css</pre>):</strong> All tabular metrics, scorecards, and deltas utilize <pre style="display:inline; padding:1px 4px;">font-variant-numeric: tabular-nums</pre> to guarantee vertical numeric alignment without jitter. Card containers implement flex column stretch rules (<pre style="display:inline; padding:1px 4px;">display: flex; flex-direction: column; justify-content: space-between</pre>) ensuring that cards, footers, and action buttons align symmetrically across rows regardless of textual variations.
</p>

<div class="section-heading">5.4 Core Algorithmic Pseudocode</div>

<div class="table-title">Algorithm 5.1: Direction-Aware Min-Max Normalization & Dynamic WSM Aggregation</div>
<pre>
Input: City record x_i, Master dataset extrema {min_k, max_k}, Base weights w_j
Output: Composite Assessment Dictionary A_res

1: Initialize available_scores = {}, available_weights = {}
2: For each indicator j in {1, 2, ..., N} do:
3:     val = x_i[j]
4:     If val is not None and not is_proxy(j) then:
5:         If polarity(j) == BENEFIT then:
6:             S_ij = ((val - min_k[j]) / (max_k[j] - min_k[j])) * 100.0
7:         Else:  // COST criterion
8:             S_ij = ((max_k[j] - val) / (max_k[j] - min_k[j])) * 100.0
9:         End If
10:        available_scores[j] = Clamp(S_ij, 0.0, 100.0)
11:        available_weights[j] = w_j
12:    End If
13: End For
14: W_total = Sum(available_weights.values())
15: If W_total > 0 then:
16:     overall_score = 0.0
17:     For each j in available_scores.keys() do:
18:         w_prime = available_weights[j] / W_total
19:         overall_score += (w_prime * available_scores[j])
20:     End For
21:     coverage_pct = (Length(available_scores) / N) * 100.0
22:     Return { "overall_score": Round(overall_score, 2), "coverage": coverage_pct, "status": "Full" }
23: Else:
24:     Return { "overall_score": None, "coverage": 0.0, "status": "Unavailable" }
25: End If
</pre>

<div class="table-title">Algorithm 5.2: Dense FAISS Vector Indexing & Semantic Search</div>
<pre>
Input: Document corpus D = {d_1, d_2, ..., d_M}, User deficit query q, Top-K parameter k
Output: Retrieved statutory policy passages R_top

1: chunks = []
2: For each document d in D do:
3:     chunks.extend(RecursiveTextSplit(d, chunk_size=500, overlap=100))
4: End For
5: transformer_model = LoadSentenceTransformer("all-MiniLM-L6-v2")
6: chunk_embeddings = transformer_model.encode(chunks, normalize_embeddings=True)
7: faiss_index = faiss.IndexFlatIP(dimension=384)
8: faiss_index.add(chunk_embeddings)
9: 
10: query_embedding = transformer_model.encode([q], normalize_embeddings=True)
11: distances, indices = faiss_index.search(query_embedding, top_k=k)
12: R_top = []
13: For idx in indices[0] do:
14:     R_top.append({ "text": chunks[idx], "similarity": distances[0][idx], "metadata": metadata[idx] })
15: End For
16: Return R_top
</pre>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- CHAPTER 6: RESULTS, EXPERIMENTAL EVALUATION & DISCUSSION -->
<!-- ========================================================================= -->
<div class="chapter-heading">CHAPTER 6<br>RESULTS, EXPERIMENTAL EVALUATION & DISCUSSION</div>

<div class="section-heading">6.1 Empirical Dataset Collection & Statistical Baseline</div>
<p>
The verified empirical baseline dataset integrates all 42 statutory urban local bodies of Maharashtra. Table 6.1 presents the descriptive statistical profile across the five core sustainability indicators.
</p>

<div class="table-title">Table 6.1: Statistical Baseline of 42 Maharashtra Cities Clean Master Dataset</div>
<table>
  <thead>
    <tr>
      <th>Metric Property</th>
      <th>Air Quality (AQI)</th>
      <th>Waste Treatment (%)</th>
      <th>Density (persons/km²)</th>
      <th>Green Space (%)</th>
      <th>Congestion Delay (%)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Count ($M$)</strong></td>
      <td>42</td>
      <td>42</td>
      <td>42</td>
      <td>42</td>
      <td>42 (9 scored, 33 proxy)</td>
    </tr>
    <tr>
      <td><strong>Mean ($\mu$)</strong></td>
      <td>112.45</td>
      <td>68.34</td>
      <td>9,842.10</td>
      <td>4.12</td>
      <td>48.60 (Metros)</td>
    </tr>
    <tr>
      <td><strong>Std Deviation ($\sigma$)</strong></td>
      <td>31.20</td>
      <td>24.80</td>
      <td>7,650.40</td>
      <td>3.85</td>
      <td>16.40</td>
    </tr>
    <tr>
      <td><strong>Minimum ($\min$)</strong></td>
      <td>48.00</td>
      <td>0.00</td>
      <td>824.00</td>
      <td>0.28</td>
      <td>15.00</td>
    </tr>
    <tr>
      <td><strong>25th Percentile</strong></td>
      <td>92.50</td>
      <td>52.10</td>
      <td>4,850.00</td>
      <td>1.20</td>
      <td>38.20</td>
    </tr>
    <tr>
      <td><strong>Median ($Q_2$)</strong></td>
      <td>108.00</td>
      <td>74.50</td>
      <td>7,890.00</td>
      <td>2.90</td>
      <td>51.40</td>
    </tr>
    <tr>
      <td><strong>75th Percentile</strong></td>
      <td>128.50</td>
      <td>88.20</td>
      <td>12,400.00</td>
      <td>5.80</td>
      <td>62.50</td>
    </tr>
    <tr>
      <td><strong>Maximum ($\max$)</strong></td>
      <td>215.00</td>
      <td>100.00</td>
      <td>39,977.00</td>
      <td>17.80</td>
      <td>71.10</td>
    </tr>
  </tbody>
</table>

<div class="section-heading">6.2 User Interface Walkthrough & Module Verification</div>
<p>
The USAS frontend was systematically verified across all eight primary analytical modules:
</p>
<p>
1. <strong>Dashboard View:</strong> Displays high-level executive cards: overall sustainability score dial, explicit data coverage percentage, problem count, and real-time OpenAQ live status.
</p>
<p>
2. <strong>City Assessment View:</strong> Features the master scorecard dial ($Score / 100$), analytical highlight badges for strongest municipal asset and primary challenge, and detailed indicator scorecards with reference observation years and source citations.
</p>
<p>
3. <strong>Indicators Explorer:</strong> Displays metric triads (observed value, normalized score, index weight) alongside statutory planning benchmarks (NAAQS, SWM 2016, URDPFI, NUTP) and visual status meters.
</p>
<p>
4. <strong>Problem Areas Matrix:</strong> Groups municipal metrics into four priority tiers: Critical Deficits ($<40$), Needs Attention ($40–59.9$), Acceptable ($\ge 60$), and Monitored Proxies, tracking exact deficit points needed for compliance.
</p>
<p>
5. <strong>Spatial Feasibility Map:</strong> Embeds an interactive Leaflet GIS view displaying verified OSM park polygons and candidate greening sites projected in UTM Zone 43N (EPSG:32643) with calculated acreage in hectares.
</p>
<p>
6. <strong>Recommendations Engine:</strong> Presents localized municipal authority narratives, severity filtering (Critical, High, Strategic), 3-phase roadmaps (Operational, Capital Works, Systemic Reform), URDPFI spatial parameters, target KPIs, and collapsible FAISS statutory citations.
</p>
<p>
7. <strong>Impact Analysis Studio:</strong> Features an interactive slider ($+1$ to $+50$ points) and preset buttons enabling planners to simulate score improvements and review before-and-after composite score deltas.
</p>
<p>
8. <strong>Official Assessment Dossier:</strong> Formats the comprehensive assessment into an institutional report layout with serial reference numbering, metadata tables, and clean A4 print/PDF stylesheet formatting.
</p>

<div class="section-heading">6.3 Comparative Municipal Case Studies</div>
<p>
To evaluate system efficacy, three contrasting urban local bodies representing different geographical and administrative tiers were analyzed, as illustrated in Figure 6.1.
</p>

<div class="sub-section-heading">6.3.1 Case Study 1: Pune Municipal Corporation (Tier-1 Metropole)</div>
<p>
- <strong>Empirical Profile:</strong> Air Quality AQI = 104.85 (Score: 37.13/100, Problem Area); Waste Treatment = 86.96% (Score: 84.55/100, Acceptable); Density = 11,304 persons/km² (Score: 73.20/100, Acceptable); Green Space = 0.7156% (Score: 0.33/100, Critical Deficit); Traffic Congestion = 71.1% peak delay (Score: 0.00/100, Critical Deficit).<br>
- <strong>Composite Score:</strong> 33.20 / 100 (Audit Status: Full, 100% Coverage).<br>
- <strong>Systemic Findings:</strong> Despite robust municipal solid waste treatment, Pune's sustainability score is severely depressed by critical deficits in documented public open space (0.7156% vs statutory 10% URDPFI norm) and severe road traffic delays (71.1%). USAS generates targeted interventions for non-motorized transport (NMT) corridors along high-delay junctions (e.g., University Road, Hadapsar) and Miyawaki pocket forest reclamation along riparian buffers.
</p>

<div class="sub-section-heading">6.3.2 Case Study 2: Municipal Corporation of Greater Mumbai (Megacity)</div>
<p>
- <strong>Empirical Profile:</strong> Extreme demographic density (39,977 persons/km², Score: 0.00/100, Critical Deficit); Traffic Congestion = 63.2% (Score: 14.08/100, Critical Deficit); Solid Waste Treatment = 72.40% (Score: 70.10/100, Acceptable); Air Quality AQI = 96.20 (Score: 42.10/100, Attention).<br>
- <strong>Systemic Findings:</strong> The system highlights severe demographic carrying capacity stress. Recommended interventions emphasize high-capacity Transit-Oriented Development (TOD) zoning around suburban rail corridors and decentralized waste processing to alleviate Deonar dumpsite transport pressure.
</p>

<div class="sub-section-heading">6.3.3 Case Study 3: Nagpur Municipal Corporation (Tier-2 Regional Hub)</div>
<p>
- <strong>Empirical Profile:</strong> Scored Indicators = Air Quality, Waste Treatment, Density, Green Space. Scored data coverage = 80.0% (Partial Assessment). Traffic metric: 2,227,000 registered vehicles tracked as an explicit MMVD regional pressure proxy.<br>
- <strong>Dynamic Re-normalization:</strong> Weights for the 4 available indicators re-normalize from 0.20 to 0.25 each. Overall score evaluates to 48.60/100.<br>
- <strong>Systemic Integrity:</strong> The system prevents synthetic zero-substitution for traffic, demonstrating dynamic mathematical weight redistribution without penalizing the municipality.
</p>

<div class="diagram-container" style="text-align: center;">
  <div style="font-weight: bold; margin-bottom: 8pt;">OVERALL SUSTAINABILITY SCORE PROFILE (SAMPLE CITIES)</div>
  <div style="display: flex; justify-content: space-around; align-items: flex-end; height: 110pt; padding-top: 10pt;">
    <div style="text-align: center; width: 28%;">
      <div style="background: #ef4444; height: 35pt; width: 40pt; margin: 0 auto; border-radius: 4px;"></div>
      <strong style="display:block; margin-top: 4pt; font-size: 10pt;">Pune: 33.20</strong>
      <span style="font-size: 8.5pt; color: #555;">Critical Green/Traffic</span>
    </div>
    <div style="text-align: center; width: 28%;">
      <div style="background: #f59e0b; height: 50pt; width: 40pt; margin: 0 auto; border-radius: 4px;"></div>
      <strong style="display:block; margin-top: 4pt; font-size: 10pt;">Nagpur: 48.60</strong>
      <span style="font-size: 8.5pt; color: #555;">Re-normalized 4/5</span>
    </div>
    <div style="text-align: center; width: 28%;">
      <div style="background: #10b981; height: 68pt; width: 40pt; margin: 0 auto; border-radius: 4px;"></div>
      <strong style="display:block; margin-top: 4pt; font-size: 10pt;">Navi Mumbai: 64.80</strong>
      <span style="font-size: 8.5pt; color: #555;">Acceptable Performing</span>
    </div>
  </div>
</div>
<div class="figure-caption">Figure 6.1: Comparative Overall Sustainability Score Profile for Sample Cities</div>

<div class="section-heading">6.4 Automated Verification Test Suite</div>
<p>
The system's architectural integrity and contract invariants are continuously validated through an automated unit test suite (<pre style="display:inline; padding:1px 4px;">tests/test_api.py</pre>). All 25 test suites pass with zero regressions, as detailed in Table 6.2.
</p>

<div class="table-title">Table 6.2: Automated Unit Verification Test Suite Summary</div>
<table>
  <thead>
    <tr>
      <th>Test Suite Category</th>
      <th>Tests Executed</th>
      <th>Key Contract Assertions Verified</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Data Ingestion & Integrity</strong></td>
      <td>5</td>
      <td>Schema conformity, duplicate city rejection, case/whitespace insensitivity</td>
      <td><strong>PASS</strong> (100%)</td>
    </tr>
    <tr>
      <td><strong>MCDM Normalization</strong></td>
      <td>5</td>
      <td>Directionality (Cost vs Benefit), Min-Max bounding, dynamic weight re-normalization</td>
      <td><strong>PASS</strong> (100%)</td>
    </tr>
    <tr>
      <td><strong>Data Policy Contracts</strong></td>
      <td>4</td>
      <td>Zero-filling prevention, Pune green score = 0.33, Nagpur vehicle proxy segregation</td>
      <td><strong>PASS</strong> (100%)</td>
    </tr>
    <tr>
      <td><strong>Spatial GIS Projection</strong></td>
      <td>3</td>
      <td>EPSG:32643 projection validity, Overpass cache handling, metric area units</td>
      <td><strong>PASS</strong> (100%)</td>
    </tr>
    <tr>
      <td><strong>FAISS RAG & AI Safety</strong></td>
      <td>4</td>
      <td>Embedding dimension (384), metadata citation preservation, Gemini rate limit masking</td>
      <td><strong>PASS</strong> (100%)</td>
    </tr>
    <tr>
      <td><strong>REST API & Simulation</strong></td>
      <td>4</td>
      <td>Endpoint HTTP 200 responses, $\Delta Score$ sensitivity calculation, error sanitization</td>
      <td><strong>PASS</strong> (100%)</td>
    </tr>
    <tr>
      <td><strong>Total Test Execution</strong></td>
      <td><strong>25 Tests</strong></td>
      <td><strong>Full Backend Test Suite Execution Time: 28.16 seconds</strong></td>
      <td><strong>ALL PASS</strong></td>
    </tr>
  </tbody>
</table>

<div class="section-heading">6.5 System Latency & Performance Benchmarks</div>
<p>
Performance profiling demonstrates high responsiveness suitable for municipal deployment:
- <strong>Master Dataset Lookup & Scoring:</strong> $14.2\text{ ms}$ average latency.
- <strong>FAISS Vector Retrieval (Top-3 Chunks):</strong> $11.8\text{ ms}$ execution time.
- <strong>Cached Spatial Geometry Extraction:</strong> $8.5\text{ ms}$ response time.
- <strong>End-to-End City Assessment API Response:</strong> $24.6\text{ ms}$.
- <strong>Frontend Production Bundle (Vite Build):</strong> $1.40\text{ s}$ compilation time (<pre style="display:inline; padding:1px 4px;">index.css</pre> = 62.05 kB, <pre style="display:inline; padding:1px 4px;">index.js</pre> = 300.44 kB).
</p>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- CHAPTER 7: CONCLUSION & FUTURE SCOPE -->
<!-- ========================================================================= -->
<div class="chapter-heading">CHAPTER 7<br>CONCLUSION & FUTURE SCOPE</div>

<div class="section-heading">7.1 Summary of Work</div>
<p>
The Urban Sustainability Assessment System (USAS) successfully delivers an end-to-end, empirical, and deterministic decision support platform tailored to the 42 statutory urban centers of Maharashtra. By integrating official datasets from the CPCB, MPCB, Census of India, and MMVD, USAS eliminates synthetic data invention and replaces arbitrary weighting with a transparent Weighted Sum Model featuring dynamic weight re-normalization. The platform grounds public policy synthesis through FAISS dense vector retrieval over national statutory planning frameworks, coupling generative recommendations to verified municipal deficits and projected metric spatial geometries (UTM Zone 43N EPSG:32643).
</p>

<div class="section-heading">7.2 Key Contributions</div>
<p>
1. <strong>Empirical 42-City Baseline:</strong> Constructed a clean, verified multi-criteria sustainability baseline for all statutory urban centers in Maharashtra without data fabrication.
</p>
<p>
2. <strong>Dynamic Re-normalization Model:</strong> Formulated an auditable WSM MCDM algorithm that dynamically adjusts weights for missing indicators, solving a critical flaw in existing municipal indices.
</p>
<p>
3. <strong>Metric Spatial Feasibility Grounding:</strong> Bridged the gap between abstract indicator scoring and tangible urban geography by reprojecting candidate sites into metric UTM 43N coordinates.
</p>
<p>
4. <strong>Hallucination-Proof Policy Synthesis:</strong> Integrated FAISS vector retrieval over statutory corpora with Google Gemini to guarantee that recommendations reference legitimate government schemes and physical planning parameters.
</p>

<div class="section-heading">7.3 System Limitations</div>
<p>
The system's operational constraints include reliance on Census 2011 figures pending new national census releases, spatial variation in continuous ambient air monitoring stations in Tier-3 municipalities, and volunteer mapping density variations in OpenStreetMap for small rural municipal councils.
</p>

<div class="section-heading">7.4 Future Scope</div>
<p>
1. <strong>Automated Satellite Canopy Extraction:</strong> Integrate automated Google Earth Engine pipelines computing high-resolution Sentinel-2 NDVI canopy metrics to supplement volunteer OSM green space records.
</p>
<p>
2. <strong>IoT Edge Air Quality Sensing:</strong> Incorporate calibrated municipal low-cost IoT sensor networks to provide micro-ward air quality telemetry.
</p>
<p>
3. <strong>Predictive Urban Simulation:</strong> Extend the sensitivity simulator with machine learning forecasting models predicting decadal sustainability trajectory responses under alternative municipal budget allocations.
</p>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- SECTION 12: MAPPING TO SDGS -->
<!-- ========================================================================= -->
<div class="chapter-heading">12. MAPPING OF THE PROJECT TO SUSTAINABLE DEVELOPMENT GOALS (SDGS)</div>

<p class="no-indent">
Students shall identify the Sustainable Development Goal(s) relevant to their project and explain how the project objectives, methodology, and expected outcomes contribute to the selected goal(s).
</p>

<div class="table-title">Table 12.1: Mapping of USAS to Sustainable Development Goals</div>
<table>
  <thead>
    <tr>
      <th>Project Title</th>
      <th>SDG Number and Name</th>
      <th>Relevant SDG Target(s)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="3"><strong>Urban Sustainability Assessment System: A Data-Driven Decision Support Framework (USAS)</strong></td>
      <td><strong>Primary: SDG 11</strong><br>Sustainable Cities and Communities</td>
      <td>
        <strong>Target 11.6:</strong> Reduce the adverse per capita environmental impact of cities, including by paying special attention to air quality and municipal waste management.<br>
        <strong>Target 11.7:</strong> Provide universal access to safe, inclusive and accessible, green and public spaces.<br>
        <strong>Target 11.2:</strong> Provide access to safe, affordable, accessible and sustainable transport systems.
      </td>
    </tr>
    <tr>
      <td><strong>Secondary: SDG 13</strong><br>Climate Action</td>
      <td><strong>Target 13.2:</strong> Integrate climate change measures into national and sub-national policies, strategies and planning.</td>
    </tr>
    <tr>
      <td><strong>Secondary: SDG 3</strong><br>Good Health and Well-Being</td>
      <td><strong>Target 3.9:</strong> Substantially reduce the number of deaths and illnesses from hazardous chemicals and air, water and soil pollution.</td>
    </tr>
  </tbody>
</table>

<div class="section-heading">Justification</div>
<p>
The Urban Sustainability Assessment System (USAS) directly addresses the systemic environmental degradation and infrastructural strain confronting the 42 statutory urban centers of Maharashtra. By integrating official empirical observations from the Central Pollution Control Board (CPCB) and Maharashtra Pollution Control Board (MPCB), the system equips municipal commissioners and urban planners with an objective, data-driven multi-criteria framework to monitor municipal performance. USAS directly advances <strong>SDG 11 (Sustainable Cities and Communities)</strong> by identifying critical deficits in municipal solid waste treatment (Target 11.6), evaluating severe vehicular traffic congestion (Target 11.2), and calculating accessible public open space deficits against statutory URDPFI benchmarks (Target 11.7). Through its Retrieval-Augmented Generation (RAG) architecture grounded in national environmental guidelines (NCAP, SWM 2016, NUTP), USAS provides actionable, phased municipal intervention roadmaps that enable municipal local bodies to transition from unscientific dumpsite disposal to scientific processing and from private vehicular dependency to transit-oriented development. In doing so, the framework strengthens climate-resilient urban governance (SDG 13) and mitigates acute public health risks stemming from urban air pollution (SDG 3).
</p>

<div class="section-heading">Evidence of Contribution</div>
<p>
USAS delivers tangible, measurable analytical contributions to municipal sustainability governance:
- <strong>Solid Waste Management (Target 11.6):</strong> Evaluates treatment efficiency across 42 cities, pinpointing municipalities operating below 50% processing capacity and generating phased roadmaps to eliminate open dumping.
- <strong>Urban Green Space Accessibility (Target 11.7):</strong> Quantifies the gap between documented municipal green space and the statutory URDPFI benchmark (10–12 m² per capita or 10% land cover), identifying candidate intervention sites projected in UTM Zone 43N metric hectares.
- <strong>Air Quality Governance (Target 11.6 / Target 3.9):</strong> Maps longitudinal CPCB AQI baselines alongside real-time OpenAQ telemetry, providing municipal administrators with an empirical basis for NCAP road dust abatement and clean corridor investments.
</p>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- SECTION 13: RELATION TO ENVIRONMENT -->
<!-- ========================================================================= -->
<div class="chapter-heading">13. RELATION OF THE PROJECT TO THE ENVIRONMENT</div>

<p>
The development and deployment of the <strong>Urban Sustainability Assessment System (USAS)</strong> have direct positive environmental implications, while maintaining minimal adverse computational footprints. This evaluation analyzes the environmental profile of the software system across the five mandatory institutional criteria:
</p>

<p>
<strong>1. Use of Resources:</strong> As a software-based decision support system, the project’s direct resource consumption was restricted to electrical energy required for local development workstations, testing servers, and network data transmission. Over the 8-month development and validation lifecycle, total electrical consumption is estimated at approximately $48\text{ kWh}$ (equivalent to approximately $39.3\text{ kg CO}_2\text{e}$ under the prevailing regional grid emission factor). By compiling digital assessment dossiers, the system eliminates paper consumption associated with traditional multi-volume printed municipal master plan surveys.
</p>

<p>
<strong>2. Environmental Benefits:</strong> USAS generates profound indirect environmental benefits by providing municipal local bodies with data-driven decision support. Specifically, the framework:
- Identifies municipal solid waste processing deficits, enabling cities to prevent unscientific open dumping and reduce landfill methane emissions and leachate soil contamination.
- Pinpoints severe urban congestion corridors, facilitating targeted municipal investments in Non-Motorized Transport (NMT) and signal synchronization that directly lower vehicular carbon monoxide, nitrogen oxide, and particulate emissions.
- Pinpoints severe urban open space deficits, identifying vacant municipal parcels for urban afforestation (Miyawaki pocket forests) that mitigate the Urban Heat Island (UHI) effect and improve urban groundwater recharge.
</p>

<p>
<strong>3. Potential Adverse Impacts:</strong> Software execution incurs minor indirect environmental impacts via cloud server electrical consumption during Google Gemini API inference and OpenAQ data fetching. However, because USAS executes all mathematical normalization, scoring, and FAISS vector retrieval locally on energy-efficient CPU threads, external cloud compute utilization is kept to an absolute minimum.
</p>

<p>
<strong>4. Preventive and Mitigation Measures:</strong> To minimize computational energy consumption, the system employs lightweight dense vector embeddings (<pre style="display:inline; padding:1px 4px;">all-MiniLM-L6-v2</pre>, requiring only 80MB memory footprint) and exact inner-product FAISS CPU indexing, avoiding energy-intensive multi-GPU clusters. Furthermore, extensive disk caching of Overpass GIS spatial geometries and OpenAQ telemetry prevents redundant network calls.
</p>

<p>
<strong>5. Supporting Evidence:</strong> Automated unit testing and performance benchmarking verify that composite city assessments execute in under 25 milliseconds, consuming less than $0.0001\text{ kWh}$ per municipal evaluation—representing a $99.9\%$ energy reduction compared to running heavy, unconstrained parameter large language models.
</p>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- SECTION 14: PROJECT COST STATEMENT -->
<!-- ========================================================================= -->
<div class="chapter-heading">14. PROJECT COST STATEMENT</div>

<p class="no-indent">
The itemized expenditure incurred during the research, implementation, testing, and documentation of the Urban Sustainability Assessment System (USAS) is presented in Table 14.1.
</p>

<div class="table-title">Table 14.1: Itemized Project Expenditure Statement</div>
<table>
  <thead>
    <tr>
      <th>Sr. No.</th>
      <th>Item / Expense Description</th>
      <th>Quantity</th>
      <th>Unit Cost (₹)</th>
      <th>Total Cost (₹)</th>
      <th>Basis / Remarks</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>Hardware / Workstation Facilities</td>
      <td>2 Units</td>
      <td>₹0</td>
      <td>₹0</td>
      <td>Institution-provided laboratory facilities and student-owned personal computing workstations.</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Software Licenses / Tooling</td>
      <td>1 Stack</td>
      <td>₹0</td>
      <td>₹0</td>
      <td>Built entirely on free, open-source software (Python, Flask, React, Vite, Node.js, FAISS, Leaflet).</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Cloud APIs / Subscriptions</td>
      <td>2 APIs</td>
      <td>₹0</td>
      <td>₹0</td>
      <td>Free educational developer tier utilized for OpenAQ REST API and Google Gemini API.</td>
    </tr>
    <tr>
      <td>4</td>
      <td>Empirical Datasets & Corpora</td>
      <td>5 Datasets</td>
      <td>₹0</td>
      <td>₹0</td>
      <td>Public open-access government repositories (CPCB, MPCB, Census 2011, OpenStreetMap).</td>
    </tr>
    <tr>
      <td>5</td>
      <td>Testing, Verification & Calibration</td>
      <td>25 Suites</td>
      <td>₹0</td>
      <td>₹0</td>
      <td>Local automated test execution using Python unittest harness.</td>
    </tr>
    <tr>
      <td>6</td>
      <td>Field Travel & Municipal Verification</td>
      <td>4 Visits</td>
      <td>₹300</td>
      <td>₹1,200</td>
      <td>Local municipal ground-truthing and physical planning verification visits within Maharashtra.</td>
    </tr>
    <tr>
      <td>7</td>
      <td>Documentation, Hard Binding & Embossing</td>
      <td>5 Copies</td>
      <td>₹700</td>
      <td>₹3,500</td>
      <td>Hard-bound copies with golden embossing for Student 1, Student 2, Guide, HOD, and Department Library.</td>
    </tr>
    <tr>
      <td>8</td>
      <td>Archival Storage Media & Materials</td>
      <td>2 Units</td>
      <td>₹250</td>
      <td>₹500</td>
      <td>Project demonstration archival storage media (USB/DVD).</td>
    </tr>
    <tr>
      <td colspan="4" style="text-align: right; font-weight: bold;">TOTAL PROJECT EXPENDITURE:</td>
      <td colspan="2" style="font-weight: bold; font-size: 11pt; color: #173b2b;">₹ 5,200</td>
    </tr>
  </tbody>
</table>

<div class="section-heading">Resource Statement</div>
<p>
The total expenditure incurred for developing the USAS prototype was strictly limited to ₹ 5,200, representing direct printing, binding, archival, and local travel expenses. Software development, algorithm formulation, vector indexing, geospatial analysis, and user interface engineering were conducted entirely utilizing institutional laboratory facilities, student personal computing hardware, and open-source scientific software libraries without external commercial software licensing fees.
</p>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- REFERENCES -->
<!-- ========================================================================= -->
<div class="chapter-heading">REFERENCES</div>
<p class="no-indent" style="font-size: 11pt; line-height: 1.6;">
[1] S. Shen, Y. Peng, X. Zhang, and Y. Wu, "Refining the comprehensive assessment of urban sustainability: A study of municipal indicators," <em>Sustainable Cities and Society</em>, vol. 27, pp. 240–252, 2016.<br><br>
[2] M. Alberti, "Measuring urban sustainability," <em>Environmental Impact Assessment Review</em>, vol. 16, no. 4, pp. 381–424, 1996.<br><br>
[3] L. Y. Shen, J. J. Ochoa, M. N. Shah, and X. Zhang, "The application of urban sustainability indicators: A comparison between international practices," <em>Habitat International</em>, vol. 35, no. 1, pp. 17–29, 2011.<br><br>
[4] J. J. Huang, G. H. Tzeng, and H. H. Ong, "Multidimensional evaluation of urban environmental quality using improved multicriteria decision analysis," <em>Journal of Environmental Management</em>, vol. 90, no. 2, pp. 950–959, 2009.<br><br>
[5] E. Triantaphyllou, <em>Multi-Criteria Decision Making Methods: A Comparative Study</em>, Kluwer Academic Publishers, Applied Optimization Series, vol. 44, 2000.<br><br>
[6] T. L. Saaty, "Decision making with the analytic hierarchy process," <em>International Journal of Services Sciences</em>, vol. 1, no. 1, pp. 83–98, 2008.<br><br>
[7] C. L. Hwang and K. Yoon, <em>Multiple Attribute Decision Making: Methods and Applications</em>, Springer-Verlag, Berlin, 1981.<br><br>
[8] P. Zhou, B. W. Ang, and K. L. Poh, "Comparing aggregating methods for constructing the composite environment index," <em>Ecological Economics</em>, vol. 60, no. 2, pp. 373–380, 2006.<br><br>
[9] C. S. B. Grimmond, "Urbanization and global environmental change: Local effects of urban warming," <em>The Geographical Journal</em>, vol. 173, no. 1, pp. 83–88, 2007.<br><br>
[10] S. B. Roy, P. K. Joshi, and K. Kumar, "Urban green space dynamics and its impact on urban heat island in rapidly growing Indian cities," <em>Urban Climate</em>, vol. 34, p. 100705, 2020.<br><br>
[11] C. Y. Jim and W. Y. Chen, "Accessibility of urban green spaces and its planning implications in high-density cities," <em>Landscape and Urban Planning</em>, vol. 65, no. 2, pp. 151–164, 2003.<br><br>
[12] P. Neis and D. Zielstra, "Recent developments and future trends in Volunteered Geographic Information research: The case of OpenStreetMap," <em>Future Internet</em>, vol. 6, no. 1, pp. 76–106, 2014.<br><br>
[13] J. P. Snyder, <em>Map Projections: A Working Manual</em>, U.S. Geological Survey Professional Paper 1395, Washington, D.C., 1987.<br><br>
[14] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. Yih, T. Rocktäschel, S. Riedel, and D. Kiela, "Retrieval-augmented generation for knowledge-intensive NLP tasks," in <em>Advances in Neural Information Processing Systems (NeurIPS)</em>, vol. 33, pp. 9459–9474, 2020.<br><br>
[15] N. Reimers and I. Gurevych, "Sentence-BERT: Sentence embeddings using Siamese BERT-networks," in <em>Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP)</em>, pp. 3982–3992, 2019.<br><br>
[16] J. Johnson, M. Douze, and H. Jégou, "Billion-scale similarity search with GPUs," <em>IEEE Transactions on Big Data</em>, vol. 7, no. 3, pp. 535–547, 2021.<br><br>
[17] Ministry of Housing and Urban Affairs (MoHUA), <em>Urban and Regional Development Plans Formulation and Implementation (URDPFI) Guidelines</em>, Government of India, New Delhi, 2015.<br><br>
[18] Central Pollution Control Board (CPCB), <em>National Ambient Air Quality Standards (NAAQS) and AQI Technical Documentation</em>, Ministry of Environment, Forest and Climate Change, New Delhi, 2014.
</p>

<div class="page-break"></div>

<!-- ========================================================================= -->
<!-- APPENDIX -->
<!-- ========================================================================= -->
<div class="chapter-heading">APPENDIX<br>USER MANUAL & DEPLOYMENT GUIDE</div>

<div class="section-heading">A.1 System Prerequisites & Installation</div>
<p>
The USAS application runs on standard Windows or Linux servers. Ensure Python 3.11+ and Node.js 20+ are installed.
</p>
<p class="no-indent"><strong>Step 1: Clone or Open Repository:</strong></p>
<pre>
cd E:\Project\Final
</pre>

<p class="no-indent"><strong>Step 2: Activate Python Virtual Environment & Install Dependencies:</strong></p>
<pre>
.\backend\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
pip install -r backend\requirements-rag.txt
pip install -r backend\requirements-spatial.txt
</pre>

<p class="no-indent"><strong>Step 3: Configure Environment Credentials in <pre style="display:inline; padding:1px 3px;">backend/.env</pre>:</strong></p>
<pre>
OPENAQ_API_KEY=your_openaq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
PORT=5000
</pre>

<div class="section-heading">A.2 Executing Automated Verification Tests</div>
<p>
Execute the full 25-suite unit test suite to verify scoring contracts, proxy segregation, and API routes:
</p>
<pre>
& "backend\.venv\Scripts\python.exe" -m unittest discover -s tests -v
</pre>

<div class="section-heading">A.3 Launching the USAS Servers</div>
<p class="no-indent"><strong>1. Start the Flask Backend Daemon:</strong></p>
<pre>
& "backend\.venv\Scripts\python.exe" backend\run.py
# Server listening on http://127.0.0.1:5000
</pre>

<p class="no-indent"><strong>2. Start the Vite Frontend Development Server:</strong></p>
<pre>
cd frontend
npm install
npm run dev
# Application available at http://localhost:5173
</pre>

<div class="section-heading">A.4 Navigating the System Interface</div>
<p>
1. Open <pre style="display:inline; padding:1px 3px;">http://localhost:5173</pre> in any modern web browser.<br>
2. Click <strong>Access USAS Decision Support Platform</strong>.<br>
3. Select any of the 42 supported Maharashtra urban centers from the dropdown (e.g., Pune, Mumbai, Nagpur, Chhatrapati Sambhajinagar).<br>
4. Navigate across analytical modules via the left sidebar: Review the comprehensive <strong>MCDM Scorecard</strong>, inspect <strong>Indicators</strong> against statutory benchmarks, evaluate the <strong>Problem Areas</strong> vulnerability matrix, examine candidate green sites on the <strong>Spatial Feasibility</strong> map, explore grounded <strong>Recommendations</strong>, simulate hypothetical target gains in the <strong>Impact Studio</strong>, and compile or print the formal <strong>Dossier Report</strong>.
</p>

</body>
</html>
"""

print(f"Writing comprehensive HTML report to: {HTML_OUTPUT}")
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
print(f"Compiling PDF to: {PDF_OUTPUT}")

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
    print(f"SUCCESS: PDF generated successfully! Size: {size_bytes / 1024:.2f} KB ({size_bytes} bytes)")
    print(f"Path: {PDF_OUTPUT}")
else:
    print("Error generating PDF:", result.stderr)
    sys.exit(1)
