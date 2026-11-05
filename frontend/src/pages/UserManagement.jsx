import { useEffect, useState } from 'react'
import {
  getUsers,
  approveUser,
  rejectUser,
  suspendUser,
} from '../services/api.js'

function UserManagement({ currentUser }) {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [successMsg, setSuccessMsg] = useState('')
  const [rejectingId, setRejectingId] = useState(null)
  const [rejectReason, setRejectReason] = useState('')
  const [actionLoading, setActionLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('pending') // 'pending' | 'all'

  const fetchUsers = async () => {
    setLoading(true)
    setError('')
    try {
      const res = await getUsers()
      if (res && res.users) {
        setUsers(res.users)
      }
    } catch (err) {
      setError(err.message || 'Failed to fetch stakeholder accounts.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchUsers()
  }, [])

  const handleApprove = async (userId, name) => {
    if (!window.confirm(`Confirm verification and approval of official account for ${name}?`)) {
      return
    }
    setActionLoading(true)
    setError('')
    setSuccessMsg('')
    try {
      const res = await approveUser(userId)
      setSuccessMsg(res.message || `Account for ${name} has been approved.`)
      await fetchUsers()
    } catch (err) {
      setError(err.message || 'Failed to approve account.')
    } finally {
      setActionLoading(false)
    }
  }

  const handleRejectSubmit = async (userId, name) => {
    if (!rejectReason.trim()) {
      alert('Please provide an official rejection reason.')
      return
    }
    setActionLoading(true)
    setError('')
    setSuccessMsg('')
    try {
      const res = await rejectUser(userId, rejectReason.trim())
      setSuccessMsg(res.message || `Registration for ${name} was rejected.`)
      setRejectingId(null)
      setRejectReason('')
      await fetchUsers()
    } catch (err) {
      setError(err.message || 'Failed to reject registration.')
    } finally {
      setActionLoading(false)
    }
  }

  const handleSuspend = async (userId, name) => {
    if (!window.confirm(`Are you sure you want to suspend access for ${name}?`)) {
      return
    }
    setActionLoading(true)
    setError('')
    setSuccessMsg('')
    try {
      const res = await suspendUser(userId)
      setSuccessMsg(res.message || `Account for ${name} has been suspended.`)
      await fetchUsers()
    } catch (err) {
      setError(err.message || 'Failed to suspend account.')
    } finally {
      setActionLoading(false)
    }
  }

  const pendingUsers = users.filter((u) => u.status === 'PENDING_VERIFICATION')
  const displayedUsers = activeTab === 'pending' ? pendingUsers : users

  return (
    <div className="page-container">
      <header className="page-header">
        <div>
          <span className="page-tag">ADMINISTRATIVE SECURITY & ACCESS CONTROL</span>
          <h1 className="page-title">Stakeholder Account Verification</h1>
          <p className="page-subtitle">
            Statutory credential review and role-based access authorization for municipal planning officials
          </p>
        </div>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <button
            type="button"
            className="header-action-button"
            onClick={fetchUsers}
            disabled={loading || actionLoading}
          >
            ↻ Refresh Records
          </button>
        </div>
      </header>

      {/* STATUTORY NOTICE BANNER */}
      <div
        style={{
          background: '#f0fdf4',
          border: '1px solid #bbf7d0',
          borderRadius: '10px',
          padding: '14px 18px',
          marginBottom: '20px',
          display: 'flex',
          gap: '12px',
          alignItems: 'flex-start',
        }}
      >
        <span style={{ fontSize: '20px' }}>🛡️</span>
        <div>
          <strong style={{ color: '#166534', fontSize: '14px', display: 'block', marginBottom: '2px' }}>
            Data Integrity & Access Authorization Protocol
          </strong>
          <p style={{ color: '#14532d', fontSize: '13px', margin: 0, lineHeight: 1.5 }}>
            To safeguard municipal sustainability decision models and underlying state datasets, public registrations
            are quarantined under <code>PENDING_VERIFICATION</code>. Only after verifying official departmental credentials,
            institutional email domain, and employee reference may an Administrator grant active system access.
          </p>
        </div>
      </div>

      {error && (
        <div className="auth-error-alert" style={{ marginBottom: '16px' }} role="alert">
          <span>{error}</span>
        </div>
      )}

      {successMsg && (
        <div
          style={{
            background: '#ecfdf5',
            border: '1px solid #10b981',
            color: '#065f46',
            padding: '12px 16px',
            borderRadius: '8px',
            marginBottom: '16px',
            fontSize: '13px',
            fontWeight: 500,
          }}
        >
          ✓ {successMsg}
        </div>
      )}

      {/* FILTER TABS */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '18px' }}>
        <button
          type="button"
          onClick={() => setActiveTab('pending')}
          style={{
            padding: '8px 16px',
            borderRadius: '6px',
            border: '1px solid',
            borderColor: activeTab === 'pending' ? '#0f766e' : '#d1d5db',
            background: activeTab === 'pending' ? '#0f766e' : '#ffffff',
            color: activeTab === 'pending' ? '#ffffff' : '#374151',
            fontWeight: 600,
            fontSize: '13px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}
        >
          <span>Pending Verification</span>
          <span
            style={{
              background: activeTab === 'pending' ? '#134e4a' : '#e5e7eb',
              color: activeTab === 'pending' ? '#ffffff' : '#1f2937',
              padding: '2px 7px',
              borderRadius: '10px',
              fontSize: '11px',
            }}
          >
            {pendingUsers.length}
          </span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab('all')}
          style={{
            padding: '8px 16px',
            borderRadius: '6px',
            border: '1px solid',
            borderColor: activeTab === 'all' ? '#0f766e' : '#d1d5db',
            background: activeTab === 'all' ? '#0f766e' : '#ffffff',
            color: activeTab === 'all' ? '#ffffff' : '#374151',
            fontWeight: 600,
            fontSize: '13px',
            cursor: 'pointer',
          }}
        >
          All Stakeholder Accounts ({users.length})
        </button>
      </div>

      {loading ? (
        <div style={{ padding: '40px', textAlign: 'center', color: '#6b7280' }}>
          Loading stakeholder records...
        </div>
      ) : displayedUsers.length === 0 ? (
        <div
          style={{
            padding: '48px',
            textAlign: 'center',
            background: '#ffffff',
            borderRadius: '12px',
            border: '1px solid #e5e7eb',
          }}
        >
          <div style={{ fontSize: '32px', marginBottom: '8px' }}>✓</div>
          <h3 style={{ fontSize: '16px', color: '#111827', margin: '0 0 6px 0' }}>
            {activeTab === 'pending' ? 'No Pending Registrations' : 'No Accounts Found'}
          </h3>
          <p style={{ fontSize: '13px', color: '#6b7280', margin: 0 }}>
            {activeTab === 'pending'
              ? 'All prospective government officials have been processed.'
              : 'No stakeholder accounts are provisioned.'}
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {displayedUsers.map((user) => {
            const isSelf = user.id === currentUser?.id
            const isPending = user.status === 'PENDING_VERIFICATION'
            const isActive = user.status === 'ACTIVE'
            const isSuspended = user.status === 'SUSPENDED'
            const isRejected = user.status === 'REJECTED'

            const statusColor = isPending
              ? { bg: '#fef3c7', text: '#92400e', border: '#fcd34d' }
              : isActive
              ? { bg: '#dcfce7', text: '#166534', border: '#86efac' }
              : isSuspended
              ? { bg: '#fee2e2', text: '#991b1b', border: '#fca5a5' }
              : { bg: '#f3f4f6', text: '#374151', border: '#d1d5db' }

            return (
              <div
                key={user.id}
                style={{
                  background: '#ffffff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '10px',
                  padding: '18px 20px',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
                }}
              >
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'flex-start',
                    marginBottom: '12px',
                    flexWrap: 'wrap',
                    gap: '10px',
                  }}
                >
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <h3 style={{ margin: 0, fontSize: '16px', fontWeight: 600, color: '#111827' }}>
                        {user.name}
                      </h3>
                      <span
                        style={{
                          background: statusColor.bg,
                          color: statusColor.text,
                          border: `1px solid ${statusColor.border}`,
                          fontSize: '11px',
                          fontWeight: 700,
                          padding: '2px 8px',
                          borderRadius: '12px',
                          textTransform: 'uppercase',
                        }}
                      >
                        {user.status}
                      </span>
                      {user.role === 'Administrator' && (
                        <span
                          style={{
                            background: '#e0e7ff',
                            color: '#3730a3',
                            border: '1px solid #c7d2fe',
                            fontSize: '11px',
                            fontWeight: 700,
                            padding: '2px 8px',
                            borderRadius: '12px',
                          }}
                        >
                          Administrator
                        </span>
                      )}
                    </div>
                    <span style={{ fontSize: '13px', color: '#4b5563', display: 'block', marginTop: '2px' }}>
                      {user.email}
                    </span>
                  </div>

                  {/* ACTION CONTROLS */}
                  {!isSelf && (
                    <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                      {isPending && (
                        <>
                          <button
                            type="button"
                            onClick={() => handleApprove(user.id, user.name)}
                            disabled={actionLoading}
                            style={{
                              padding: '6px 14px',
                              background: '#15803d',
                              color: '#ffffff',
                              border: 'none',
                              borderRadius: '6px',
                              fontSize: '12px',
                              fontWeight: 600,
                              cursor: 'pointer',
                            }}
                          >
                            ✓ Verify & Approve
                          </button>
                          <button
                            type="button"
                            onClick={() => setRejectingId(rejectingId === user.id ? null : user.id)}
                            disabled={actionLoading}
                            style={{
                              padding: '6px 14px',
                              background: '#b91c1c',
                              color: '#ffffff',
                              border: 'none',
                              borderRadius: '6px',
                              fontSize: '12px',
                              fontWeight: 600,
                              cursor: 'pointer',
                            }}
                          >
                            ✕ Reject
                          </button>
                        </>
                      )}

                      {isActive && user.role !== 'Administrator' && (
                        <button
                          type="button"
                          onClick={() => handleSuspend(user.id, user.name)}
                          disabled={actionLoading}
                          style={{
                            padding: '6px 12px',
                            background: '#ffffff',
                            color: '#b91c1c',
                            border: '1px solid #f87171',
                            borderRadius: '6px',
                            fontSize: '12px',
                            fontWeight: 600,
                            cursor: 'pointer',
                          }}
                        >
                          Suspend Access
                        </button>
                      )}

                      {isSuspended && (
                        <button
                          type="button"
                          onClick={() => handleApprove(user.id, user.name)}
                          disabled={actionLoading}
                          style={{
                            padding: '6px 12px',
                            background: '#15803d',
                            color: '#ffffff',
                            border: 'none',
                            borderRadius: '6px',
                            fontSize: '12px',
                            fontWeight: 600,
                            cursor: 'pointer',
                          }}
                        >
                          Reactivate Account
                        </button>
                      )}
                    </div>
                  )}
                </div>

                {/* DETAILS GRID */}
                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                    gap: '12px',
                    padding: '12px',
                    background: '#f9fafb',
                    borderRadius: '8px',
                    fontSize: '13px',
                  }}
                >
                  <div>
                    <span style={{ color: '#6b7280', fontSize: '11px', textTransform: 'uppercase', display: 'block' }}>
                      Designation
                    </span>
                    <strong style={{ color: '#1f2937' }}>{user.designation || '—'}</strong>
                  </div>
                  <div>
                    <span style={{ color: '#6b7280', fontSize: '11px', textTransform: 'uppercase', display: 'block' }}>
                      Department / Organization
                    </span>
                    <strong style={{ color: '#1f2937' }}>{user.department || '—'}</strong>
                  </div>
                  <div>
                    <span style={{ color: '#6b7280', fontSize: '11px', textTransform: 'uppercase', display: 'block' }}>
                      Official Employee / ID Ref
                    </span>
                    <strong style={{ color: '#1f2937' }}>{user.employee_id || '—'}</strong>
                  </div>
                  <div>
                    <span style={{ color: '#6b7280', fontSize: '11px', textTransform: 'uppercase', display: 'block' }}>
                      Verification Evidence
                    </span>
                    <span style={{ color: '#374151' }}>{user.verification_evidence || '—'}</span>
                  </div>
                </div>

                {isRejected && user.rejection_reason && (
                  <div
                    style={{
                      marginTop: '10px',
                      padding: '8px 12px',
                      background: '#fee2e2',
                      borderRadius: '6px',
                      fontSize: '12px',
                      color: '#991b1b',
                    }}
                  >
                    <strong>Rejection Reason:</strong> {user.rejection_reason}
                  </div>
                )}

                {/* REJECT MODAL / INPUT */}
                {rejectingId === user.id && (
                  <div
                    style={{
                      marginTop: '12px',
                      padding: '12px',
                      background: '#fef2f2',
                      border: '1px solid #fecaca',
                      borderRadius: '8px',
                    }}
                  >
                    <label
                      htmlFor={`reject-reason-${user.id}`}
                      style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: '#991b1b', marginBottom: '6px' }}
                    >
                      Official Rejection Justification
                    </label>
                    <input
                      id={`reject-reason-${user.id}`}
                      type="text"
                      value={rejectReason}
                      onChange={(e) => setRejectReason(e.target.value)}
                      placeholder="e.g. Employee ID could not be validated against department roster."
                      style={{
                        width: '100%',
                        padding: '8px 10px',
                        borderRadius: '6px',
                        border: '1px solid #f87171',
                        fontSize: '13px',
                        marginBottom: '8px',
                      }}
                    />
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <button
                        type="button"
                        onClick={() => handleRejectSubmit(user.id, user.name)}
                        disabled={actionLoading}
                        style={{
                          padding: '6px 14px',
                          background: '#dc2626',
                          color: '#ffffff',
                          border: 'none',
                          borderRadius: '6px',
                          fontSize: '12px',
                          fontWeight: 600,
                          cursor: 'pointer',
                        }}
                      >
                        Confirm Rejection
                      </button>
                      <button
                        type="button"
                        onClick={() => {
                          setRejectingId(null)
                          setRejectReason('')
                        }}
                        style={{
                          padding: '6px 12px',
                          background: '#ffffff',
                          color: '#4b5563',
                          border: '1px solid #d1d5db',
                          borderRadius: '6px',
                          fontSize: '12px',
                          cursor: 'pointer',
                        }}
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default UserManagement
