# PrivyLoans - Privacy-Preserving Loan Application System

<div align="center">

![PrivyLoans](https://img.shields.io/badge/PrivyLoans-React%20%2B%20Flask-success)
![React](https://img.shields.io/badge/React-18.2.0-blue)
![Flask](https://img.shields.io/badge/Flask-Latest-green)
![License](https://img.shields.io/badge/License-Educational-orange)

**A modern, secure loan application system with cryptographic privacy protection**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Tech Stack](#-tech-stack)

</div>

---

## 🎯 Overview

PrivyLoans is a privacy-preserving loan application system that uses advanced cryptography to protect user identity while maintaining security and transparency. Built with React frontend and Flask REST API backend.

### Key Highlights

- 🔒 **Privacy-First**: Digital signatures, zero-knowledge proofs, blind signatures
- ⚡ **Modern Stack**: React 18 + Flask REST API
- 🎨 **Beautiful UI**: Modern dark theme with smooth animations
- 📱 **Responsive**: Works on all devices
- 🚀 **Fast**: Single Page Application with no page reloads
- 🔐 **Secure**: MFA, encryption, rate limiting

## ✨ Features

### For Users
- ✅ Secure registration and login
- ✅ Two-factor authentication (MFA)
- ✅ Loan application with cryptographic protection
- ✅ Real-time application tracking
- ✅ Cryptographic approval certificates
- ✅ Application management

### For Admins
- ✅ Admin dashboard
- ✅ ML-based loan approval/rejection
- ✅ Transparent rejection explanations
- ✅ Cryptographic verification

### Security Features
- 🔒 Digital Signatures
- 🔒 Zero-Knowledge Proofs
- 🔒 Blind Signatures
- 🔒 End-to-end Encryption
- 🔒 MFA Authentication

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm

### Installation

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Node dependencies
npm install

# 3. Initialize database
python -c "from api import app, db; app.app_context().push(); db.create_all()"

# 4. Start backend (Terminal 1)
python api.py

# 5. Start frontend (Terminal 2)
npm run dev
```

### Access

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Admin Login**: http://localhost:3000/admin/login

### Default Admin Credentials

```
Username: admin
Password: admin123
```

Create admin: `python setup_admin.py`

## 📚 Documentation

### 📖 Essential Guides

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** | Navigation guide | Start here |
| **[SETUP_GUIDE.md](SETUP_GUIDE.md)** | Setup instructions | Setting up |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | Quick commands | Daily use |
| **[README_REACT.md](README_REACT.md)** | Full documentation | Reference |

### 🔍 Deep Dive

| Document | Purpose |
|----------|---------|
| **[PROJECT_COMPLETE.md](PROJECT_COMPLETE.md)** | Project summary |
| **[MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)** | Technical details |
| **[BEFORE_AFTER.md](BEFORE_AFTER.md)** | Comparisons |
| **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** | Deployment guide |

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           React Frontend                │
│  (SPA with React Router & Context)      │
└──────────────┬──────────────────────────┘
               │ HTTP/JSON
               ▼
┌─────────────────────────────────────────┐
│         Flask REST API                  │
│  (Authentication, Business Logic)       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      SQLite Database                    │
│  (User Data, Applications)              │
└─────────────────────────────────────────┘
```

## 📁 Project Structure

```
privyloans/
├── src/                      # React frontend
│   ├── components/           # Reusable components
│   ├── pages/                # Page components
│   ├── context/              # State management
│   └── App.jsx               # Main app
├── api.py                    # Flask REST API
├── database.py               # Database models
├── crypto_utils.py           # Cryptography
├── package.json              # Node dependencies
├── vite.config.js            # Vite config
└── requirements.txt          # Python dependencies
```

## 🛠️ Tech Stack

### Frontend
- **React** 18.2.0 - UI framework
- **React Router** 6.20.0 - Routing
- **Axios** 1.6.2 - HTTP client
- **Vite** 5.0.8 - Build tool
- **CSS3** - Styling

### Backend
- **Flask** - Web framework
- **Flask-CORS** - CORS support
- **Flask-Login** - Authentication
- **SQLAlchemy** - ORM
- **Bcrypt** - Password hashing
- **PyOTP** - MFA
- **Scikit-learn** - ML model

### Security
- **ECDSA** - Digital signatures
- **Cryptography** - Encryption
- **Zero-Knowledge Proofs** - Privacy
- **Blind Signatures** - Anonymity

## 🎨 Screenshots

### Home Page
Modern landing page with hero section and feature highlights.

### Dashboard
User dashboard showing all loan applications with status tracking.

### Application Form
Comprehensive loan application form with cryptographic protection.

### Admin Panel
Admin dashboard with ML-based approval system.

## 🔧 Development

### Commands

```bash
# Start development servers
python api.py          # Backend
npm run dev            # Frontend

# Build for production
npm run build

# Run tests
npm test               # Frontend tests
pytest                 # Backend tests
```

### Environment Variables

Create `.env` file:

```env
SECRET_KEY=your-secret-key
SQLALCHEMY_DATABASE_URI=sqlite:///privyloans.db
```

## 🚀 Deployment

### Quick Deploy

```bash
# Build frontend
npm run build

# Deploy with Gunicorn
gunicorn -w 4 api:app
```

See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for detailed instructions.

## 🧪 Testing

### User Flow
1. Register → Setup MFA → Login
2. Apply for loan → View dashboard
3. Check status → View certificate

### Admin Flow
1. Login → View applications
2. ML processes pending applications
3. View approval/rejection reasons

## 📊 Features Comparison

| Feature | Before (HTML) | After (React) |
|---------|---------------|---------------|
| Page Loads | Full reload | No reload |
| Navigation | Slow | Instant |
| User Experience | Basic | Modern |
| Code Organization | Monolithic | Modular |
| Maintainability | Difficult | Easy |
| Scalability | Limited | High |

## 🤝 Contributing

This is an educational project. Feel free to:
- Fork the repository
- Create feature branches
- Submit pull requests
- Report issues

## 📝 License

Educational use only.

## 🆘 Support

### Getting Help

1. Check [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
2. Review [SETUP_GUIDE.md](SETUP_GUIDE.md)
3. See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
4. Read [README_REACT.md](README_REACT.md)

### Common Issues

**Port in use:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Module not found:**
```bash
pip install flask-cors
npm install
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for more solutions.

## 🎓 Learning Resources

- [React Documentation](https://react.dev/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Vite Documentation](https://vitejs.dev/)
- [React Router](https://reactrouter.com/)

## ✅ Status

- ✅ Frontend: Complete
- ✅ Backend: Complete
- ✅ Documentation: Complete
- ✅ Testing: Ready
- ✅ Deployment: Ready

## 🎉 Acknowledgments

Built with:
- React team for amazing framework
- Flask team for robust backend
- Vite team for fast build tool
- Open source community

## 📞 Contact

For questions or issues, please refer to the documentation files.

---

<div align="center">

**Built with ❤️ using React and Flask**

[Documentation](DOCUMENTATION_INDEX.md) • [Setup Guide](SETUP_GUIDE.md) • [Quick Reference](QUICK_REFERENCE.md)

</div>
