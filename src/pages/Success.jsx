import React from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import Navbar from '../components/Navbar'
import './Success.css'

const Success = () => {
  const [searchParams] = useSearchParams()
  const appId = searchParams.get('app_id')

  return (
    <div>
      <Navbar />
      
      <div className="success-container">
        <div className="success-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
        </div>
        <h1>Application Submitted Successfully!</h1>
        <p>Your loan application has been securely submitted with cryptographic protection.</p>
        
        {appId && (
          <div className="app-id-box">
            <label>Application ID:</label>
            <code>{appId}</code>
          </div>
        )}

        <div className="success-actions">
          <Link to="/dashboard" className="btn btn-primary">View Dashboard</Link>
          <Link to="/" className="btn btn-secondary">Go Home</Link>
        </div>
      </div>
    </div>
  )
}

export default Success
