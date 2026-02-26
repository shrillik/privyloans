import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import Alert from '../components/Alert'
import './Auth.css'

const SetupMFA = () => {
  const [qrCode, setQrCode] = useState('')
  const [code, setCode] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    fetchQRCode()
  }, [])

  const fetchQRCode = async () => {
    try {
      const response = await axios.get('/api/mfa/setup')
      setQrCode(response.data.qr_code)
    } catch (err) {
      setError('Failed to generate QR code')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await axios.post('/api/mfa/setup', { code })
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.message || 'Invalid code')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-container">
        <h2>Setup MFA</h2>
        <p className="auth-subtitle">Scan QR code with your authenticator app</p>

        {error && <Alert type="danger" message={error} onClose={() => setError('')} />}

        {qrCode && (
          <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
            <img src={`data:image/png;base64,${qrCode}`} alt="QR Code" style={{ maxWidth: '250px', borderRadius: '10px' }} />
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="code">Enter 6-digit code</label>
            <input
              type="text"
              id="code"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="000000"
              maxLength="6"
              required
            />
          </div>

          <button type="submit" className="btn-submit" disabled={loading}>
            {loading ? 'Verifying...' : 'Enable MFA'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default SetupMFA
