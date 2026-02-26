import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Navbar from '../components/Navbar'
import Alert from '../components/Alert'
import './AdminDashboard.css'

const AdminDashboard = () => {
  const [applications, setApplications] = useState([])
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState({ type: '', text: '' })

  useEffect(() => {
    fetchApplications()
  }, [])

  const fetchApplications = async () => {
    try {
      const response = await axios.get('/api/admin/applications')
      setApplications(response.data.applications)
      
      const hasProcessed = response.data.applications.some(app => 
        app.status === 'APPROVED' || app.status === 'REJECTED'
      )
      
      if (hasProcessed) {
        setMessage({ type: 'success', text: 'Processing Complete: Applications reviewed.' })
      }
    } catch (error) {
      setMessage({ type: 'danger', text: 'Failed to load applications' })
    } finally {
      setLoading(false)
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

      <div className="admin-container">
        <h2>Admin Dashboard</h2>

        {message.text && <Alert type={message.type} message={message.text} onClose={() => setMessage({ type: '', text: '' })} />}

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Application ID</th>
                <th>Name</th>
                <th>Amount</th>
                <th>Valid</th>
                <th>Status</th>
                <th>Prediction</th>
              </tr>
            </thead>
            <tbody>
              {applications.length === 0 ? (
                <tr>
                  <td colSpan="6" style={{ textAlign: 'center', padding: '2rem' }}>
                    No applications found
                  </td>
                </tr>
              ) : (
                applications.map((app) => (
                  <tr key={app.id}>
                    <td><small>{app.id}</small></td>
                    <td>{app.name}</td>
                    <td>₹{Number(app.amount).toLocaleString()}</td>
                    <td>{app.valid ? '✔' : '✘'}</td>
                    <td>
                      <span className={`status-badge ${app.status}`}>
                        {app.status}
                      </span>
                    </td>
                    <td>
                      <div>
                        <strong>{app.prediction}</strong>
                        {app.explanations && app.explanations.length > 0 && (
                          <ul className="explanation-list">
                            {app.explanations.map((exp, idx) => (
                              <li key={idx}>{exp}</li>
                            ))}
                          </ul>
                        )}
                      </div>
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

export default AdminDashboard
