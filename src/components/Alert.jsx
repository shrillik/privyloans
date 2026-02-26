import React from 'react'
import './Alert.css'

const Alert = ({ type = 'info', message, onClose }) => {
  if (!message) return null

  return (
    <div className={`alert alert-${type}`}>
      {message}
      {onClose && (
        <button className="alert-close" onClick={onClose}>×</button>
      )}
    </div>
  )
}

export default Alert
