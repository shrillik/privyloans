import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import axios from 'axios'
import Navbar from '../components/Navbar'
import './Certificate.css'

const Certificate = () => {
  const { appId } = useParams()
  const [certificate, setCertificate] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCertificate()
  }, [appId])

  const fetchCertificate = async () => {
    try {
      const response = await axios.get(`/api/applications/${appId}/certificate`)
      setCertificate(response.data)
    } catch (error) {
      console.error('Failed to load certificate')
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

  if (!certificate) {
    return (
      <div>
        <Navbar />
        <div className="certificate-container">
          <p>Certificate not available</p>
          <Link to="/dashboard">← Back to Dashboard</Link>
        </div>
      </div>
    )
  }

  return (
    <div>
      <Navbar />

      <div className="certificate-container">
        <div className="certificate-card">
          <div className="cert-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              <path d="M9 12l2 2 4-4"/>
            </svg>
          </div>
          <h1>Cryptographic Approval Certificate</h1>
          <p className="subtitle">Privacy-Preserving Loan Approval</p>

          <div className="qr-section">
            <img src={`data:image/png;base64,${certificate.qr_code}`} alt="Certificate QR Code" />
          </div>

          <div className="cert-details">
            <div className="cert-row">
              <span className="cert-label">Application ID:</span>
              <code>{certificate.app_id}</code>
            </div>

            <div className="cert-row">
              <span className="cert-label">Commitment:</span>
              <code className="truncate">{certificate.commitment}</code>
            </div>

            <div className="cert-row">
              <span className="cert-label">Token:</span>
              <code className="truncate">{certificate.token}</code>
            </div>

            <div className="cert-row">
              <span className="cert-label">Issued At:</span>
              <span>{certificate.issued_at}</span>
            </div>
          </div>

          <div className="cert-footer">
            <p>This certificate proves loan approval without revealing personal information.</p>
            <Link to="/dashboard" className="btn btn-primary">Back to Dashboard</Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Certificate
