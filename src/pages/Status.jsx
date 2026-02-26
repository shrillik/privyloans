import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import Navbar from '../components/Navbar'
import Alert from '../components/Alert'
import './Status.css'

const Status = () => {
  const [appId, setAppId] = useState('')
  const [application, setApplication] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await axios.post('/api/status/check', { app_id: appId })
      setApplication(response.data.application)
    } catch (err) {
      setError(err.response?.data?.message || 'Application not found')
      setApplication(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Navbar />
      <div className="status-page">
        <div className="status-container">
          <h2>Check Application Status</h2>

          {error && <Alert type="danger" message={error} onClose={() => setError('')} />}

          <form onSubmit={handleSubmit} className="status-form">
            <label>Application ID:</label>
            <input
              type="text"
              value={appId}
              onChange={(e) => setAppId(e.target.value)}
              placeholder="Enter your application ID"
              required
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Checking...' : 'Check Status'}
            </button>
          </form>

          {application && (
            <div className="status-card">
              <div className="status-row">
                <span className="label">Name:</span>
                <span>{application.name}</span>
              </div>
              <div className="status-row">
                <span className="label">Status:</span>
                <span className={`status-value ${application.status}`}>
                  {application.status}
                </span>
              </div>
              <div className="status-row">
                <span className="label">ZKP Check:</span>
                <span>{application.valid ? '✔ Valid' : '✘ Invalid'}</span>
              </div>
            </div>
          )}

          <div className="footer-link">
            <Link to="/">← Back to Home</Link>
          </div>
        </div>
      </div>
    </>
  )
}

export default Status
