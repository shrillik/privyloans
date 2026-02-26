import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import ThemeToggle from './ThemeToggle'
import './Navbar.css'

const Navbar = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/')
  }

  return (
    <div className="navbar-wrapper">
      <nav className="navbar">
        <Link to="/" className="logo">
          <span className="logo-text">PrivyLoans</span>
        </Link>

        <div className="nav-actions">
          <ThemeToggle />
          
          <div className="nav-buttons">
            {user ? (
              <>
                {user.type === 'admin' ? (
                  <Link to="/admin" className="nav-btn nav-btn-secondary">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                      <circle cx="12" cy="7" r="4" />
                    </svg>
                    Admin Dashboard
                  </Link>
                ) : (
                  <>
                    <Link to="/dashboard" className="nav-btn nav-btn-secondary">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <rect x="3" y="3" width="7" height="7" />
                        <rect x="14" y="3" width="7" height="7" />
                        <rect x="14" y="14" width="7" height="7" />
                        <rect x="3" y="14" width="7" height="7" />
                      </svg>
                      Dashboard
                    </Link>
                    <Link to="/apply" className="nav-btn nav-btn-secondary">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <line x1="12" y1="5" x2="12" y2="19" />
                        <line x1="5" y1="12" x2="19" y2="12" />
                      </svg>
                      Apply
                    </Link>
                  </>
                )}
                <button onClick={handleLogout} className="nav-btn nav-btn-primary">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                    <polyline points="16 17 21 12 16 7" />
                    <line x1="21" y1="12" x2="9" y2="12" />
                  </svg>
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="nav-btn nav-btn-ghost">User Login</Link>
                <Link to="/admin/login" className="nav-btn nav-btn-primary">Admin Login</Link>
              </>
            )}
          </div>
        </div>
      </nav>
    </div>
  )
}

export default Navbar
