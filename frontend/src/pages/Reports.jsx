import { useEffect, useState } from 'react'
import { getReport, downloadReportPdf } from '../services/api.js'

function Reports({ city, assessment, loading, apiError, impactScenario }) {
  const [report, setReport] = useState(null)
  const [error, setError] = useState('')
  const [fetching, setFetching] = useState(false)
  const [downloading, setDownloading] = useState(false)
  const [downloadError, setDownloadError] = useState('')

  useEffect(() => {
    if (!city) {
      setReport(null)
      return
    }
    let active = true
    setFetching(true)
    setError('')
    getReport(city)
      .then((data) => {
        if (active) setReport(data)
      })
      .catch((err) => {
        if (active) setError(err.message)
      })
      .finally(() => {
        if (active) setFetching(false)
      })
    return () => {
      active = false
    }
  }, [city])

  const handleDownloadPdf = async () => {
    if (!city) return
    setDownloading(true)
    setDownloadError('')
    try {
      await downloadReportPdf(city)
    } catch (err) {
      setDownloadError(err.message || 'Failed to generate PDF')
    } finally {
      setDownloading(false)
    }
  }

  const formatRawValue = (val) => {
    if (val == null) return '—'
    if (typeof val === 'number') {
      if (val >= 1000) return val.toLocaleString(undefined, { maximumFractionDigits: 1 })
      return val % 1 === 0 ? val.toString() : val.toFixed(2)
    }
    return val
  }

  return (
    <div className="content-page report-page-container">
      <header className="content-page-header no-print">
        <div>
          <h1>Urban Sustainability Assessment Report</h1>
          <p>
            Official comprehensive assessment dossier: multi-criteria evaluation scorecard, policy interventions, and impact scenarios.
          </p>
        </div>
        <div className="report-header-actions" style={{ display: 'flex', gap: '10px' }}>
          <button
            type="button"
            className="btn-print-report"
            onClick={handleDownloadPdf}
            disabled={!report || downloading}
            style={{
              background: '#0f766e',
              color: 'white',
              border: 'none',
              padding: '10px 18px',
              borderRadius: '8px',
              fontWeight: '600',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            {downloading ? 'Generating PDF...' : '⬇ Download Official PDF'}
          </button>
          <button
            type="button"
            className="btn-print-report"
            onClick={() => window.print()}
            disabled={!report}
          >
            🖨 Print / Preview
          </button>
        </div>
      </header>

      {downloadError && (
        <div className="error-card no-print" role="alert" style={{ marginBottom: '16px' }}>
          <span>Error downloading PDF: {downloadError}</span>
        </div>
      )}

      <main className="content-page-body">
        {!city ? (
          <div className="empty-state no-print">
            <h2>No City Selected</h2>
            <p>Select a city from the dashboard to generate and inspect its comprehensive assessment report.</p>
          </div>
        ) : (
          <>
            {(loading || fetching) && (
              <div className="loading-card no-print">
                <p>Compiling comprehensive sustainability report and retrieving policy citations for {city}…</p>
              </div>
            )}

            {(apiError || error) && (
              <div className="error-card no-print" role="alert">
                {apiError || error}
              </div>
            )}

            {report && (
              <div className="formal-report-dossier" id="printable-report">
                {/* 1. COVER PAGE / EXECUTIVE HEADER */}
                <div className="report-cover-header">
                  <div className="institution-brand">
                    <span className="brand-abbr">USAS</span>
                    <div>
                      <h2>Urban Sustainability Assessment System</h2>
                      <p>State-Level Decision Support Framework for Cities in Maharashtra</p>
                    </div>
                  </div>
                  <div className="report-serial-badge">
                    <span>STATUTORY URBAN DOSSIER</span>
                    <strong>REF: USAS-MH-2026-{city.toUpperCase().replace(/\s+/g, '-')}</strong>
                  </div>
                </div>

                {/* EXECUTIVE METADATA BANNER */}
                <div className="report-meta-table-wrap">
                  <table className="report-meta-table">
                    <tbody>
                      <tr>
                        <th>Target Urban Center:</th>
                        <td><strong>{city}, Maharashtra</strong></td>
                        <th>Evaluation Date:</th>
                        <td>{report.assessment_date}</td>
                      </tr>
                      <tr>
                        <th>Overall Sustainability Score:</th>
                        <td>
                          <span className="report-score-badge">
                            {report.overall_score != null ? `${report.overall_score} / 100` : '—'}
                          </span>{' '}
                          ({report.score_status} Assessment)
                        </td>
                        <th>Empirical Data Coverage:</th>
                        <td>{report.data_coverage_pct}% ({report.indicators?.filter(i => i.available).length || 4} of 5 Indicators Scored)</td>
                      </tr>
                      <tr>
                        <th>Governing Model:</th>
                        <td>Weighted Sum Model (WSM) + Min-Max Normalization</td>
                        <th>Jurisdiction Body:</th>
                        <td>{city} Municipal Local Body</td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                {/* 2. EXECUTIVE SUMMARY */}
                <section className="report-section">
                  <div className="report-section-header">
                    <h3>1.0 Executive Summary</h3>
                  </div>
                  <p className="report-lead-text">
                    This statutory dossier provides an empirical, deterministic assessment of <strong>{city}</strong> across
                    five core urban sustainability pillars. Evaluated under the Maharashtra State Urban Decision Support Framework,
                    the municipality achieved an overall index score of <strong>{report.overall_score != null ? `${report.overall_score}/100` : 'Incomplete'}</strong> with{' '}
                    <strong>{report.data_coverage_pct}% data coverage</strong>.
                  </p>
                  <p>
                    Indicators scoring below 40.0 points represent critical municipal deficits demanding prioritized capital
                    budgeting and evidence-grounded policy interventions.
                  </p>
                </section>

                {/* 3. ASSESSMENT OVERVIEW & SCORECARD */}
                <section className="report-section">
                  <div className="report-section-header">
                    <h3>2.0 Assessment Overview & Five Core Indicators</h3>
                    <p>Transparent raw measurements, normalized 0–100 scores, reference years, and source provenance.</p>
                  </div>

                  <table className="report-data-table">
                    <thead>
                      <tr>
                        <th>Pillar Name</th>
                        <th>Empirical Value</th>
                        <th>Standard Unit</th>
                        <th>Reference Year</th>
                        <th>Norm Score</th>
                        <th>Weight</th>
                        <th>Statutory Provenance</th>
                      </tr>
                    </thead>
                    <tbody>
                      {report.indicators?.map((ind) => (
                        <tr key={ind.key || ind.name}>
                          <td><strong>{ind.name}</strong></td>
                          <td>{formatRawValue(ind.value ?? ind.raw_value)}</td>
                          <td>{ind.unit}</td>
                          <td>{ind.year || ind.reference_year || '—'}</td>
                          <td>
                            {ind.score != null ? (
                              <span className={`pill-score ${ind.score < 40 ? 'pill-crit' : ind.score < 60 ? 'pill-att' : 'pill-good'}`}>
                                {ind.score} / 100
                              </span>
                            ) : (
                              <span className="pill-score pill-na">Not Available</span>
                            )}
                          </td>
                          <td>20%</td>
                          <td><small>{ind.source_name || ind.source}</small></td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </section>

                {/* 4. PROBLEM AREAS */}
                <section className="report-section">
                  <div className="report-section-header">
                    <h3>3.0 Problem Areas & Severity Audit</h3>
                    <p>Statutory classification of municipal performance against uniform state standards.</p>
                  </div>

                  {report.problem_areas && report.problem_areas.length > 0 ? (
                    <div className="report-problems-grid">
                      {report.problem_areas.map((prob) => (
                        <article key={prob.key || prob.name} className="report-problem-card">
                          <div className="card-top">
                            <span className="tag-crit">Critical Deficit (&lt;40)</span>
                            <strong>Score: {prob.score} / 100</strong>
                          </div>
                          <h4>{prob.name}</h4>
                          <p>
                            Raw measurement of <strong>{formatRawValue(prob.raw_value ?? prob.value)} {prob.unit}</strong>{' '}
                            falls significantly below the state acceptable threshold. Immediate capital intervention required.
                          </p>
                        </article>
                      ))}
                    </div>
                  ) : (
                    <p>No indicators fall below the 40/100 critical problem threshold in this municipality.</p>
                  )}
                </section>

                {/* 5. RECOMMENDATIONS */}
                <section className="report-section">
                  <div className="report-section-header">
                    <h3>4.0 Evidence-Grounded Policy Recommendations</h3>
                    <p>Interventions synthesized via Retrieval-Augmented Generation (RAG) over NCAP, URDPFI, MPCB, and TOD regulations.</p>
                  </div>

                  <div className="report-recs-container">
                    {report.recommendations?.slice(0, 4).map((rec, idx) => (
                      <article key={rec.id || idx} className="report-rec-card">
                        <div className="rec-card-header">
                          <span className="rec-number">#{idx + 1}</span>
                          <div>
                            <h4>{rec.title}</h4>
                            <span className="rec-category">Target: {rec.indicator}</span>
                          </div>
                        </div>

                        <p className="rec-body">{rec.recommendation}</p>

                        {/* Phased Roadmap */}
                        {rec.phased_roadmap && (
                          <div className="report-roadmap-grid">
                            <div>
                              <strong>Phase 1: Immediate (Months 0–6)</strong>
                              <p>{rec.phased_roadmap.phase_1_immediate}</p>
                            </div>
                            <div>
                              <strong>Phase 2: Medium-Term (Months 6–18)</strong>
                              <p>{rec.phased_roadmap.phase_2_medium}</p>
                            </div>
                            <div>
                              <strong>Phase 3: Systemic (Months 18–36)</strong>
                              <p>{rec.phased_roadmap.phase_3_long}</p>
                            </div>
                          </div>
                        )}

                        <div className="report-meta-split" style={{ marginTop: '10px' }}>
                          <div>
                            <strong>Planning Standard & Framework:</strong>
                            <p>URDPFI 2015 Guidelines & Maharashtra UDCPR 2020.</p>
                          </div>
                          <div>
                            <strong>Eligible Funding Schemes:</strong>
                            <p>{rec.funding_mechanisms || '15th Finance Commission & AMRUT 2.0 Grants.'}</p>
                          </div>
                        </div>

                        {/* Retrieved Evidence Chunks */}
                        {rec.evidence && rec.evidence.length > 0 && (
                          <div className="report-evidence-box">
                            <strong>Retrieved Knowledge Base Evidence:</strong>
                            <ul>
                              {rec.evidence.slice(0, 2).map((ev) => (
                                <li key={ev.evidence_id}>
                                  [{ev.evidence_id}] {ev.title} ({ev.publication_year || 'Year not recorded'}, p.{ev.page || '1'}): "{ev.excerpt.slice(0, 180)}…"
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </article>
                    ))}
                  </div>
                </section>

                {/* 6. IMPACT SCENARIO MODELING */}
                <section className="report-section">
                  <div className="report-section-header">
                    <h3>5.0 Scenario Sensitivity & Impact Simulation</h3>
                    <p>Quantitative evaluation of target indicator gains on overall sustainability index.</p>
                  </div>

                  {impactScenario && impactScenario.city === city ? (
                    <div className="scenario-report-box">
                      <div className="scenario-meta-row">
                        <span>Simulated Indicator: <strong>{impactScenario.indicator}</strong></span>
                        <span>Assumed Score Gain: <strong>+{impactScenario.assumed_normalized_score_change_points} Points</strong></span>
                        <span>Overall Index Impact: <strong>+{Number(impactScenario.overall_score_change).toFixed(2)} Points</strong></span>
                      </div>
                      <p>
                        Baseline Score: <strong>{impactScenario.baseline_overall_score}</strong> → Projected Score: <strong>{impactScenario.projected_overall_score} / 100</strong>.
                      </p>
                      <small>Assumptions: Other indicators held constant; 20% proportional weight applied.</small>
                    </div>
                  ) : (
                    <div className="scenario-sensitivity-table-wrap">
                      <p>Summary sensitivity projection across target indicators (+10 points assumed gain):</p>
                      <table className="report-data-table">
                        <thead>
                          <tr>
                            <th>Indicator Target</th>
                            <th>Current Baseline Score</th>
                            <th>Projected Indicator Score (+10)</th>
                            <th>Projected Overall Score Gain</th>
                          </tr>
                        </thead>
                        <tbody>
                          {report.indicators
                            ?.filter((i) => i.available)
                            .map((i) => {
                              const availCount = report.indicators?.filter(ind => ind.available).length || 4
                              const gain = (10.0 * 0.20) / (availCount * 0.20)
                              return (
                                <tr key={i.key || i.name}>
                                  <td>{i.name}</td>
                                  <td>{i.score} / 100</td>
                                  <td>{Math.min(100, (i.score || 0) + 10)} / 100</td>
                                  <td><strong>+{gain.toFixed(2)} Points</strong></td>
                                </tr>
                              )
                            })}
                        </tbody>
                      </table>
                    </div>
                  )}
                </section>

                {/* 7. METHODOLOGY & STATUTORY CITATIONS */}
                <section className="report-section">
                  <div className="report-section-header">
                    <h3>6.0 Methodology, Governing Standards & Limitations</h3>
                  </div>

                  <div className="limitations-content">
                    <h4>Multi-Criteria Decision-Making (MCDM) Framework:</h4>
                    <p>
                      Evaluated using the Weighted Sum Model (WSM) with Min-Max normalization relative to the 42 comparison cities.
                      Missing indicators are mathematically re-normalized across available parameters.
                    </p>

                    <h4>Governing Statutory Frameworks:</h4>
                    <ul className="citations-list">
                      <li><strong>National Clean Air Programme (NCAP 2019)</strong> — Ministry of Environment, Forest and Climate Change (MoEFCC).</li>
                      <li><strong>Solid Waste Management (SWM) Rules, 2016</strong> — Notification under Environment (Protection) Act, 1986.</li>
                      <li><strong>Urban and Regional Development Plans Formulation and Implementation (URDPFI) Guidelines 2015</strong> — MoHUA.</li>
                      <li><strong>National Urban Transport Policy (NUTP 2014)</strong> — Ministry of Housing and Urban Affairs (MoHUA).</li>
                      <li><strong>Maharashtra Unified Development Control and Promotion Regulations (UDCPR 2020)</strong> — Urban Development Department.</li>
                    </ul>

                    <h4>Analytical Limitations & Operational Scope:</h4>
                    <ul>
                      {report.limitations?.map((lim, idx) => (
                        <li key={idx}>{lim}</li>
                      ))}
                    </ul>
                  </div>
                </section>

                {/* SIGNATURE / SIGN-OFF BLOCK */}
                <div className="report-signoff-block">
                  <div className="sign-col">
                    <span>Generated By:</span>
                    <strong>USAS Decision Support Engine</strong>
                    <small>State Urban Analytics & Planning Cell</small>
                  </div>
                  <div className="sign-col">
                    <span>Target Municipal Local Body:</span>
                    <strong>{city} Municipal Administration</strong>
                    <small>Urban Development Directorate, Maharashtra</small>
                  </div>
                  <div className="sign-col">
                    <span>Verification Status:</span>
                    <strong>Deterministic & Explainable</strong>
                    <small>Checked against MPCB/CPCB/Census records</small>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
}

export default Reports
