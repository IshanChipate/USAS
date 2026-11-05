import { useEffect, useState } from 'react'
import { runImpact } from '../services/api.js'

function ImpactAnalysis({ city, assessment, loading, apiError, onScenarioResult }) {
  const available = assessment?.indicators?.filter((item) => item.available) ?? []
  const [indicator, setIndicator] = useState('')
  const [points, setPoints] = useState(10)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [simulating, setSimulating] = useState(false)

  useEffect(() => {
    setIndicator(available[0]?.key ?? '')
    setResult(null)
    setError('')
  }, [city, assessment])

  const simulate = async (event) => {
    if (event) event.preventDefault()
    setError('')
    setSimulating(true)
    try {
      const selected = indicator || available[0]?.key
      if (!selected) throw new Error('No available indicator can be simulated for this city.')
      const scenario = await runImpact(city, selected, Number(points))
      setResult(scenario)
      onScenarioResult?.(scenario)
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setSimulating(false)
    }
  }

  const selectedIndicatorMeta = available.find((item) => item.key === (indicator || available[0]?.key))

  return (
    <div className="content-page">
      <header className="content-page-header">
        <div>
          <h1>Scenario Impact Analysis Studio</h1>
          <p>
            Deterministic sensitivity modeling: simulate target score improvements and evaluate overall sustainability index response.
          </p>
        </div>
      </header>

      <main className="content-page-body">
        {!city ? (
          <div className="empty-state">
            <h2>No City Selected</h2>
            <p>Please select a city from the dashboard to simulate policy intervention scenarios.</p>
          </div>
        ) : (
          <>
            {/* HERO OVERVIEW BANNER */}
            <section className="impact-hero-banner">
              <div className="impact-hero-text">
                <span className="impact-eyebrow">MCDM SENSITIVITY SIMULATOR</span>
                <h2>{city} Policy Intervention Modeling</h2>
                <p>
                  Explore how targeted capital investments and regulatory reforms translate into overall city sustainability score gains.
                  The simulator applies the Weighted Sum Model (WSM) re-normalized across available indicators:
                  <br />
                  <code className="formula-code">
                    Δ Overall Score = (Δ Indicator Score) × [ Indicator Weight (0.20) / Total Available Weight ]
                  </code>
                </p>
              </div>

              <div className="impact-hero-stats">
                <div className="hero-stat-pill">
                  <span>Current Baseline Score</span>
                  <strong>{assessment?.overall_score != null ? `${assessment.overall_score}/100` : '—'}</strong>
                </div>
                <div className="hero-stat-pill">
                  <span>Simulatable Indicators</span>
                  <strong>{available.length} Scored Measures</strong>
                </div>
              </div>
            </section>

            {loading && (
              <div className="loading-card">
                <p>Loading assessment metrics for scenario modeling…</p>
              </div>
            )}

            {apiError && (
              <div className="error-card" role="alert">
                {apiError}
              </div>
            )}

            {assessment && (
              <div className="simulator-layout-grid">
                {/* SIMULATOR CONTROLS CARD */}
                <form className="simulator-controls-card" onSubmit={simulate}>
                  <div className="card-header-bar">
                    <h3>Configure Intervention Scenario</h3>
                    <span className="control-badge">Interactive Controls</span>
                  </div>

                  {/* Indicator Selection */}
                  <div className="control-group">
                    <label htmlFor="sim-indicator">
                      <strong>Select Target Indicator:</strong>
                      <span className="label-helper">Choose any indicator currently evaluated in the index</span>
                    </label>
                    <select
                      id="sim-indicator"
                      className="sim-select"
                      value={indicator}
                      onChange={(event) => setIndicator(event.target.value)}
                    >
                      {available.map((item) => (
                        <option value={item.key} key={item.key}>
                          {item.name} (Current Score: {item.score}/100 · Raw: {item.value} {item.unit})
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Indicator Quick Metadata */}
                  {selectedIndicatorMeta && (
                    <div className="sim-indicator-summary">
                      <div>
                        <span>Current Raw Measure:</span>
                        <strong>
                          {selectedIndicatorMeta.value} {selectedIndicatorMeta.unit}
                        </strong>
                      </div>
                      <div>
                        <span>Normalized Score:</span>
                        <strong>{selectedIndicatorMeta.score} / 100</strong>
                      </div>
                      <div>
                        <span>Index Weight:</span>
                        <strong>20% (Equal Weight)</strong>
                      </div>
                    </div>
                  )}

                  {/* Slider & Number Input */}
                  <div className="control-group">
                    <div className="slider-label-row">
                      <label htmlFor="sim-slider">
                        <strong>Assumed Score Improvement:</strong>
                      </label>
                      <span className="slider-value-display">+{points} Points</span>
                    </div>

                    <input
                      id="sim-slider"
                      type="range"
                      min="1"
                      max="50"
                      value={points}
                      onChange={(event) => setPoints(Number(event.target.value))}
                      className="sim-range-slider"
                    />

                    <div className="slider-ticks">
                      <span>+1 pt</span>
                      <span>+10 pts</span>
                      <span>+25 pts</span>
                      <span>+50 pts</span>
                    </div>
                  </div>

                  {/* Quick Preset Buttons */}
                  <div className="preset-buttons-row">
                    <button
                      type="button"
                      className={`preset-btn ${points === 5 ? 'active' : ''}`}
                      onClick={() => setPoints(5)}
                    >
                      +5 pts (Operational)
                    </button>
                    <button
                      type="button"
                      className={`preset-btn ${points === 10 ? 'active' : ''}`}
                      onClick={() => setPoints(10)}
                    >
                      +10 pts (Capital Works)
                    </button>
                    <button
                      type="button"
                      className={`preset-btn ${points === 20 ? 'active' : ''}`}
                      onClick={() => setPoints(20)}
                    >
                      +20 pts (Systemic Reform)
                    </button>
                  </div>

                  {/* Submit Button */}
                  <button
                    type="submit"
                    className="btn-run-simulation"
                    disabled={!available.length || simulating}
                  >
                    {simulating ? 'Computing WSM Projection…' : 'Simulate Scenario Impact →'}
                  </button>

                  {error && (
                    <div className="sim-error-box" role="alert">
                      {error}
                    </div>
                  )}
                </form>

                {/* SIMULATION RESULTS CARD */}
                <div className="simulator-results-panel">
                  {result ? (
                    <div className="results-card">
                      <div className="results-header">
                        <div>
                          <span className="results-badge">PROJECTION OUTPUT</span>
                          <h2>{result.indicator} Intervention Scenario</h2>
                        </div>
                        <span className="delta-badge">
                          +{Number(result.overall_score_change).toFixed(2)} Overall Index Gain
                        </span>
                      </div>

                      {/* Before / After Dual Cards */}
                      <div className="before-after-grid">
                        <div className="ba-card">
                          <span className="ba-label">Target Indicator Score</span>
                          <div className="ba-score-row">
                            <span className="ba-old">{result.baseline_indicator_score}</span>
                            <span className="ba-arrow">→</span>
                            <span className="ba-new">{result.projected_indicator_score}</span>
                            <span className="ba-delta">
                              (+{result.effective_normalized_score_change_points})
                            </span>
                          </div>
                          <div className="ba-meter-track">
                            <div
                              className="ba-meter-fill"
                              style={{ width: `${Math.min(100, result.projected_indicator_score)}%` }}
                            ></div>
                          </div>
                          <small>Scale: 0–100 · Capped at 100 max</small>
                        </div>

                        <div className="ba-card ba-highlight">
                          <span className="ba-label">Overall City Sustainability Score</span>
                          <div className="ba-score-row">
                            <span className="ba-old">{result.baseline_overall_score}</span>
                            <span className="ba-arrow">→</span>
                            <span className="ba-new">{result.projected_overall_score}</span>
                            <span className="ba-delta delta-overall">
                              (+{Number(result.overall_score_change).toFixed(2)})
                            </span>
                          </div>
                          <div className="ba-meter-track">
                            <div
                              className="ba-meter-fill fill-overall"
                              style={{ width: `${Math.min(100, result.projected_overall_score)}%` }}
                            ></div>
                          </div>
                          <small>Weighted across all available city indicators</small>
                        </div>
                      </div>

                      {/* Methodological Assumptions & Constraints */}
                      <div className="assumptions-box">
                        <h4>Model Assumptions & Constraints</h4>
                        <ul>
                          {result.assumptions.map((assump, idx) => (
                            <li key={idx}>{assump}</li>
                          ))}
                        </ul>
                        <div className="persistence-note">
                          <span>Audit Record Status:</span>{' '}
                          {result.persistence?.saved ? 'Scenario logged to MongoDB.' : 'Active in local session cache (MongoDB optional).'}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="results-placeholder">
                      <div className="placeholder-icon">📊</div>
                      <h3>Ready to Run Simulation</h3>
                      <p>
                        Select an indicator and assumed score gain on the left, then click{' '}
                        <strong>"Simulate Scenario Impact"</strong> to compute before and after metrics.
                      </p>
                    </div>
                  )}
                </div>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
}

export default ImpactAnalysis
