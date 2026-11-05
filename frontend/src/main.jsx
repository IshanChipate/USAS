import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

import './styles/global.css'
import './styles/login.css'
import './styles/sidebar.css'
import './styles/dashboard.css'
import './styles/assessment.css'
import './styles/indicators.css'
import './styles/problems.css'
import './styles/recommendations.css'
import './styles/impact.css'
import './styles/reports.css'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)