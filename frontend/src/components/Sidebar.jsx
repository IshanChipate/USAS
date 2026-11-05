function Sidebar({ currentPage, onNavigate, currentUser, onLogout }) {
  const menuItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
    },
    {
      id: 'assessment',
      label: 'City Assessment',
    },
    {
      id: 'indicators',
      label: 'Indicators',
    },
    {
      id: 'problems',
      label: 'Problem Areas',
    },
    {
      id: 'recommendations',
      label: 'Recommendations',
    },
    {
      id: 'impact',
      label: 'Impact Analysis',
    },
    {
      id: 'reports',
      label: 'Reports',
    },
  ]

  // Add User Verification for Administrators
  if (currentUser?.role === 'Administrator') {
    menuItems.push({
      id: 'user-management',
      label: 'User Verification',
    })
  }

  const initials = currentUser?.name
    ? currentUser.name
        .split(' ')
        .filter(Boolean)
        .slice(0, 2)
        .map((n) => n[0])
        .join('')
        .toUpperCase()
    : 'MH'

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-box">USAS</div>
        <div>
          <h2>USAS</h2>
          <span>Sustainability System</span>
        </div>
      </div>

      <nav className="sidebar-navigation">
        {menuItems.map((item) => (
          <button
            key={item.id}
            type="button"
            className={
              currentPage === item.id
                ? 'sidebar-item active'
                : 'sidebar-item'
            }
            onClick={() => onNavigate(item.id)}
          >
            {item.label}
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        {currentUser && (
          <div className="sidebar-user-card">
            <div className="sidebar-user-row">
              <div className="sidebar-user-avatar">{initials}</div>
              <div className="sidebar-user-details">
                <span className="sidebar-user-name" title={currentUser.name}>
                  {currentUser.name}
                </span>
                <span className="sidebar-user-role">{currentUser.role}</span>
                <span className="sidebar-user-dept" title={currentUser.department}>
                  {currentUser.department}
                </span>
              </div>
            </div>
            <button
              type="button"
              className="sidebar-logout-btn"
              onClick={onLogout}
              title="Sign Out of Session"
            >
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                <polyline points="16 17 21 12 16 7" />
                <line x1="21" y1="12" x2="9" y2="12" />
              </svg>
              Sign Out
            </button>
          </div>
        )}

        <div className="sidebar-brand-meta">
          <p>Government of Maharashtra</p>
          <span>Urban Analytics & Decision Support</span>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
