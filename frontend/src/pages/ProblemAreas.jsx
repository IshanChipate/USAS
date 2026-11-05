function ProblemAreas({ city, assessment, loading, apiError, onNavigate }) {
  if (!city) {
    return (
      <div className="content-page">
        <header className="content-page-header">
          <div>
            <h1>Urban Risk & Priority Classification</h1>
            <p>Multi-criteria classification of urban sustainability performance indicators.</p>
          </div>
        </header>
        <main className="content-page-body">
          <div className="empty-state">
            <h2>No City Selected</h2>
            <p>Please select a city from the dashboard to review the urban risk and indicator classifications.</p>
          </div>
        </main>
      </div>
    )
  }

  const classifications = assessment?.indicator_classifications ?? []
  const indicators = assessment?.indicators ?? []

  // Merge classifications with rich indicator metadata
  const enrichedClassifications = classifications.map((item) => {
    const matchedInd = indicators.find((i) => i.key === item.key)
    const isProxy = matchedInd?.is_proxy || (!item.available && item.raw_value != null)
    return {
      ...item,
      isProxy,
      source: matchedInd?.source || 'Official Maharashtra State Repository',
      source_url: matchedInd?.source_url,
      source_page: matchedInd?.source_page,
    }
  })

  // Separate into 4 priority categories
  const criticalItems = enrichedClassifications.filter(
    (item) => item.classification === 'Problem Area'
  )
  const attentionItems = enrichedClassifications.filter(
    (item) => item.classification === 'Needs Attention'
  )
  const acceptableItems = enrichedClassifications.filter(
    (item) => item.classification === 'Acceptable'
  )
  const unmeasuredItems = enrichedClassifications.filter(
    (item) => item.isProxy || item.classification === 'Unavailable'
  )

  const formatRawValue = (item) => {
    if (item.raw_value == null) return 'Data pending'
    if (typeof item.raw_value === 'number') {
      if (item.raw_value >= 1000) {
        return item.raw_value.toLocaleString(undefined, { maximumFractionDigits: 1 })
      }
      return item.raw_value % 1 === 0 ? item.raw_value.toString() : item.raw_value.toFixed(2)
    }
    return item.raw_value
  }

  return (
    <div className="content-page">
      <header className="content-page-header">
        <div>
          <h1>Urban Risk & Priority Matrix: {city}</h1>
          <p>
            Standardized evaluation thresholds: normalized score &lt; 40 triggers a <strong>Problem Area</strong> (High Priority);
            40–59.9 indicates <strong>Needs Attention</strong> (Medium Priority); ≥ 60 is <strong>Acceptable</strong>.
          </p>
        </div>
      </header>

      <main className="content-page-body">
        {/* EXECUTIVE RISK SUMMARY BANNER */}
        <section className="risk-overview-banner">
          <div className="risk-banner-content">
            <span className="risk-eyebrow">RISK & VULNERABILITY AUDIT</span>
            <h2>{city} Indicator Classification Profile</h2>
            <p>
              The system classifies all available empirical measures against uniform state thresholds.
              Problem areas flag critical urban sustainability deficits that demand prioritized municipal budgetary allocation and
              targeted evidence-grounded policy interventions.
            </p>
          </div>

          <div className="risk-stats-row">
            <div className="risk-stat-badge stat-crit">
              <span>Critical Deficits</span>
              <strong>{criticalItems.length}</strong>
              <small>Score &lt; 40 / 100</small>
            </div>
            <div className="risk-stat-badge stat-att">
              <span>Needs Attention</span>
              <strong>{attentionItems.length}</strong>
              <small>Score 40–59.9 / 100</small>
            </div>
            <div className="risk-stat-badge stat-acc">
              <span>Acceptable</span>
              <strong>{acceptableItems.length}</strong>
              <small>Score ≥ 60 / 100</small>
            </div>
            <div className="risk-stat-badge stat-prox">
              <span>Unmeasured (N/A)</span>
              <strong>{unmeasuredItems.length}</strong>
              <small>Excluded from WSM</small>
            </div>
          </div>
        </section>

        {loading && (
          <div className="loading-card">
            <p>Loading indicator classifications and threshold analysis for {city}…</p>
          </div>
        )}

        {apiError && (
          <div className="error-card" role="alert">
            {apiError}
          </div>
        )}

        {assessment && (
          <div className="risk-matrix-container">
            {/* 1. CRITICAL PROBLEM AREAS */}
            <section className="risk-category-section">
              <div className="category-header header-critical">
                <div className="cat-title-wrap">
                  <span className="cat-icon">🔴</span>
                  <div>
                    <h2>Critical Problem Areas (High Severity)</h2>
                    <p>Urgent sustainability gaps falling below the minimum threshold (Score &lt; 40/100).</p>
                  </div>
                </div>
                <span className="cat-count-badge badge-critical">{criticalItems.length} Indicators</span>
              </div>

              {criticalItems.length > 0 ? (
                <div className="risk-cards-grid">
                  {criticalItems.map((item) => (
                    <article className="risk-item-card card-border-critical" key={item.key}>
                      <div className="risk-card-top">
                        <div>
                          <span className="priority-pill pill-critical">Immediate Action Required</span>
                          <h3>{item.indicator}</h3>
                        </div>
                        <div className="risk-score-pill score-critical">
                          <span>Score: {item.score}/100</span>
                        </div>
                      </div>

                      <div className="risk-metric-box">
                        <span className="metric-tag">Observed Baseline</span>
                        <strong>{formatRawValue(item)} {item.unit}</strong>
                        <small>Ref Year: {item.reference_year || 'Historical'}</small>
                      </div>

                      <p className="risk-desc">{item.metric_description}</p>

                      <div className="risk-gap-bar">
                        <div className="gap-text">
                          <span>Threshold Deficit:</span>
                          <strong>{item.score != null ? (40.0 - item.score).toFixed(2) : '—'} points below acceptable baseline</strong>
                        </div>
                        <div className="gap-track">
                          <div
                            className="gap-fill fill-critical"
                            style={{ width: `${Math.max(5, item.score || 0)}%` }}
                          ></div>
                        </div>
                      </div>

                      <div className="risk-card-actions">
                        <button
                          type="button"
                          className="btn-card-action btn-recommendation"
                          onClick={() => onNavigate && onNavigate('recommendations')}
                        >
                          View Action Roadmap →
                        </button>
                      </div>
                    </article>
                  ))}
                </div>
              ) : (
                <div className="empty-category-card">
                  <p>✔ No indicators fell below the critical threshold (&lt;40). All scored measures meet minimum baseline.</p>
                </div>
              )}
            </section>

            {/* 2. PRIORITY ATTENTION NEEDED */}
            <section className="risk-category-section">
              <div className="category-header header-attention">
                <div className="cat-title-wrap">
                  <span className="cat-icon">🟡</span>
                  <div>
                    <h2>Priority Attention Needed (Moderate Priority)</h2>
                    <p>Indicators performing moderately (Score 40–59.9/100) requiring targeted infrastructure upgrades.</p>
                  </div>
                </div>
                <span className="cat-count-badge badge-attention">{attentionItems.length} Indicators</span>
              </div>

              {attentionItems.length > 0 ? (
                <div className="risk-cards-grid">
                  {attentionItems.map((item) => (
                    <article className="risk-item-card card-border-attention" key={item.key}>
                      <div className="risk-card-top">
                        <div>
                          <span className="priority-pill pill-attention">Targeted Upgrades</span>
                          <h3>{item.indicator}</h3>
                        </div>
                        <div className="risk-score-pill score-attention">
                          <span>Score: {item.score}/100</span>
                        </div>
                      </div>

                      <div className="risk-metric-box">
                        <span className="metric-tag">Observed Baseline</span>
                        <strong>{formatRawValue(item)} {item.unit}</strong>
                        <small>Ref Year: {item.reference_year || 'Historical'}</small>
                      </div>

                      <p className="risk-desc">{item.metric_description}</p>

                      <div className="risk-gap-bar">
                        <div className="gap-text">
                          <span>Target Headroom:</span>
                          <strong>{item.score != null ? (60.0 - item.score).toFixed(2) : '—'} points to reach Acceptable tier</strong>
                        </div>
                        <div className="gap-track">
                          <div
                            className="gap-fill fill-attention"
                            style={{ width: `${Math.max(5, item.score || 0)}%` }}
                          ></div>
                        </div>
                      </div>

                      <div className="risk-card-actions">
                        <button
                          type="button"
                          className="btn-card-action"
                          onClick={() => onNavigate && onNavigate('recommendations')}
                        >
                          Review Phased Plan →
                        </button>
                      </div>
                    </article>
                  ))}
                </div>
              ) : (
                <div className="empty-category-card">
                  <p>No indicators currently sit in the moderate attention tier.</p>
                </div>
              )}
            </section>

            {/* 3. ACCEPTABLE PERFORMANCE */}
            <section className="risk-category-section">
              <div className="category-header header-acceptable">
                <div className="cat-title-wrap">
                  <span className="cat-icon">🟢</span>
                  <div>
                    <h2>Acceptable Performance (Strategic Maintenance)</h2>
                    <p>Indicators performing above state baseline (Score ≥ 60/100). Focus on ecological resilience and maintenance.</p>
                  </div>
                </div>
                <span className="cat-count-badge badge-acceptable">{acceptableItems.length} Indicators</span>
              </div>

              {acceptableItems.length > 0 ? (
                <div className="risk-cards-grid">
                  {acceptableItems.map((item) => (
                    <article className="risk-item-card card-border-acceptable" key={item.key}>
                      <div className="risk-card-top">
                        <div>
                          <span className="priority-pill pill-acceptable">Stable Performance</span>
                          <h3>{item.indicator}</h3>
                        </div>
                        <div className="risk-score-pill score-acceptable">
                          <span>Score: {item.score}/100</span>
                        </div>
                      </div>

                      <div className="risk-metric-box">
                        <span className="metric-tag">Observed Baseline</span>
                        <strong>{formatRawValue(item)} {item.unit}</strong>
                        <small>Ref Year: {item.reference_year || 'Historical'}</small>
                      </div>

                      <p className="risk-desc">{item.metric_description}</p>

                      <div className="risk-gap-bar">
                        <div className="gap-text">
                          <span>Performance Status:</span>
                          <strong>Satisfies State Sustainability Baseline</strong>
                        </div>
                        <div className="gap-track">
                          <div
                            className="gap-fill fill-acceptable"
                            style={{ width: `${Math.max(5, item.score || 0)}%` }}
                          ></div>
                        </div>
                      </div>
                    </article>
                  ))}
                </div>
              ) : (
                <div className="empty-category-card">
                  <p>All indicators currently require active intervention.</p>
                </div>
              )}
            </section>

            {/* 4. UNMEASURED / NON-SCORING CONTEXTUAL BASELINE */}
            {unmeasuredItems.length > 0 && (
              <section className="risk-category-section">
                <div className="category-header header-proxy">
                  <div className="cat-title-wrap">
                    <span className="cat-icon">ℹ️</span>
                    <div>
                      <h2>Unmeasured Indicators (Excluded from Scoring)</h2>
                      <p>Indicators without direct empirical telemetry (e.g. traffic congestion outside TomTom coverage) are excluded from WSM scoring to protect data integrity, with registered vehicle counts reported strictly as contextual background.</p>
                    </div>
                  </div>
                  <span className="cat-count-badge badge-proxy">{unmeasuredItems.length} Excluded (N/A)</span>
                </div>

                <div className="risk-cards-grid">
                  {unmeasuredItems.map((item) => (
                    <article className="risk-item-card card-border-proxy" key={item.key}>
                      <div className="risk-card-top">
                        <div>
                          <span className="priority-pill pill-proxy">Contextual Baseline</span>
                          <h3>{item.indicator}</h3>
                        </div>
                        <div className="risk-score-pill score-proxy">
                          <span>N/A (Excluded from Score)</span>
                        </div>
                      </div>

                      <div className="risk-metric-box">
                        <span className="metric-tag">Reported Volume</span>
                        <strong>{formatRawValue(item)} {item.unit}</strong>
                        <small>Ref Year: {item.reference_year || '2022'}</small>
                      </div>

                      <p className="risk-desc">{item.metric_description}</p>
                      <small className="source-note">Source: {item.source || 'Maharashtra Motor Vehicles Department (MMVD)'}</small>
                    </article>
                  ))}
                </div>
              </section>
            )}

            {/* RECOMMENDATIONS WORKFLOW LINK */}
            <section className="recommendation-workflow-card">
              <div className="recommendation-workflow-text">
                <h3>Formulate Grounded Policy Interventions</h3>
                <p>
                  Retrieve verified RAG policy evidence (NCAP, URDPFI, MPCB, TOD) and synthesize contextual recommendations
                  grounded in this city's specific problem areas.
                </p>
              </div>
              <button
                type="button"
                className="btn-open-recommendations"
                onClick={() => onNavigate && onNavigate('recommendations')}
              >
                View Grounded Recommendations →
              </button>
            </section>
          </div>
        )}
      </main>
    </div>
  )
}

export default ProblemAreas
