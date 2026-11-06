function Assessment({ city, assessment, loading, apiError, onBack }) {
  if (!city) {
    return (
      <div className="content-page">
        <header className="content-page-header">
          <div>
            <h1>Urban Sustainability Assessment</h1>
            <p>USAS Comprehensive Assessment Module</p>
          </div>
          <button type="button" className="back-button" onClick={onBack}>
            Back to Dashboard
          </button>
        </header>
        <main className="content-page-body">
          <div className="empty-state">
            <h2>No City Selected</h2>
            <p>Please select a city from the dashboard to review the complete sustainability assessment.</p>
          </div>
        </main>
      </div>
    )
  }

  const indicators = assessment?.indicators ?? []
  const overallScore = assessment?.overall_score
  const coverage = assessment?.data_coverage_pct ?? 0
  const availableCount = assessment?.available_indicator_count ?? 0

  // Derive highest and lowest scoring indicators
  const scoredIndicators = indicators.filter((i) => i.score != null)
  const strongest = scoredIndicators.length
    ? scoredIndicators.reduce((prev, curr) => (curr.score > prev.score ? curr : prev), scoredIndicators[0])
    : null
  const critical = scoredIndicators.length
    ? scoredIndicators.reduce((prev, curr) => (curr.score < prev.score ? curr : prev), scoredIndicators[0])
    : null

  const formatRawValue = (item) => {
    if (item.value == null) return 'Data pending'
    if (typeof item.value === 'number') {
      if (item.value >= 1000) {
        return item.value.toLocaleString(undefined, { maximumFractionDigits: 1 })
      }
      return item.value % 1 === 0 ? item.value.toString() : item.value.toFixed(2)
    }
    return item.value
  }

  return (
    <div className="content-page assessment-page">
      <header className="content-page-header">
        <div>
          <h1>Urban Sustainability Assessment: {city}</h1>
          <p>
            Deterministic Multi-Criteria Decision Making (MCDM) evaluation across five core urban sustainability indicators.
          </p>
        </div>
        <button type="button" className="back-button" onClick={onBack}>
          ← Back to Dashboard
        </button>
      </header>

      <main className="content-page-body">
        {loading && (
          <div className="loading-card">
            <p>Loading comprehensive assessment for {city}…</p>
          </div>
        )}

        {apiError && (
          <div className="error-card" role="alert">
            {apiError}
          </div>
        )}

        {assessment && (
          <>
            {/* EXECUTIVE ASSESSMENT HERO BANNER */}
            <section className="assessment-hero-card">
              <div className="hero-left">
                <span className="hero-eyebrow">EXECUTIVE SCORECARD</span>
                <h2>{city} Sustainability Assessment</h2>
                <p className="hero-desc">
                  Evaluated using the Weighted Sum Model (WSM) with Min-Max normalization relative to the 42-city
                  Maharashtra baseline dataset. Reference years and source provenance are preserved for full statutory and analytical explainability.
                </p>

                <div className="hero-meta-row">
                  <div className="hero-meta-item">
                    <span>Assessment Date</span>
                    <strong>{assessment.assessment_date}</strong>
                  </div>
                  <div className="hero-meta-item">
                    <span>Data Coverage</span>
                    <strong>{coverage}% ({availableCount} of 5 Indicators)</strong>
                  </div>
                  <div className="hero-meta-item">
                    <span>Audit Status</span>
                    <strong>{assessment.score_status} Assessment</strong>
                  </div>
                </div>
              </div>

              <div className="hero-right">
                <div className="score-dial">
                  <span className="score-dial-num">
                    {overallScore != null ? overallScore : '—'}
                  </span>
                  <span className="score-dial-max">/ 100</span>
                  <small className="score-dial-label">Overall Index Score</small>
                </div>
              </div>
            </section>

            {/* KEY FINDINGS BANNER */}
            <div className="assessment-highlights-grid">
              <div className="highlight-card card-primary">
                <span className="highlight-tag">Top Performing Asset</span>
                <h3>{strongest ? strongest.name : 'Awaiting data'}</h3>
                <p>
                  {strongest
                    ? `Highest normalized performance at ${strongest.score}/100 (${formatRawValue(strongest)} ${strongest.unit}).`
                    : 'All indicators performing within comparable bands.'}
                </p>
              </div>

              <div className="highlight-card card-critical">
                <span className="highlight-tag tag-critical">Primary Priority Challenge</span>
                <h3>{critical && critical.score < 40 ? critical.name : 'No Critical Deficit'}</h3>
                <p>
                  {critical && critical.score < 40
                    ? `Lowest normalized score at ${critical.score}/100 (${formatRawValue(critical)} ${critical.unit}); requires immediate intervention.`
                    : 'All scored indicators satisfy the minimum threshold (>40/100). Focus on targeted optimization.'}
                </p>
              </div>

              <div className="highlight-card card-method">
                <span className="highlight-tag tag-method">Methodology</span>
                <h3>Weighted Sum Model (Equal 20%)</h3>
                <p>
                  Configured indicator weights are equally balanced at 0.20 per indicator. Available weights are re-normalized
                  proportionately for partial datasets without synthetic zero substitution.
                </p>
              </div>
            </div>

            {/* 5-INDICATOR DETAILED SCORECARDS */}
            <section className="assessment-detail-section">
              <div className="section-title">
                <h2>Five Core Indicators Comprehensive Breakdown</h2>
                <p>Transparent empirical values, normalized scores, reference years, and institutional data sources.</p>
              </div>

              <div className="detailed-indicators-grid">
                {indicators.map((item) => {
                  const isProxy = item.is_proxy || (!item.available && item.value != null)
                  const score = item.score

                  const classification =
                    score != null
                      ? score < 40
                        ? 'Problem Area'
                        : score < 60
                        ? 'Needs Attention'
                        : 'Acceptable'
                      : isProxy
                      ? 'N/A (Excluded)'
                      : 'Unavailable'

                  const badgeClass =
                    classification === 'Problem Area'
                      ? 'badge-problem'
                      : classification === 'Needs Attention'
                      ? 'badge-attention'
                      : classification === 'Acceptable'
                      ? 'badge-acceptable'
                      : 'badge-na'

                  return (
                    <article className="detailed-indicator-card" key={item.key}>
                      <div className="card-top-row">
                        <div>
                          <span className="indicator-sub-tag">Indicator</span>
                          <h3>{item.name}</h3>
                        </div>
                        <span className={`status-badge ${badgeClass}`}>{classification}</span>
                      </div>

                      <div className="card-metrics-row">
                        <div className="metric-box">
                          <span className="metric-box-label">Raw Observed Measure</span>
                          <strong className="metric-box-val">
                            {formatRawValue(item)} <span className="unit-text">{item.unit}</span>
                          </strong>
                          <small className="metric-box-year">
                            Reference Year: {item.reference_year || 'Historical'}
                            {item.is_live && ' · 🟢 Live Telemetry'}
                          </small>
                          {item.is_live && item.live_meta && (
                            <div style={{ marginTop: '4px', fontSize: '11px', color: '#059669', fontWeight: 600 }}>
                              PM2.5: {item.live_meta.pm25} µg/m³ · PM10: {item.live_meta.pm10 || '—'} µg/m³
                            </div>
                          )}
                        </div>

                        <div className="metric-box score-box">
                          <span className="metric-box-label">Normalized Score</span>
                          <strong className="metric-box-val score-highlight">
                            {score != null ? `${score} ` : 'N/A '}
                            {score != null && <span className="unit-text">/ 100</span>}
                          </strong>
                          <small className="metric-box-year">
                            {score != null
                              ? score < 40
                                ? '🔴 Critical Deficit'
                                : score < 60
                                ? '🟡 Needs Attention'
                                : '🟢 Performing Well'
                              : 'Non-Scoring Baseline'}
                          </small>
                        </div>
                      </div>

                      {/* Visual Progress Bar */}
                      {score != null && (
                        <div className="indicator-progress-wrap">
                          <div className="progress-labels">
                            <span>0 (Dataset Min)</span>
                            <span>Score: {score}/100</span>
                            <span>100 (Dataset Max)</span>
                          </div>
                          <div className="progress-track">
                            <div
                              className="progress-bar-fill"
                              style={{
                                width: `${Math.min(100, Math.max(0, score))}%`,
                                backgroundColor: score < 40 ? '#ef4444' : score < 60 ? '#f59e0b' : '#10b981',
                              }}
                            ></div>
                          </div>
                        </div>
                      )}

                      <p className="indicator-notes">{item.metric_description || item.data_note}</p>

                      <div className="indicator-card-footer">
                        <div className="source-info">
                          <strong>Data Source:</strong>{' '}
                          <span>{item.source || item.source_file || 'Official Maharashtra State Repository'}</span>
                          {item.source_page && <span> · Page {item.source_page}</span>}
                          {item.source_url && (
                            <span>
                              {' '}·{' '}
                              <a href={item.source_url} target="_blank" rel="noreferrer" className="source-url-link">
                                Source Link ↗
                              </a>
                            </span>
                          )}
                        </div>
                      </div>
                    </article>
                  )
                })}
              </div>
            </section>

            {/* METHODOLOGICAL TRANSPARENCY CARD */}
            <section className="transparency-card">
              <div className="transparency-header">
                <h3>Methodological Transparency & Analytical Standards</h3>
                <span className="dataset-badge">{coverage}% Data Coverage</span>
              </div>
              <p>
                {assessment.score_method} Scores are relative to the empirical distribution of cities in this comparison dataset
                and do not replace statutory local environmental audits. When traffic congestion data is unavailable,
                registered vehicle volumes are tracked as non-scoring contextual baseline data rather than fabricated as congestion scores, and Traffic is marked N/A and excluded from WSM scoring.
              </p>
            </section>
          </>
        )}
      </main>
    </div>
  )
}

export default Assessment
