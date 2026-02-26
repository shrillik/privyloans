import React, { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import axios from 'axios'
import Navbar from '../components/Navbar'
import Alert from '../components/Alert'
import './ApplicationDetails.css'

const ApplicationDetails = () => {
  const { appId } = useParams()
  const navigate = useNavigate()
  const [application, setApplication] = useState(null)
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState({ type: '', text: '' })

  useEffect(() => {
    fetchApplication()
  }, [appId])

  const fetchApplication = async () => {
    try {
      const response = await axios.get(`/api/applications/${appId}`)
      setApplication(response.data.application)
    } catch (error) {
      setMessage({ type: 'danger', text: 'Application not found' })
    } finally {
      setLoading(false)
    }
  }

  const handleWithdraw = async () => {
    if (!window.confirm('Are you sure you want to withdraw this application?')) {
      return
    }

    try {
      await axios.post(`/api/applications/${appId}/withdraw`)
      setMessage({ type: 'success', text: 'Application withdrawn' })
      setTimeout(() => navigate('/dashboard'), 2000)
    } catch (error) {
      setMessage({ type: 'danger', text: error.response?.data?.message || 'Failed to withdraw' })
    }
  }

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <div className="spinner"></div>
      </div>
    )
  }

  if (!application) {
    return (
      <div>
        <Navbar />
        <div className="details-container">
          <Alert type="danger" message="Application not found" />
          <Link to="/dashboard">← Back to Dashboard</Link>
        </div>
      </div>
    )
  }

  return (
    <div>
      <Navbar />

      <div className="details-container">
        <h2>Application Details</h2>

        {message.text && <Alert type={message.type} message={message.text} onClose={() => setMessage({ type: '', text: '' })} />}

        <div className="details-card">
          <div className="detail-row">
            <span className="label">Status:</span>
            <span className={`status-badge ${application.status}`}>
              {application.status}
            </span>
          </div>

          <div className="detail-row">
            <span className="label">ZKP Verification:</span>
            <span>{application.is_zkp_valid ? '✔ Valid' : '✘ Invalid'}</span>
          </div>

          <div className="detail-row">
            <span className="label">Name:</span>
            <span>{application.name}</span>
          </div>

          <div className="detail-row">
            <span className="label">Amount:</span>
            <span>₹{Number(application.amount).toLocaleString()}</span>
          </div>

          <div className="detail-row">
            <span className="label">Purpose:</span>
            <span>{application.purpose}</span>
          </div>

          <div className="detail-row">
            <span className="label">Email:</span>
            <span>{application.email}</span>
          </div>

          <div className="detail-row">
            <span className="label">Phone:</span>
            <span>{application.phone}</span>
          </div>
        </div>

        <div className="action-buttons">
          {application.status === 'APPROVED' && (
            <Link to={`/application/${appId}/certificate`} className="btn btn-blue">
              View Certificate
            </Link>
          )}

          {application.status === 'PENDING' && (
            <button onClick={handleWithdraw} className="btn btn-red">
              Withdraw Application
            </button>
          )}

          <Link to="/dashboard" className="btn btn-secondary">
            Back to Dashboard
          </Link>
        </div>
      </div>
    </div>
  )
}

export default ApplicationDetails
