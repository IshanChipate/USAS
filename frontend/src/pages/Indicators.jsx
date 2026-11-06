function Indicators({ city, assessment, loading, apiError }) {
  if (!city) {
    return (
      <div className="content-page">
        <header className="content-page-header">
          <div>
            <h1>Sustainability Indicators Explorer</h1>
            <p>Empirical metrics, statutory benchmarks, and data provenance across 42 Maharashtra cities.</p>
          </div>
        </header>
        <main className="content-page-body">
          <div className="empty-state">
            <h2>No City Selected</h2>
            <p>Please select a city from the dashboard to explore detailed indicator statistics.</p>
          </div>
        </main>
      </div>
    )
  }

  const indicators = assessment?.indicators ?? []

  // Contextual statutory benchmarks for indicators
  const BENCHMARKS = {
    'Air Quality': {
      standard: 'CPCB National Ambient Air Quality Standards (NAAQS)',
      benchmarkText: 'Target: AQI ≤ 100 (Satisfactory / Clean air threshold). Values > 100 indicate elevated health risks.',
      category: 'Environmental Quality & Public Health',
    },
    'Waste Management': {
      standard: 'Solid Waste Management (SWM) Rules, 2016 & Swachh Bharat Mission (U) 2.0',
      benchmarkText: 'Target: 100% door-to-door source segregation and scientific processing; zero untreated disposal.',
      category: 'Civic Sanitation & Resource Recovery',
    },
    'Population Density': {
      standard: 'URDPFI Guidelines 2015 (MoHUA Urban Density Norms)',
      benchmarkText: 'Lower density reflects lower stress on water, sewer, and transport networks relative to municipal area.',
      category: 'Demographic Pressure & Carrying Capacity',
    },
    'Green Space': {
      standard: 'URDPFI Open Space Benchmark (10–12 m² per capita)',
      benchmarkText: 'Target: Minimum 10% of municipal land area dedicated to accessible public parks and green spaces.',
      category: 'Urban Ecology & Climate Resilience',
    },
    'Traffic': {
      standard: 'National Urban Transport Policy (NUTP 2014) & MoRTH Mobility Norms',
      benchmarkText: 'Where congestion is scored, TomTom traffic index measures delay. In unmeasured cities, Traffic is excluded from WSM scoring with registered vehicles kept as non-scoring contextual baseline.',
      category: 'Urban Mobility & Network Demand',
    },
  }

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
    <div className="content-page">
      <header className="content-page-header">
        <div>
          <h1>Sustainability Indicators: {city}</h1>
          <p>
            Detailed indicator analysis comparing observed empirical values against state distributions and national benchmarks.
          </p>
        </div>
      </header>

      <main className="content-page-body">
        {/* CITY CONTEXT BANNER */}
        <section className="indicators-overview-banner">
          <div className="overview-text">
            <span className="overview-badge">DATASET PROVENANCE</span>
            <h2>{city} Urban Indicator Profile</h2>
            <p>
              Each indicator is normalized on a 0–100 scale using empirical Min-Max bounds across Maharashtra urban centers.
              Data coverage for {city} is {assessment?.data_coverage_pct ?? 0}%, with {assessment?.available_indicator_count ?? 0} of 5
              indicators directly evaluated in the overall index.
            </p>
          </div>
          <div className="overview-stat-box">
            <span className="stat-label">Coverage Status</span>
            <strong className="stat-value">{assessment?.score_status ?? 'Partial'}</strong>
            <small>{assessment?.available_indicator_count ?? 0} Indicators Scored</small>
          </div>
        </section>

        {loading && (
          <div className="loading-card">
            <p>Loading indicator metrics and provenance data for {city}…</p>
          </div>
        )}

        {apiError && (
          <div className="error-card" role="alert">
            {apiError}
          </div>
        )}

        {/* DETAILED INDICATOR EXPLORER CARDS */}
        {assessment && (
          <div className="indicators-explorer-list">
            {indicators.map((item) => {
              const benchmark = BENCHMARKS[item.name] || {
                standard: 'National Urban Planning Guidelines',
                benchmarkText: 'Standard statutory planning guidance applies.',
                category: 'Urban Performance Measure',
              }

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

              const statusClass =
                classification === 'Problem Area'
                  ? 'status-problem'
                  : classification === 'Needs Attention'
                  ? 'status-attention'
                  : classification === 'Acceptable'
                  ? 'status-acceptable'
                  : 'status-na'

              return (
                <article className="indicator-explorer-card" key={item.key}>
                  {/* Card Header */}
                  <div className="card-header-bar">
                    <div className="header-titles">
                      <span className="category-pill">{benchmark.category}</span>
                      <h2>{item.name}</h2>
                    </div>
                    <div className="header-badges">
                      <span className={`eval-badge ${statusClass}`}>{classification}</span>
                      <span className="availability-pill">
                        {item.available ? 'Scored Indicator' : isProxy ? 'Non-Scoring Baseline' : 'Missing'}
                      </span>
                    </div>
                  </div>

                  {/* Core Metrics Grid */}
                  <div className="metrics-triad-grid">
                    <div className="triad-col">
                      <span className="triad-label">Observed Empirical Value</span>
                      <strong className="triad-value">
                        {formatRawValue(item)} <span className="triad-unit">{item.unit}</span>
                      </strong>
                      <small className="triad-sub">
                        Reference Period: {item.reference_year || 'Historical'}
                        {item.is_live && ' · 🟢 Live'}
                      </small>
                      {item.is_live && item.live_meta && (
                        <div style={{ marginTop: '4px', fontSize: '11px', color: '#059669', fontWeight: 600 }}>
                          PM2.5: {item.live_meta.pm25} µg/m³ · Station #{item.live_meta.station_id}
                        </div>
                      )}
                    </div>

                    <div className="triad-col triad-score">
                      <span className="triad-label">Comparative Score (0–100)</span>
                      <strong className="triad-value score-text">
                        {score != null ? `${score} ` : 'N/A '}
                        {score != null && <span className="triad-unit">/ 100</span>}
                      </strong>
                      <small className="triad-sub">
                        {score != null
                          ? score < 40
                            ? 'Below State Threshold (<40)'
                            : score < 60
                            ? 'Moderate Performance (40–60)'
                            : 'Above State Threshold (≥60)'
                          : 'Non-scoring contextual baseline'}
                      </small>
                    </div>

                    <div className="triad-col triad-weight">
                      <span className="triad-label">WSM Index Weight</span>
                      <strong className="triad-value">20.0%</strong>
                      <small className="triad-sub">Equal weighting scheme</small>
                    </div>
                  </div>

                  {/* Visual Score Meter */}
                  {score != null && (
                    <div className="explorer-meter-section">
                      <div className="meter-labels">
                        <span className="label-crit">Critical (&lt;40)</span>
                        <span className="label-att">Attention (40–60)</span>
                        <span className="label-acc">Acceptable (≥60)</span>
                      </div>
                      <div className="meter-track">
                        <div
                          className="meter-fill"
                          style={{
                            width: `${Math.min(100, Math.max(0, score))}%`,
                            backgroundColor: score < 40 ? '#ef4444' : score < 60 ? '#f59e0b' : '#10b981',
                          }}
                        ></div>
                      </div>
                    </div>
                  )}

                  {/* Planning Benchmark Box */}
                  <div className="benchmark-box">
                    <strong>Statutory Framework & Benchmark:</strong>
                    <p>{benchmark.benchmarkText}</p>
                    <small>Standard: {benchmark.standard}</small>
                  </div>

                  {/* Methodology & Data Provenance */}
                  <div className="provenance-grid">
                    <div>
                      <strong>Indicator Metric Description:</strong>
                      <p>{item.metric_description || item.data_note}</p>
                    </div>
                    <div>
                      <strong>Official Data Source:</strong>
                      <p>
                        {item.source || item.source_file || 'Official Maharashtra State Repository'}
                        {item.source_page ? ` · Page ${item.source_page}` : ''}
                        {item.source_url && (
                          <>
                            {' '}·{' '}
                            <a href={item.source_url} target="_blank" rel="noreferrer" className="provenance-link">
                              Official Document Link ↗
                            </a>
                          </>
                        )}
                      </p>
                    </div>
                  </div>
                </article>
              )
            })}
          </div>
        )}
      </main>
    </div>
  )
}

export default Indicators
