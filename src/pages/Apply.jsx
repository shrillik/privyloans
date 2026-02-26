import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import Navbar from '../components/Navbar'
import Alert from '../components/Alert'
import './Apply.css'

const Apply = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: 'MFA Verified',
    pan: '',
    age: '',
    purpose: '',
    term: '',
    income: '',
    amount: ''
  })

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setShowModal(true)

    // Simulate crypto animation
    await new Promise(resolve => setTimeout(resolve, 4000))

    try {
      const response = await axios.post('/api/applications/apply', formData)
      navigate(`/success?app_id=${response.data.app_id}`)
    } catch (err) {
      setError(err.response?.data?.message || 'Application submission failed')
      setShowModal(false)
    }
  }

  return (
    <div>
      <Navbar />

      <main className="form-wrapper">
        <div className="form-container">
          <h2>Loan Application Form</h2>
          <p>Your application will be protected with cryptography.</p>

          {error && <Alert type="danger" message={error} onClose={() => setError('')} />}

          <form onSubmit={handleSubmit} className="loan-form">
            <div className="form-group full-width">
              <label htmlFor="name">Full Name</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Jane Doe"
                required
              />
            </div>

            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="jane@example.com"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="phone">Verified Phone</label>
                <input
                  type="text"
                  id="phone"
                  name="phone"
                  value={formData.phone}
                  readOnly
                />
              </div>

              <div className="form-group">
                <label htmlFor="pan">PAN Number</label>
                <input
                  type="text"
                  id="pan"
                  name="pan"
                  value={formData.pan}
                  onChange={handleChange}
                  placeholder="ABCDE1234F"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="age">Age</label>
                <input
                  type="number"
                  id="age"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                  placeholder="25"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="purpose">Purpose of Loan</label>
                <input
                  type="text"
                  id="purpose"
                  name="purpose"
                  value={formData.purpose}
                  onChange={handleChange}
                  placeholder="e.g., Education, Home"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="term">Term (in months)</label>
                <input
                  type="number"
                  id="term"
                  name="term"
                  value={formData.term}
                  onChange={handleChange}
                  placeholder="12"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="income">Annual Income (₹)</label>
                <input
                  type="number"
                  id="income"
                  name="income"
                  value={formData.income}
                  onChange={handleChange}
                  placeholder="500000"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="amount">Loan Amount (₹)</label>
                <input
                  type="number"
                  id="amount"
                  name="amount"
                  value={formData.amount}
                  onChange={handleChange}
                  placeholder="100000"
                  required
                />
              </div>
            </div>

            <button type="submit" className="btn-submit" disabled={loading}>
              Submit Application
            </button>
          </form>
        </div>
      </main>

      {showModal && (
        <div className="animation-modal">
          <div className="animation-container">
            <h3>Securing Application</h3>
            <div className="loading-spinner"></div>
            <p style={{ marginTop: '1rem', color: 'var(--text-secondary)' }}>
              Applying cryptographic protections...
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

export default Apply
