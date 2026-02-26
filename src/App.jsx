import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'

// Pages
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Apply from './pages/Apply'
import Status from './pages/Status'
import ApplicationDetails from './pages/ApplicationDetails'
import Certificate from './pages/Certificate'
import AdminLogin from './pages/AdminLogin'
import AdminDashboard from './pages/AdminDashboard'
import SetupMFA from './pages/SetupMFA'
import VerifyMFA from './pages/VerifyMFA'
import Success from './pages/Success'

// Protected Route Component
const ProtectedRoute = ({ children, adminOnly = false }) => {
  const { user, loading } = useAuth()
  
  if (loading) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <div className="spinner"></div>
    </div>
  }
  
  if (!user) {
    return <Navigate to="/login" replace />
  }
  
  if (adminOnly && user.type !== 'admin') {
    return <Navigate to="/dashboard" replace />
  }
  
  if (!adminOnly && user.type === 'admin') {
    return <Navigate to="/admin" replace />
  }
  
  return children
}

function App() {
  return (
    <ThemeProvider>
      <Router>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/admin/login" element={<AdminLogin />} />
            <Route path="/status" element={<Status />} />
            
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } />
            
            <Route path="/apply" element={
              <ProtectedRoute>
                <Apply />
              </ProtectedRoute>
            } />
            
            <Route path="/setup-mfa" element={<SetupMFA />} />
            <Route path="/verify-mfa" element={<VerifyMFA />} />
            
            <Route path="/success" element={
              <ProtectedRoute>
                <Success />
              </ProtectedRoute>
            } />
            
            <Route path="/application/:appId" element={
              <ProtectedRoute>
                <ApplicationDetails />
              </ProtectedRoute>
            } />
            
            <Route path="/application/:appId/certificate" element={
              <ProtectedRoute>
                <Certificate />
              </ProtectedRoute>
            } />
            
            <Route path="/admin" element={
              <ProtectedRoute adminOnly>
                <AdminDashboard />
              </ProtectedRoute>
            } />
          </Routes>
        </AuthProvider>
      </Router>
    </ThemeProvider>
  )
}

export default App
