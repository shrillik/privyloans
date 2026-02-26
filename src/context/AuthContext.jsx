import React, { createContext, useState, useContext, useEffect } from 'react'
import axios from 'axios'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    try {
      const response = await axios.get('/api/auth/me')
      setUser(response.data.user)
    } catch (error) {
      setUser(null)
    } finally {
      setLoading(false)
    }
  }

  const login = async (username, password, isAdmin = false) => {
    const endpoint = isAdmin ? '/api/auth/admin/login' : '/api/auth/login'
    const response = await axios.post(endpoint, { username, password })
    
    // Only set user if MFA is not required
    if (!response.data.mfa_required) {
      setUser(response.data.user)
    }
    
    return response.data
  }

  const register = async (username, password) => {
    const response = await axios.post('/api/auth/register', { username, password })
    setUser(response.data.user)
    return response.data
  }

  const logout = async () => {
    await axios.post('/api/auth/logout')
    setUser(null)
  }

  const value = {
    user,
    loading,
    login,
    register,
    logout,
    checkAuth
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
