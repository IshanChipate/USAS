import { useEffect, useState } from 'react'
import { getRecommendations } from '../services/api.js'

function Recommendations({ city, assessment, loading, apiError, onNavigate }) {
  const [recommendations, setRecommendations] = useState([])
  const [fetching, setFetching] = useState(false)
  const [error, setError] = useState('')
  const [activeFilter, setActiveFilter] = useState('ALL')
  const [showEvidence, setShowEvidence] = useState({})

  useEffect(() => {
    if (!city) return
    let active = true
    setFetching(true)
    setError('')
    getRecommendations(city)
      .then((data) => {
        if (active) {
          setRecommendations(data.recommendations || [])
        }
      })
      .catch((requestError) => {
        if (active) setError(requestError.message)
      })
      .finally(() => {
        if (active) setFetching(false)
      })
    return () => {
      active = false
    }
  }, [city])

  const toggleEvidence = (index) => {
    setShowEvidence((prev) => ({
      ...prev,
      [index]: !prev[index],
    }))
  }

  const filterCounts = {
    ALL: recommendations.length,
    CRITICAL: recommendations.filter((r) => r.priority?.includes('Critical')).length,
    HIGH: recommendations.filter((r) => r.priority?.includes('High')).length,
    STRATEGIC: recommendations.filter((r) => r.priority?.includes('Strategic')).length,
  }

  const filteredRecommendations = recommendations.filter((item) => {
    if (activeFilter === 'CRITICAL') return item.priority?.includes('Critical')
    if (activeFilter === 'HIGH') return item.priority?.includes('High')
    if (activeFilter === 'STRATEGIC') return item.priority?.includes('Strategic')
    return true
  })

  return (
    <div className="content-page">
      <header className="content-page-header">
        <div>
          <h1>Urban Intervention Recommendations</h1>
          <p>
            Deterministic, evidence-grounded action plans tailored to Maharashtra urban local bodies.
            Combines local municipal context, phased roadmaps, institutional frameworks, and verified policy citations.
          </p>
        </div>
      </header>

      <main className="content-page-body">
        {!city ? (
          <div className="empty-state">
            <h2>No City Selected</h2>
            <p>Select a city from the dashboard or city selector above to review actionable sustainability interventions.</p>
          </div>
        ) : (
          <>
            {/* City Context Card */}
            <section className="recommendation-city-banner">
              <div className="banner-details">
                <span className="banner-badge">Municipal Jurisdiction</span>
                <h2>{recommendations[0]?.local_authority || `${city} Municipal Administration`}</h2>
                <p className="city-narrative">{recommendations[0]?.local_context || `Targeted urban sustainability framework for ${city}, Maharashtra.`}</p>
                {recommendations[0]?.key_landmarks && (
                  <p className="city-landmarks">
                    <strong>Key Corridors & Priority Zones:</strong> {recommendations[0].key_landmarks}
                  </p>
                )}
              </div>
              <div className="banner-stats">
                <div className="stat-pill">
                  <span>Overall Score</span>
                  <strong>{assessment?.overall_sustainability_score != null ? `${assessment.overall_sustainability_score}/100` : 'Assessing'}</strong>
                </div>
                <div className="stat-pill">
                  <span>Interventions</span>
                  <strong>{recommendations.length} Indicators</strong>
                </div>
                <button
                  type="button"
                  className="btn-explore-map"
                  onClick={() => onNavigate && onNavigate('impact')}
                >
                  Simulate Scenario Impact →
                </button>
              </div>
            </section>

            {/* Filter Tabs */}
            <div className="recommendation-filter-bar">
              <button
                type="button"
                className={`filter-btn ${activeFilter === 'ALL' ? 'active' : ''}`}
                onClick={() => setActiveFilter('ALL')}
              >
                All Action Plans ({filterCounts.ALL})
              </button>
              <button
                type="button"
                className={`filter-btn filter-critical ${activeFilter === 'CRITICAL' ? 'active' : ''}`}
                onClick={() => setActiveFilter('CRITICAL')}
              >
                Critical Priority ({filterCounts.CRITICAL})
              </button>
              <button
                type="button"
                className={`filter-btn filter-high ${activeFilter === 'HIGH' ? 'active' : ''}`}
                onClick={() => setActiveFilter('HIGH')}
              >
                High Priority ({filterCounts.HIGH})
              </button>
              <button
                type="button"
                className={`filter-btn filter-strategic ${activeFilter === 'STRATEGIC' ? 'active' : ''}`}
                onClick={() => setActiveFilter('STRATEGIC')}
              >
                Strategic Optimization ({filterCounts.STRATEGIC})
              </button>
            </div>

            {(loading || fetching) && (
              <div className="loading-card">
                <p>Loading localized recommendations and retrieving RAG evidence chunks…</p>
              </div>
            )}

            {(apiError || error) && (
              <div className="error-card" role="alert">
                {apiError || error}
              </div>
            )}

            {/* Recommendation Cards */}
            {!fetching && filteredRecommendations.length > 0 && (
              <div className="recommendation-grid">
                {filteredRecommendations.map((item, index) => {
                  const priorityClass = item.priority?.includes('Critical')
                    ? 'priority-critical'
                    : item.priority?.includes('High')
                    ? 'priority-high'
                    : 'priority-strategic'

                  return (
                    <article className={`recommendation-card ${priorityClass}`} key={item.indicator}>
                      {/* Card Header */}
                      <div className="rec-card-header">
                        <div className="rec-title-wrap">
                          <div className="rec-badge-row">
                            <span className={`priority-tag ${priorityClass}`}>
                              {item.priority}
                            </span>
                            <span className="indicator-tag">
                              {item.indicator}
                            </span>
                            <span className="score-tag">
                              Score: {item.score != null ? `${item.score}/100` : 'N/A (Excluded)'}
                            </span>
                          </div>
                          <h2>{item.title}</h2>
                        </div>
                      </div>

                      {/* Executive Summary & Local Diagnostic */}
                      <div className="rec-executive-box">
                        <p><strong>Urban Diagnostic:</strong> {item.executive_summary}</p>
                      </div>

                      {/* Phased Roadmap */}
                      {item.phased_roadmap && (
                        <div className="rec-roadmap-section">
                          <h3>Phased Implementation Roadmap</h3>
                          <div className="phases-container">
                            <div className="phase-card phase-1">
                              <div className="phase-header">
                                <span className="phase-badge">Phase 1</span>
                                <strong>Immediate Execution (Months 0–6)</strong>
                              </div>
                              <p>{item.phased_roadmap.phase_1_immediate}</p>
                            </div>

                            <div className="phase-card phase-2">
                              <div className="phase-header">
                                <span className="phase-badge">Phase 2</span>
                                <strong>Medium-Term Capital Works (Months 6–18)</strong>
                              </div>
                              <p>{item.phased_roadmap.phase_2_medium}</p>
                            </div>

                            <div className="phase-card phase-3">
                              <div className="phase-header">
                                <span className="phase-badge">Phase 3</span>
                                <strong>Systemic Policy & Transformation (Months 18–36)</strong>
                              </div>
                              <p>{item.phased_roadmap.phase_3_long}</p>
                            </div>
                          </div>
                        </div>
                      )}


                      {/* KPIs and Funding */}
                      <div className="rec-meta-grid">
                        <div className="rec-meta-col">
                          <h4>Measurable Target KPIs</h4>
                          <ul>
                            {item.target_kpis?.map((kpi, kpiIdx) => (
                              <li key={kpiIdx}>{kpi}</li>
                            ))}
                          </ul>
                        </div>
                        <div className="rec-meta-col">
                          <h4>Eligible Funding Schemes</h4>
                          <p className="funding-text">{item.funding_mechanisms}</p>
                          <h4>Governing Policy Citations</h4>
                          <div className="policy-pills">
                            {item.policy_citations?.map((pol, polIdx) => (
                              <a
                                key={polIdx}
                                href={pol.url}
                                target="_blank"
                                rel="noreferrer"
                                className="policy-pill-link"
                              >
                                {pol.framework} ({pol.authority})
                              </a>
                            ))}
                          </div>
                        </div>
                      </div>

                      {/* Gemini AI Enhancement if available */}
                      {item.generated_text ? (
                        <div className="rec-gemini-box">
                          <h4>Gemini AI Synthesized Brief</h4>
                          <p>{item.generated_text}</p>
                        </div>
                      ) : (
                        <div className="rec-offline-notice">
                          <span>Local Grounded Plan</span>
                          <small>Generated deterministically from validated Maharashtra urban planning rules and local RAG knowledge base. (Gemini API key is optional in .env)</small>
                        </div>
                      )}

                      {/* Retrieved Policy Evidence Section */}
                      {item.evidence && item.evidence.length > 0 && (
                        <div className="rec-evidence-accordion">
                          <button
                            type="button"
                            className="evidence-toggle-btn"
                            onClick={() => toggleEvidence(index)}
                          >
                            {showEvidence[index] ? '▲ Hide' : '▼ Inspect'} Retrieved Policy Evidence ({item.evidence.length} Chunks from Knowledge Base)
                          </button>
                          {showEvidence[index] && (
                            <div className="evidence-list-container">
                              {item.evidence.map((source) => (
                                <article className="evidence-chunk-card" key={source.evidence_id}>
                                  <div className="evidence-chunk-header">
                                    <span className="chunk-id">[{source.evidence_id}]</span>
                                    <strong>{source.title}</strong>
                                    {source.publication_year && <span className="chunk-year">({source.publication_year})</span>}
                                    {source.page && <span className="chunk-page">Page {source.page}</span>}
                                    <span className="chunk-similarity">Similarity: {source.similarity}</span>
                                  </div>
                                  <p className="chunk-text">"{source.excerpt}"</p>
                                  {source.source_url && (
                                    <a
                                      href={source.source_url}
                                      target="_blank"
                                      rel="noreferrer"
                                      className="chunk-source-link"
                                    >
                                      View Source Document ↗
                                    </a>
                                  )}
                                </article>
                              ))}
                            </div>
                          )}
                        </div>
                      )}
                    </article>
                  )
                })}
              </div>
            )}

            {!fetching && filteredRecommendations.length === 0 && (
              <div className="empty-state">
                <h2>No Interventions for Selected Filter</h2>
                <p>Try switching to "All Action Plans" to view complete sustainability measures for {city}.</p>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
}

export default Recommendations
