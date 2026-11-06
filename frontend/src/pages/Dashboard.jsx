import { useEffect, useState } from 'react'
import { getLiveAirQuality } from '../services/api.js'

function Dashboard({
  onStartAssessment,
  cities = [],
  city = '',
  onCityChange,
  assessment,
  loading,
  apiError,
  onNavigate,
  currentUser,
}) {
  const [liveAir, setLiveAir] = useState(null)
  const [fetchingAir, setFetchingAir] = useState(false)

  useEffect(() => {
    if (!city) return
    let active = true
    setFetchingAir(true)
    getLiveAirQuality(city)
      .then((data) => {
        if (active) setLiveAir(data)
      })
      .catch(() => {
        if (active) setLiveAir(null)
      })
      .finally(() => {
        if (active) setFetchingAir(false)
      })
    return () => {
      active = false
    }
  }, [city])

  const problemCount = assessment?.problem_areas?.length ?? 0
  const attentionCount = assessment?.indicator_classifications?.filter(
    (c) => c.classification === 'Needs Attention'
  ).length ?? 0

  return (
    <div className="dashboard-page">
      <header className="dashboard-header">
        <div>
          <h1>Urban Sustainability Dashboard</h1>
          <p>A Data-Driven Decision Support Framework for Maharashtra Cities (USAS)</p>
        </div>
        <div className="user-info">
          <span>{currentUser?.department ? `${currentUser.name} (${currentUser.role})` : 'Urban Analytics & Planning Cell · Maharashtra'}</span>
        </div>
      </header>

      <main className="dashboard-content">
        {/* WELCOME BANNER */}
        <section className="dashboard-welcome">
          <div>
            <span className="dashboard-eyebrow">DETERMINISTIC DECISION SUPPORT</span>
            <h2>Multi-Criteria Urban Assessment Framework</h2>
            <p>
              USAS evaluates 42 Maharashtra urban centers across five core indicators using the Weighted Sum Model
              with Min-Max normalization. Data provenance, real-world coverage, and evidence-grounded policy interventions
              are reported with full transparency.
            </p>
          </div>
        </section>

        {/* CITY SELECTOR */}
        <section className="city-selection-panel">
          <div className="section-title">
            <span className="section-number">01</span>
            <div>
              <h2>City Assessment Target</h2>
              <p>Select any of the 42 supported Maharashtra urban centers.</p>
            </div>
          </div>

          <div className="city-input-area">
            <div className="city-input-group">
              <label htmlFor="city">City Name</label>
              <select
                id="city"
                value={city}
                onChange={(event) => onCityChange?.(event.target.value)}
                disabled={!cities.length}
              >
                {!cities.length && <option value="">No cities available</option>}
                {cities.map((name) => (
                  <option key={name} value={name}>
                    {name}
                  </option>
                ))}
              </select>
            </div>

            <button
              type="button"
              className="assessment-button"
              onClick={() => onStartAssessment(city)}
              disabled={!city}
            >
              Examine Complete Assessment →
            </button>
          </div>

          <div className="city-selection-note">
            <span>ℹ</span>
            <p>
              Missing indicators are not replaced with zeros. The system re-normalizes weights across available
              measures and reports partial data coverage explicitly.
            </p>
          </div>
        </section>

        {/* HIGH-LEVEL METRICS */}
        <section className="current-assessment">
          <div className="section-title">
            <span className="section-number">02</span>
            <div>
              <h2>Executive Assessment Summary</h2>
              <p>{city ? `${city} · Assessment Date: ${assessment?.assessment_date || 'Current'}` : 'Select a city to begin.'}</p>
            </div>
          </div>

          <div className="assessment-status-grid">
            <div className="status-card">
              <span>Overall Sustainability Score</span>
              <strong className={assessment?.overall_score != null ? 'status-value-highlight' : 'status-value-muted'}>
                {assessment?.overall_score != null ? `${assessment.overall_score} / 100` : '—'}
              </strong>
              <small>{assessment ? `${assessment.score_status} Assessment` : 'Awaiting data'}</small>
            </div>

            <div className="status-card">
              <span>Data Coverage</span>
              <strong>{assessment ? `${assessment.data_coverage_pct}%` : '—'}</strong>
              <small>{assessment ? `${assessment.available_indicator_count} of 5 indicators available` : 'Not computed'}</small>
            </div>

            <div className="status-card">
              <span>Identified Issues</span>
              <strong style={{ color: problemCount > 0 ? '#dc2626' : '#059669' }}>
                {problemCount} Problem · {attentionCount} Attention
              </strong>
              <small>{assessment ? 'Threshold-based evaluation' : 'Awaiting city'}</small>
            </div>

            <div className="status-card">
              <span>Live Air Quality (OpenAQ)</span>
              <strong>
                {fetchingAir
                  ? 'Connecting to OpenAQ...'
                  : liveAir?.status === 'LIVE'
                  ? `AQI: ${liveAir.aqi ?? '—'} (PM2.5: ${liveAir.pm25} µg/m³)`
                  : liveAir?.status === 'CACHED'
                  ? `Cached AQI: ${liveAir.aqi ?? '—'} (PM2.5: ${liveAir.pm25})`
                  : 'CPCB CAAQMS Baseline'}
              </strong>
              <small>
                {liveAir?.status === 'LIVE'
                  ? `🟢 Live 2026 Telemetry · Station #${liveAir.station_id}`
                  : liveAir?.status === 'CACHED'
                  ? `🟡 Cached 2026 Telemetry · Station #${liveAir.station_id}`
                  : 'Latest 2026 CAAQMS Baseline'}
              </small>
            </div>
          </div>
        </section>

        {apiError && (
          <section className="assessment-message" role="alert">
            <p>Analytics Service Notice: {apiError}. Check network connection or verify service status.</p>
          </section>
        )}

        {/* FIVE INDICATOR BREAKDOWN */}
        {assessment && (
          <section className="indicator-breakdown-section">
            <div className="section-title">
              <span className="section-number">03</span>
              <div>
                <h2>Five Core Indicators Breakdown</h2>
                <p>Transparent raw values, normalized 0–100 scores, and source provenance.</p>
              </div>
            </div>

            <div className="indicator-cards-grid">
              {assessment.indicators.map((item) => {
                const isProxy = item.is_proxy || (!item.available && item.value != null)
                const classification =
                  item.score != null
                    ? item.score < 40
                      ? 'Problem Area'
                      : item.score < 60
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

                const formattedVal =
                  item.value != null
                    ? typeof item.value === 'number'
                      ? item.value >= 1000
                        ? item.value.toLocaleString(undefined, { maximumFractionDigits: 1 })
                        : item.value % 1 === 0
                        ? item.value.toString()
                        : item.value.toFixed(2)
                      : item.value
                    : 'Not Available'

                return (
                  <div className="indicator-summary-card" key={item.key}>
                    <div className="indicator-summary-header">
                      <h3>{item.name}</h3>
                      <span className={`status-badge ${badgeClass}`}>{classification}</span>
                    </div>

                    <div className="indicator-score-row">
                      <div className="score-display">
                        <span className="score-value">
                          {item.score != null ? item.score : isProxy ? 'N/A' : '—'}
                        </span>
                        {item.score != null && <span className="score-max">/ 100</span>}
                      </div>
                      <div className="raw-display">
                        <span className="raw-value">
                          {formattedVal} {item.unit && <span className="unit-sub">{item.unit}</span>}
                        </span>
                        <small className="raw-year">Ref: {item.reference_year || 'Historical'}{item.is_live ? ' · 🟢 Live Telemetry' : ''}</small>
                      </div>
                    </div>

                    {item.score != null && (
                      <div className="score-progress-bar">
                        <div
                          className="score-progress-fill"
                          style={{
                            width: `${Math.min(100, Math.max(0, item.score || 0))}%`,
                            backgroundColor:
                              (item.score || 0) < 40
                                ? '#dc2626'
                                : (item.score || 0) < 60
                                ? '#d97706'
                                : '#16a34a',
                          }}
                        ></div>
                      </div>
                    )}

                    {isProxy && (
                      <div className="proxy-indicator-pill" style={{ background: '#f3f4f6', color: '#4b5563', border: '1px solid #e5e7eb' }}>
                        <span>Non-scoring contextual baseline (MoRTH / MMVD Registry)</span>
                      </div>
                    )}

                    <p className="indicator-metric-desc">{item.metric_description}</p>

                    <div className="indicator-source-meta">
                      <small>Source: {item.source || item.source_file || 'Official Repository Data'}</small>
                    </div>
                  </div>
                )
              })}
            </div>
          </section>
        )}

        {/* QUICK NAVIGATION ACTION TILES */}
        {assessment && (
          <section className="action-tiles-section">
            <div className="section-title">
              <span className="section-number">04</span>
              <div>
                <h2>Decision Support Workflow</h2>
                <p>Explore diagnostic indicators, grounded policy evidence, and hypothetical scenarios.</p>
              </div>
            </div>

            <div className="action-tiles-grid">
              <div
                className="action-tile"
                onClick={() => onNavigate?.('indicators')}
                role="button"
                tabIndex={0}
              >
                <div className="tile-icon">📈</div>
                <h3>Core Indicators</h3>
                <p>
                  Inspect transparent raw values, normalized 0–100 scores, reference years, and source provenance.
                </p>
                <span className="tile-link">Explore Indicators →</span>
              </div>

              <div
                className="action-tile"
                onClick={() => onNavigate?.('recommendations')}
                role="button"
                tabIndex={0}
              >
                <div className="tile-icon">📚</div>
                <h3>Grounded Recommendations</h3>
                <p>
                  Retrieve NCAP, URDPFI, MPCB, and TOD policy evidence via FAISS and generate interventions with Gemini.
                </p>
                <span className="tile-link">View Policy Evidence →</span>
              </div>

              <div
                className="action-tile"
                onClick={() => onNavigate?.('impact')}
                role="button"
                tabIndex={0}
              >
                <div className="tile-icon">📊</div>
                <h3>Impact Analysis</h3>
                <p>
                  Model hypothetical score adjustments and recalculate the overall WSM sustainability score before-and-after.
                </p>
                <span className="tile-link">Run Scenario Model →</span>
              </div>

              <div
                className="action-tile"
                onClick={() => onNavigate?.('reports')}
                role="button"
                tabIndex={0}
              >
                <div className="tile-icon">📄</div>
                <h3>Full Assessment Report</h3>
                <p>
                  Generate the comprehensive decision-support report with source provenance, coverage, and limitations.
                </p>
                <span className="tile-link">Generate Report →</span>
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  )
}

export default Dashboard
