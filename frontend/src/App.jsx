import { useEffect, useState } from 'react'
import Dashboard from './pages/Dashboard.jsx'
import Assessment from './pages/Assessment.jsx'
import Indicators from './pages/Indicators.jsx'
import ProblemAreas from './pages/ProblemAreas.jsx'
import Recommendations from './pages/Recommendations.jsx'
import ImpactAnalysis from './pages/ImpactAnalysis.jsx'
import Reports from './pages/Reports.jsx'
import UserManagement from './pages/UserManagement.jsx'
import Sidebar from './components/Sidebar.jsx'
import {
  getAssessment,
  getCities,
  login,
  register,
  changePassword,
  getMe,
  logout,
} from './services/api.js'

const VALID_PAGES = [
  'dashboard',
  'assessment',
  'indicators',
  'problems',
  'recommendations',
  'impact',
  'reports',
  'user-management',
]

function parseHashLocation() {
  try {
    const raw = window.location.hash.replace(/^#\/?/, '')
    if (!raw) return { page: null, city: null }
    const [pathPart, queryPart] = raw.split('?')
    const page = VALID_PAGES.includes(pathPart) ? pathPart : null
    let city = null
    if (queryPart) {
      const params = new URLSearchParams(queryPart)
      const c = params.get('city')
      if (c) city = decodeURIComponent(c)
    }
    return { page, city }
  } catch {
    return { page: null, city: null }
  }
}

function getInitialPage() {
  const { page } = parseHashLocation()
  if (page) return page
  try {
    const saved = localStorage.getItem('usas_current_page')
    if (saved && VALID_PAGES.includes(saved)) return saved
  } catch {}
  return 'dashboard'
}

function getInitialCity() {
  const { city } = parseHashLocation()
  if (city) return city
  try {
    const saved = localStorage.getItem('usas_selected_city')
    if (saved) return saved
  } catch {}
  return ''
}

function App() {
  const [currentUser, setCurrentUser] = useState(() => {
    try {
      const stored = localStorage.getItem('usas_user_profile')
      return stored ? JSON.parse(stored) : null
    } catch {
      return null
    }
  })
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    return Boolean(localStorage.getItem('usas_auth_token'))
  })

  const [authMode, setAuthMode] = useState('login') // 'login' or 'register'
  const [authLoading, setAuthLoading] = useState(false)
  const [authError, setAuthError] = useState('')
  const [authSuccess, setAuthSuccess] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [rememberMe, setRememberMe] = useState(true)

  // Login form state (empty defaults - no hardcoded credentials!)
  const [loginEmail, setLoginEmail] = useState('')
  const [loginPassword, setLoginPassword] = useState('')

  // Register form state
  const [regName, setRegName] = useState('')
  const [regEmail, setRegEmail] = useState('')
  const [regPassword, setRegPassword] = useState('')
  const [regDesignation, setRegDesignation] = useState('Urban Planner')
  const [regDepartment, setRegDepartment] = useState('')
  const [regEmployeeId, setRegEmployeeId] = useState('')
  const [regEvidence, setRegEvidence] = useState('')

  // Mandatory First-Login Password Change Modal State
  const [pwdCurrent, setPwdCurrent] = useState('')
  const [pwdNew, setPwdNew] = useState('')
  const [pwdConfirm, setPwdConfirm] = useState('')
  const [pwdLoading, setPwdLoading] = useState(false)
  const [pwdError, setPwdError] = useState('')
  const [pwdSuccess, setPwdSuccess] = useState('')

  // App page state with refresh persistence
  const [currentPage, setCurrentPage] = useState(getInitialPage)
  const [selectedCity, setSelectedCity] = useState(getInitialCity)
  const [cities, setCities] = useState([])
  const [assessment, setAssessment] = useState(null)
  const [loading, setLoading] = useState(false)
  const [apiError, setApiError] = useState('')
  const [impactScenario, setImpactScenario] = useState(null)

  // Sync navigation & selected city to URL hash and localStorage
  useEffect(() => {
    try {
      if (currentPage) localStorage.setItem('usas_current_page', currentPage)
      if (selectedCity) localStorage.setItem('usas_selected_city', selectedCity)
    } catch {}

    const query = selectedCity ? `?city=${encodeURIComponent(selectedCity)}` : ''
    const targetHash = `#/${currentPage}${query}`
    if (window.location.hash !== targetHash) {
      window.history.replaceState(null, '', targetHash)
    }
  }, [currentPage, selectedCity])

  // Handle browser back/forward buttons
  useEffect(() => {
    const handleHashChange = () => {
      const { page, city } = parseHashLocation()
      if (page && page !== currentPage) setCurrentPage(page)
      if (city && city !== selectedCity) setSelectedCity(city)
    }
    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [currentPage, selectedCity])

  // Verify stored session token on mount
  useEffect(() => {
    const token = localStorage.getItem('usas_auth_token')
    if (!token) return

    getMe()
      .then((res) => {
        if (res?.user) {
          setCurrentUser(res.user)
          setIsLoggedIn(true)
          localStorage.setItem('usas_user_profile', JSON.stringify(res.user))
        }
      })
      .catch(() => {
        // Token invalid or expired
        localStorage.removeItem('usas_auth_token')
        localStorage.removeItem('usas_user_profile')
        setCurrentUser(null)
        setIsLoggedIn(false)
      })
  }, [])

  // Load cities once authenticated (preserving existing selection)
  useEffect(() => {
    if (!isLoggedIn) return

    getCities()
      .then(({ cities: availableCities }) => {
        setCities(availableCities)
        if (availableCities.length) {
          setSelectedCity((current) => {
            if (current && availableCities.includes(current)) {
              return current
            }
            const saved = localStorage.getItem('usas_selected_city')
            if (saved && availableCities.includes(saved)) {
              return saved
            }
            return availableCities[0]
          })
        }
      })
      .catch((error) => setApiError(error.message))
  }, [isLoggedIn])

  // Load city assessment data
  useEffect(() => {
    if (!isLoggedIn || !selectedCity) return
    let active = true
    setLoading(true)
    setApiError('')
    getAssessment(selectedCity)
      .then((result) => {
        if (active) setAssessment(result)
      })
      .catch((error) => {
        if (active) {
          setAssessment(null)
          setApiError(error.message)
        }
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [isLoggedIn, selectedCity])

  const handleCityChange = (city) => {
    setSelectedCity(city)
    setImpactScenario(null)
  }

  const handleLoginSubmit = async (event) => {
    event.preventDefault()
    setAuthLoading(true)
    setAuthError('')
    setAuthSuccess('')
    try {
      const res = await login(loginEmail, loginPassword)
      localStorage.setItem('usas_auth_token', res.token)
      localStorage.setItem('usas_user_profile', JSON.stringify(res.user))
      setCurrentUser(res.user)
      setIsLoggedIn(true)
    } catch (err) {
      setAuthError(err.message || 'Authentication failed. Please verify your official credentials.')
    } finally {
      setAuthLoading(false)
    }
  }

  const handleRegisterSubmit = async (event) => {
    event.preventDefault()
    setAuthLoading(true)
    setAuthError('')
    setAuthSuccess('')
    try {
      const res = await register({
        name: regName,
        email: regEmail,
        password: regPassword,
        designation: regDesignation,
        department: regDepartment,
        employee_id: regEmployeeId,
        verification_evidence: regEvidence,
      })
      setAuthSuccess(
        res.message ||
          'Registration submitted successfully with status PENDING_VERIFICATION. An administrator will verify your official credentials before granting access.'
      )
      // Reset sensitive fields
      setRegPassword('')
      setRegEvidence('')
    } catch (err) {
      setAuthError(err.message || 'Registration failed. Please check submitted information.')
    } finally {
      setAuthLoading(false)
    }
  }

  const handlePasswordChangeSubmit = async (event) => {
    event.preventDefault()
    if (pwdNew !== pwdConfirm) {
      setPwdError('New password and confirmation do not match.')
      return
    }
    if (pwdNew.length < 6) {
      setPwdError('New password must be at least 6 characters long.')
      return
    }
    setPwdLoading(true)
    setPwdError('')
    setPwdSuccess('')
    try {
      const res = await changePassword(pwdCurrent, pwdNew)
      setPwdSuccess(res.message || 'Password successfully updated.')
      const updatedUser = { ...currentUser, must_change_password: false }
      setCurrentUser(updatedUser)
      localStorage.setItem('usas_user_profile', JSON.stringify(updatedUser))
      setPwdCurrent('')
      setPwdNew('')
      setPwdConfirm('')
    } catch (err) {
      setPwdError(err.message || 'Failed to update password. Verify current password.')
    } finally {
      setPwdLoading(false)
    }
  }

  const handleLogout = async () => {
    await logout()
    setCurrentUser(null)
    setIsLoggedIn(false)
    setCurrentPage('dashboard')
    try {
      localStorage.removeItem('usas_current_page')
    } catch {}
    window.location.hash = '#/dashboard'
  }

  const handleStartAssessment = (city) => {
    setSelectedCity(city)
    setCurrentPage('assessment')
  }

  const handleNavigate = (page) => {
    setCurrentPage(page)
  }

  const handleBackToDashboard = () => {
    setCurrentPage('dashboard')
  }

  /* AUTHENTICATION VIEW */
  if (!isLoggedIn) {
    return (
      <div className="login-page">
        <div className="login-card" style={{ maxWidth: '480px' }}>
          <div className="login-header">
            <div className="usas-logo">USAS</div>
            <h1>Urban Sustainability</h1>
            <h2>Assessment System</h2>
            <p>
              Government of Maharashtra · Urban Analytics & Decision Support Portal
            </p>
          </div>

          {/* MODE SWITCHER */}
          <div className="auth-mode-switch">
            <button
              type="button"
              className={`auth-tab-btn ${authMode === 'login' ? 'active' : ''}`}
              onClick={() => {
                setAuthMode('login')
                setAuthError('')
                setAuthSuccess('')
              }}
            >
              Official Sign In
            </button>
            <button
              type="button"
              className={`auth-tab-btn ${authMode === 'register' ? 'active' : ''}`}
              onClick={() => {
                setAuthMode('register')
                setAuthError('')
                setAuthSuccess('')
              }}
            >
              Register Official Account
            </button>
          </div>

          {authError && (
            <div className="auth-error-alert" role="alert">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="8" x2="12" y2="12" />
                <line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
              <span>{authError}</span>
            </div>
          )}

          {authSuccess && (
            <div
              style={{
                background: '#ecfdf5',
                border: '1px solid #10b981',
                color: '#065f46',
                padding: '12px 14px',
                borderRadius: '8px',
                marginBottom: '16px',
                fontSize: '13px',
                lineHeight: 1.5,
              }}
              role="status"
            >
              <strong>✓ Submitted for Verification:</strong>
              <p style={{ margin: '4px 0 0 0' }}>{authSuccess}</p>
            </div>
          )}

          {/* SIGN IN FORM */}
          {authMode === 'login' && (
            <form className="login-form" onSubmit={handleLoginSubmit}>
              <div className="form-group">
                <label htmlFor="email">Official Institutional Email Address</label>
                <input
                  type="email"
                  id="email"
                  value={loginEmail}
                  onChange={(e) => setLoginEmail(e.target.value)}
                  placeholder="e.g. officer@usas.gov.in"
                  required
                />
              </div>

              <div className="form-group">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <label htmlFor="password">Authorized Password</label>
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    style={{ background: 'none', border: 'none', color: '#0f766e', fontSize: '12px', cursor: 'pointer', fontWeight: '500' }}
                  >
                    {showPassword ? 'Hide Password' : 'Show Password'}
                  </button>
                </div>
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                  placeholder="Enter your confidential password"
                  required
                />
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px', color: '#4b5563' }}>
                <input
                  type="checkbox"
                  id="rememberMe"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  style={{ width: '16px', height: '16px', cursor: 'pointer', accentColor: '#14532d' }}
                />
                <label htmlFor="rememberMe" style={{ cursor: 'pointer' }}>Keep session active on this workstation</label>
              </div>

              <button
                type="submit"
                className="login-button"
                disabled={authLoading}
              >
                {authLoading ? 'Authenticating...' : 'Sign In to Decision Support System'}
              </button>
            </form>
          )}

          {/* REGISTRATION FORM */}
          {authMode === 'register' && (
            <form className="login-form" onSubmit={handleRegisterSubmit}>
              <div className="form-group">
                <label htmlFor="regName">Full Name</label>
                <input
                  type="text"
                  id="regName"
                  value={regName}
                  onChange={(e) => setRegName(e.target.value)}
                  placeholder="e.g. Smt. Neha Patil"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="regEmail">Official Institutional / Government Email</label>
                <input
                  type="email"
                  id="regEmail"
                  value={regEmail}
                  onChange={(e) => setRegEmail(e.target.value)}
                  placeholder="e.g. neha.patil@punecorp.gov.in"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="regPassword">Access Password (Min 6 chars)</label>
                <input
                  type="password"
                  id="regPassword"
                  value={regPassword}
                  onChange={(e) => setRegPassword(e.target.value)}
                  placeholder="Create secure password"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="regDesignation">Designation</label>
                <input
                  type="text"
                  id="regDesignation"
                  value={regDesignation}
                  onChange={(e) => setRegDesignation(e.target.value)}
                  placeholder="e.g. Assistant Director of Town Planning"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="regDept">Government Department / Municipal Body</label>
                <input
                  type="text"
                  id="regDept"
                  value={regDepartment}
                  onChange={(e) => setRegDepartment(e.target.value)}
                  placeholder="e.g. Pune Municipal Corporation (PMC)"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="regEmpId">Official Employee / Identification Reference</label>
                <input
                  type="text"
                  id="regEmpId"
                  value={regEmployeeId}
                  onChange={(e) => setRegEmployeeId(e.target.value)}
                  placeholder="e.g. MH-PMC-TP-2024-082"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="regEvidence">Verification Reference / Evidence</label>
                <input
                  type="text"
                  id="regEvidence"
                  value={regEvidence}
                  onChange={(e) => setRegEvidence(e.target.value)}
                  placeholder="e.g. Government Resolution / Order No. UDD-2024/CR-12"
                />
              </div>

              <button
                type="submit"
                className="login-button"
                disabled={authLoading}
              >
                {authLoading ? 'Submitting Registration...' : 'Submit Registration for Administrative Approval'}
              </button>
            </form>
          )}

          {/* STATUTORY COMPLIANCE FOOTER */}
          <div className="login-footer">
            <p>Urban Sustainability Assessment System (USAS)</p>
            <span>State Urban Analytics & Decision Support Infrastructure · Restricted Official Access</span>
          </div>
        </div>
      </div>
    )
  }

  /* MANDATORY FIRST-LOGIN PASSWORD CHANGE MODAL */
  if (currentUser?.must_change_password) {
    return (
      <div className="login-page">
        <div className="login-card" style={{ maxWidth: '460px' }}>
          <div className="login-header">
            <div className="usas-logo" style={{ background: '#b45309' }}>🔑</div>
            <h1 style={{ fontSize: '22px' }}>Security Action Required</h1>
            <h2 style={{ fontSize: '18px', color: '#b45309' }}>Update Initial Password</h2>
            <p style={{ fontSize: '13px', lineHeight: 1.5 }}>
              Welcome, <strong>{currentUser.name}</strong>. In accordance with statutory security mandates,
              your initial administrative password must be changed before accessing operational data.
            </p>
          </div>

          {pwdError && (
            <div className="auth-error-alert" role="alert">
              <span>{pwdError}</span>
            </div>
          )}

          {pwdSuccess && (
            <div
              style={{
                background: '#ecfdf5',
                border: '1px solid #10b981',
                color: '#065f46',
                padding: '10px 14px',
                borderRadius: '8px',
                marginBottom: '16px',
                fontSize: '13px',
              }}
            >
              ✓ {pwdSuccess}
            </div>
          )}

          <form className="login-form" onSubmit={handlePasswordChangeSubmit}>
            <div className="form-group">
              <label htmlFor="pwdCurrent">Current Password</label>
              <input
                type="password"
                id="pwdCurrent"
                value={pwdCurrent}
                onChange={(e) => setPwdCurrent(e.target.value)}
                placeholder="Enter current password"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="pwdNew">New Secure Password (Min 6 chars)</label>
              <input
                type="password"
                id="pwdNew"
                value={pwdNew}
                onChange={(e) => setPwdNew(e.target.value)}
                placeholder="Enter new password"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="pwdConfirm">Confirm New Password</label>
              <input
                type="password"
                id="pwdConfirm"
                value={pwdConfirm}
                onChange={(e) => setPwdConfirm(e.target.value)}
                placeholder="Re-enter new password"
                required
              />
            </div>

            <button
              type="submit"
              className="login-button"
              style={{ background: '#b45309' }}
              disabled={pwdLoading}
            >
              {pwdLoading ? 'Updating Password...' : 'Update Password & Access System'}
            </button>

            <button
              type="button"
              onClick={handleLogout}
              style={{
                background: 'transparent',
                border: '1px solid #d1d5db',
                color: '#6b7280',
                padding: '10px',
                borderRadius: '8px',
                fontSize: '13px',
                cursor: 'pointer',
              }}
            >
              Cancel & Sign Out
            </button>
          </form>
        </div>
      </div>
    )
  }

  /* PAGE CONTENT */
  const renderPage = () => {
    if (currentPage === 'dashboard') {
      return (
        <Dashboard
          onStartAssessment={handleStartAssessment}
          cities={cities}
          city={selectedCity}
          onCityChange={handleCityChange}
          assessment={assessment}
          loading={loading}
          apiError={apiError}
          onNavigate={handleNavigate}
          currentUser={currentUser}
        />
      )
    }

    if (currentPage === 'assessment') {
      return (
        <Assessment
          city={selectedCity}
          onBack={handleBackToDashboard}
          assessment={assessment}
          loading={loading}
          apiError={apiError}
          onRefresh={() => setSelectedCity((city) => `${city}`)}
        />
      )
    }

    if (currentPage === 'indicators') {
      return (
        <Indicators
          city={selectedCity}
          assessment={assessment}
          loading={loading}
          apiError={apiError}
        />
      )
    }

    if (currentPage === 'problems') {
      return (
        <ProblemAreas
          city={selectedCity}
          assessment={assessment}
          loading={loading}
          apiError={apiError}
          onNavigate={handleNavigate}
        />
      )
    }

    if (currentPage === 'recommendations') {
      return (
        <Recommendations
          city={selectedCity}
          assessment={assessment}
          loading={loading}
          apiError={apiError}
          onNavigate={handleNavigate}
        />
      )
    }

    if (currentPage === 'impact') {
      return (
        <ImpactAnalysis
          city={selectedCity}
          assessment={assessment}
          loading={loading}
          apiError={apiError}
          onScenarioResult={setImpactScenario}
        />
      )
    }

    if (currentPage === 'reports') {
      return (
        <Reports
          city={selectedCity}
          assessment={assessment}
          loading={loading}
          apiError={apiError}
          impactScenario={impactScenario}
        />
      )
    }

    if (currentPage === 'user-management' && currentUser?.role === 'Administrator') {
      return <UserManagement currentUser={currentUser} />
    }

    return (
      <Dashboard
        onStartAssessment={handleStartAssessment}
        cities={cities}
        city={selectedCity}
        onCityChange={handleCityChange}
        assessment={assessment}
        loading={loading}
        apiError={apiError}
        onNavigate={handleNavigate}
        currentUser={currentUser}
      />
    )
  }

  return (
    <div className="app-layout">
      <Sidebar
        currentPage={currentPage}
        onNavigate={handleNavigate}
        currentUser={currentUser}
        onLogout={handleLogout}
      />
      <div className="app-content">{renderPage()}</div>
    </div>
  )
}

export default App
