// Dynamic API URL: In dev mode defaults to Flask on 127.0.0.1:5000/api; in production uses relative /api
const API_BASE = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://127.0.0.1:5000/api' : '/api')

async function request(path, options = {}) {
  const token = typeof window !== 'undefined' ? localStorage.getItem('usas_auth_token') : null
  const authHeaders = token ? { Authorization: `Bearer ${token}` } : {}

  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders,
      ...options.headers,
    },
    ...options,
  })
  const payload = await response.json().catch(() => ({}))
  if (!response.ok) {
    const errorMsg = payload.error || `Request failed with status ${response.status}`
    const error = new Error(errorMsg)
    error.status = response.status
    error.code = payload.code
    throw error
  }
  return payload
}

// Authentication & Session Management
export const login = (email, password) => request('/auth/login', {
  method: 'POST',
  body: JSON.stringify({ email, password }),
})

export const register = (userData) => request('/auth/register', {
  method: 'POST',
  body: JSON.stringify(userData),
})

export const changePassword = (current_password, new_password) => request('/auth/change-password', {
  method: 'POST',
  body: JSON.stringify({ current_password, new_password }),
})

export const getMe = () => request('/auth/me')

export const logout = async () => {
  try {
    await request('/auth/logout', { method: 'POST' })
  } finally {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('usas_auth_token')
      localStorage.removeItem('usas_user_profile')
    }
  }
}

// Administrator Verification & User Access Management
export const getUsers = (status) => request(status ? `/auth/users?status=${encodeURIComponent(status)}` : '/auth/users')
export const getPendingUsers = () => request('/auth/pending-users')
export const approveUser = (userId) => request(`/auth/users/${encodeURIComponent(userId)}/approve`, {
  method: 'POST',
})
export const rejectUser = (userId, reason) => request(`/auth/users/${encodeURIComponent(userId)}/reject`, {
  method: 'POST',
  body: JSON.stringify({ reason }),
})
export const suspendUser = (userId) => request(`/auth/users/${encodeURIComponent(userId)}/suspend`, {
  method: 'POST',
})

// Core Analytics & Reporting Endpoints
export const getHealth = () => request('/health')
export const getCities = () => request('/cities')
export const getAssessment = (city) => request(`/assessment/${encodeURIComponent(city)}`)
export const getAllAssessments = () => request('/assessment')
export const getProblems = (city) => request(`/problems/${encodeURIComponent(city)}`)
export const getLiveAirQuality = (city) => request(`/live/air-quality/${encodeURIComponent(city)}`)
export const getRecommendations = (city) => request(`/recommendations/${encodeURIComponent(city)}`)
export const runImpact = (city, indicator, improvement_points) => request(`/impact/${encodeURIComponent(city)}`, {
  method: 'POST',
  body: JSON.stringify({ indicator, improvement_points }),
})
export const getReport = (city) => request(`/report/${encodeURIComponent(city)}`)
export const getRagStatus = () => request('/rag/status')
export const triggerRagIndex = () => request('/rag/index', { method: 'POST' })

// Publication-Quality PDF Report Download
export const downloadReportPdf = async (city) => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('usas_auth_token') : null
  const authHeaders = token ? { Authorization: `Bearer ${token}` } : {}

  const response = await fetch(`${API_BASE}/report/${encodeURIComponent(city)}/pdf`, {
    headers: { ...authHeaders },
  })

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}))
    throw new Error(payload.error || 'Failed to generate PDF report')
  }

  const blob = await response.blob()
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `USAS_${city}_Sustainability_Report.pdf`
  document.body.appendChild(a)
  a.click()
  a.remove()
  window.URL.revokeObjectURL(url)
}
