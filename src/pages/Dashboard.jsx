import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import Navbar from '../components/Navbar'
import Alert from '../components/Alert'
import './Dashboard.css'

const Dashboard = () => {
  const [applications, setApplications] = useState([])
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState({ type: '', text: '' })

  useEffect(() => {
    fetchApplications()
  }, [])

  const fetchApplications = async () => {
    try {
      const response = await axios.get('/api/applications')
      setApplications(response.data.applications)
    } catch (error) {
      setMessage({ type: 'danger', text: 'Failed to load applications' })
    } finally {
      setLoading(false)
    }
  }

  const handleWithdraw = async (appId) => {
    if (!window.confirm('Are you sure you want to permanently withdraw and delete this application?')) {
      return
    }

    try {
      await axios.post(`/api/applications/${appId}/withdraw`)
      setMessage({ type: 'success', text: 'Application withdrawn successfully' })
      fetchApplications()
    } catch (error) {
      setMessage({ type: 'danger', text: error.response?.data?.message || 'Failed to withdraw application' })
    }
  }

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <div className="spinner"></div>
      </div>
    )
  }

  return (
    <div>
      <Navbar />
      
      <div className="dashboard-container">
        {message.text && <Alert type={message.type} message={message.text} onClose={() => setMessage({ type: '', text: '' })} />}

        <div className="dashboard-header">
          <h2>My Loan Applications</h2>
          <Link to="/" className="btn-home">Go Home</Link>
        </div>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Application ID</th>
                <th>Amount</th>
                <th>Purpose</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {applications.length === 0 ? (
                <tr>
                  <td colSpan="5" style={{ textAlign: 'center', padding: '2rem' }}>
                    No applications found. <Link to="/apply">Apply now</Link>
                  </td>
                </tr>
              ) : (
                applications.map((app) => (
                  <tr key={app.id}>
                    <td><small>{app.id}</small></td>
                    <td>₹{Number(app.amount).toLocaleString()}</td>
                    <td>{app.purpose}</td>
                    <td>
                      <span className={`status-badge ${app.status}`}>
                        {app.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="action-cell">
                      <Link to={`/application/${app.id}`} className="action-link">
                        Details
                      </Link>
                      {app.status === 'PENDING' && (
                        <button
                          onClick={() => handleWithdraw(app.id)}
                          className="btn-withdraw"
                        >
                          Withdraw
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
