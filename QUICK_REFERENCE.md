# PrivyLoans - Quick Reference Card

## 🚀 Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt
npm install

# Initialize database
python -c "from api import app, db; app.app_context().push(); db.create_all()"

# Start backend (Terminal 1)
python api.py

# Start frontend (Terminal 2)
npm run dev
```

## 🌐 URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Admin Login**: http://localhost:3000/admin/login

## 👤 Default Credentials

### Admin
- Username: `admin`
- Password: `admin123`
- Setup: `python setup_admin.py`

### User
- Create at: http://localhost:3000/register

## 📁 Project Structure

```
privyloans/
├── src/                 # React frontend
│   ├── components/      # Reusable components
│   ├── pages/           # Page components
│   ├── context/         # State management
│   └── App.jsx          # Main app
├── api.py               # Flask REST API
├── app.py               # Original Flask app (legacy)
├── database.py          # Database models
├── crypto_utils.py      # Cryptography
├── package.json         # Node dependencies
└── requirements.txt     # Python dependencies
```

## 🔌 API Endpoints

### Auth
- `POST /api/auth/register` - Register
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Current user

### Applications
- `GET /api/applications` - List applications
- `POST /api/applications/apply` - Submit application
- `GET /api/applications/:id` - Get details
- `POST /api/applications/:id/withdraw` - Withdraw

### Admin
- `POST /api/auth/admin/login` - Admin login
- `GET /api/admin/applications` - All applications

### MFA
- `GET /api/mfa/setup` - Get QR code
- `POST /api/mfa/setup` - Enable MFA
- `POST /api/mfa/verify` - Verify code

## 🎨 Component Files

### Pages
- `Home.jsx` - Landing page
- `Login.jsx` - User login
- `Register.jsx` - User registration
- `Dashboard.jsx` - User dashboard
- `Apply.jsx` - Loan application form
- `Status.jsx` - Public status check
- `ApplicationDetails.jsx` - Application details
- `Certificate.jsx` - Approval certificate
- `AdminLogin.jsx` - Admin login
- `AdminDashboard.jsx` - Admin dashboard
- `SetupMFA.jsx` - MFA setup
- `VerifyMFA.jsx` - MFA verification
- `Success.jsx` - Success page

### Components
- `Navbar.jsx` - Navigation bar
- `Alert.jsx` - Alert messages

### Context
- `AuthContext.jsx` - Authentication state

## 🛠️ Common Commands

### Development
```bash
# Start backend
python api.py

# Start frontend
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Database
```bash
# Create database
python -c "from api import app, db; app.app_context().push(); db.create_all()"

# Reset database
del instance\privyloans.db
python -c "from api import app, db; app.app_context().push(); db.create_all()"

# Create admin
python setup_admin.py
```

### Dependencies
```bash
# Install Python packages
pip install -r requirements.txt

# Install Node packages
npm install

# Update packages
pip install --upgrade -r requirements.txt
npm update
```

## 🐛 Troubleshooting

### Port in use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Module not found
```bash
pip install flask-cors
npm install
```

### Database locked
```bash
# Stop servers, delete DB, recreate
del instance\privyloans.db
python -c "from api import app, db; app.app_context().push(); db.create_all()"
```

### CORS errors
```bash
# Ensure flask-cors is installed
pip install flask-cors

# Restart backend
python api.py
```

### npm errors
```bash
npm cache clean --force
rmdir /s /q node_modules
npm install
```

## 📊 Tech Stack

### Frontend
- React 18.2.0
- React Router 6.20.0
- Axios 1.6.2
- Vite 5.0.8

### Backend
- Flask
- Flask-CORS
- Flask-Login
- SQLAlchemy
- Bcrypt

## 🔐 Security Features

- Digital Signatures
- Zero-Knowledge Proofs
- Blind Signatures
- End-to-end Encryption
- MFA Authentication
- Password Hashing

## 📝 File Locations

### Configuration
- `vite.config.js` - Vite config
- `package.json` - Node config
- `.env` - Environment variables
- `requirements.txt` - Python packages

### Database
- `instance/privyloans.db` - SQLite database
- `database.py` - Database models

### Crypto
- `crypto_utils.py` - Digital signatures
- `zkp_utils.py` - Zero-knowledge proofs
- `blind_signature_utils.py` - Blind signatures
- `encryption_utils.py` - Encryption

### ML
- `train_model.py` - Model training
- `loan_model.joblib` - Trained model
- `scaler.joblib` - Feature scaler

## 🎯 User Flow

1. Register → Setup MFA → Login
2. Apply for loan → View dashboard
3. Check status → View certificate (if approved)

## 👨‍💼 Admin Flow

1. Login → View applications
2. ML auto-processes pending applications
3. View approval/rejection reasons

## 📱 Responsive Breakpoints

- Mobile: < 768px
- Tablet: 768px - 900px
- Desktop: > 900px

## 🎨 CSS Variables

```css
--background-dark: #000000
--background-light: #161b22
--accent-green: #2ea043
--accent-blue: #58a6ff
--accent-red: #f85149
--accent-yellow: #e3b341
```

## 📚 Documentation

- `README_REACT.md` - Full documentation
- `SETUP_GUIDE.md` - Setup instructions
- `MIGRATION_SUMMARY.md` - Migration details
- `QUICK_REFERENCE.md` - This file

## 🆘 Support

For issues:
1. Check error messages
2. Review browser console (F12)
3. Check terminal output
4. Refer to SETUP_GUIDE.md
5. Check MIGRATION_SUMMARY.md

## ✅ Verification Checklist

- [ ] Backend running on :5000
- [ ] Frontend running on :3000
- [ ] Can register user
- [ ] Can setup MFA
- [ ] Can login
- [ ] Can submit application
- [ ] Can view dashboard
- [ ] Admin can login
- [ ] Admin sees applications

---

**Quick tip**: Keep this file open while developing!
