import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Navbar from '../components/Navbar'
import './Home.css'

const Home = () => {
  const { user } = useAuth()

  return (
    <div className="home-page">
      <Navbar />
      
      <section className="hero">
        <div className="hero-content">
            <span className="hero-badge">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
              {user?.type === 'admin' ? 'Admin Portal' : 'Secure Banking Solutions'}
            </span>

            <h1>
              {user?.type === 'admin' ? (
                <>
                  Manage loan applications <br />
                  with <span className="gradient-text">full control</span>
                </>
              ) : (
                <>
                  Privacy-first loan applications <br />
                  with <span className="gradient-text">advanced security</span>
                </>
              )}
            </h1>

            <p>
              {user?.type === 'admin' ? (
                'Access the admin dashboard to review, approve, or reject loan applications. Monitor all user activities and manage the system with complete administrative control.'
              ) : (
                'Experience next-generation financial services with military-grade encryption, digital signatures, and zero-knowledge proof technology that protects your identity throughout the entire application process.'
              )}
            </p>

            <div className="hero-buttons">
              {user?.type === 'admin' ? (
                <Link to="/admin" className="btn btn-primary">
                  Go to Admin Dashboard
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                  </svg>
                </Link>
              ) : (
                <>
                  <Link to="/apply" className="btn btn-primary">
                    Apply for Loan
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M5 12h14M12 5l7 7-7 7"/>
                    </svg>
                  </Link>
                  <Link to="/status" className="btn btn-secondary">
                    Check Application Status
                  </Link>
                </>
              )}
            </div>

            {user?.type !== 'admin' && (
              <>
                <div className="hero-features">
                  <span>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <polyline points="20 6 9 17 4 12"/>
                    </svg>
                    Instant Approval
                  </span>
                  <span>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    </svg>
                    Bank-Grade Security
                  </span>
                  <span>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </svg>
                    Complete Privacy
                  </span>
                </div>

                <div className="trust-indicators">
                  <div className="trust-item">
                    <div className="trust-number">256-bit</div>
                    <div className="trust-label">Encryption</div>
                  </div>
                  <div className="trust-item">
                    <div className="trust-number">24/7</div>
                    <div className="trust-label">Support</div>
                  </div>
                  <div className="trust-item">
                    <div className="trust-number">100%</div>
                    <div className="trust-label">Secure</div>
                  </div>
                  <div className="trust-item">
                    <div className="trust-number">FDIC</div>
                    <div className="trust-label">Insured</div>
                  </div>
                </div>
              </>
            )}
          </div>

          {user?.type !== 'admin' && (
            <div className="hero-visual">
              <div className="floating-cards">
                {/* Main Application Card */}
                <div className="card card-application">
                  <div className="card-header">
                    <div className="card-icon">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <polyline points="14 2 14 8 20 8"/>
                        <line x1="16" y1="13" x2="8" y2="13"/>
                        <line x1="16" y1="17" x2="8" y2="17"/>
                        <polyline points="10 9 9 9 8 9"/>
                      </svg>
                    </div>
                    <div className="card-title">
                      <h3>Loan Application</h3>
                      <p>Quick & Secure Process</p>
                    </div>
                  </div>
                  
                  <div className="card-body">
                    <div className="form-field">
                      <label>Loan Amount</label>
                      <div className="input-display">$50,000</div>
                    </div>
                    
                    <div className="form-field">
                      <label>Purpose</label>
                      <div className="input-display">Business Expansion</div>
                    </div>
                    
                    <div className="form-field">
                      <label>Term Length</label>
                      <div className="input-display">36 months</div>
                    </div>
                    
                    <button className="card-button">
                      Submit Application
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <polyline points="20 6 9 17 4 12"/>
                      </svg>
                    </button>
                  </div>
                </div>

                {/* Stats Card */}
                <div className="card card-stats">
                  <div className="stats-header">
                    <h4>Application Status</h4>
                    <span className="status-badge-mini approved">Active</span>
                  </div>
                  
                  <div className="stats-chart">
                    <div className="chart-line">
                      <svg viewBox="0 0 200 80" preserveAspectRatio="none">
                        <path 
                          d="M 0 60 L 40 55 L 80 45 L 120 35 L 160 30 L 200 20" 
                          fill="none" 
                          stroke="currentColor" 
                          strokeWidth="2"
                          className="chart-path"
                        />
                        <path 
                          d="M 0 60 L 40 55 L 80 45 L 120 35 L 160 30 L 200 20 L 200 80 L 0 80 Z" 
                          fill="url(#chartGradient)" 
                          opacity="0.2"
                        />
                        <defs>
                          <linearGradient id="chartGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stopColor="currentColor" stopOpacity="0.3"/>
                            <stop offset="100%" stopColor="currentColor" stopOpacity="0"/>
                          </linearGradient>
                        </defs>
                      </svg>
                    </div>
                    
                    <div className="stats-metrics">
                      <div className="metric">
                        <span className="metric-value">98.5%</span>
                        <span className="metric-label">Approval Rate</span>
                      </div>
                      <div className="metric">
                        <span className="metric-value">2.4hrs</span>
                        <span className="metric-label">Avg. Processing</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Security Badge Card */}
                <div className="card card-security">
                  <div className="security-icon">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                      <path d="M9 12l2 2 4-4"/>
                    </svg>
                  </div>
                  <div className="security-text">
                    <h4>256-bit Encrypted</h4>
                    <p>Bank-level security</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {user?.type === 'admin' && (
            <div className="hero-visual">
              <div className="floating-cards">
                {/* Admin Dashboard Card */}
                <div className="card card-application">
                  <div className="card-header">
                    <div className="card-icon">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                        <path d="M2 17l10 5 10-5"/>
                        <path d="M2 12l10 5 10-5"/>
                      </svg>
                    </div>
                    <div className="card-title">
                      <h3>Admin Control</h3>
                      <p>Manage Applications</p>
                    </div>
                  </div>
                  
                  <div className="card-body">
                    <div className="form-field">
                      <label>Total Applications</label>
                      <div className="input-display">0</div>
                    </div>
                    
                    <div className="form-field">
                      <label>Pending Review</label>
                      <div className="input-display">0</div>
                    </div>
                    
                    <div className="form-field">
                      <label>Approved Today</label>
                      <div className="input-display">0</div>
                    </div>
                    
                    <Link to="/admin" className="card-button">
                      View Dashboard
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M5 12h14M12 5l7 7-7 7"/>
                      </svg>
                    </Link>
                  </div>
                </div>

                {/* Admin Stats Card */}
                <div className="card card-stats">
                  <div className="stats-header">
                    <h4>System Status</h4>
                    <span className="status-badge-mini approved">Online</span>
                  </div>
                  
                  <div className="stats-chart">
                    <div className="chart-line">
                      <svg viewBox="0 0 200 80" preserveAspectRatio="none">
                        <path 
                          d="M 0 50 L 40 45 L 80 40 L 120 35 L 160 30 L 200 25" 
                          fill="none" 
                          stroke="currentColor" 
                          strokeWidth="2"
                          className="chart-path"
                        />
                        <path 
                          d="M 0 50 L 40 45 L 80 40 L 120 35 L 160 30 L 200 25 L 200 80 L 0 80 Z" 
                          fill="url(#chartGradient)" 
                          opacity="0.2"
                        />
                        <defs>
                          <linearGradient id="chartGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stopColor="currentColor" stopOpacity="0.3"/>
                            <stop offset="100%" stopColor="currentColor" stopOpacity="0"/>
                          </linearGradient>
                        </defs>
                      </svg>
                    </div>
                    
                    <div className="stats-metrics">
                      <div className="metric">
                        <span className="metric-value">100%</span>
                        <span className="metric-label">System Uptime</span>
                      </div>
                      <div className="metric">
                        <span className="metric-value">0</span>
                        <span className="metric-label">Active Users</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Admin Security Badge Card */}
                <div className="card card-security">
                  <div className="security-icon">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                    </svg>
                  </div>
                  <div className="security-text">
                    <h4>Admin Access</h4>
                    <p>Full system control</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </section>
    </div>
  )
}

export default Home
