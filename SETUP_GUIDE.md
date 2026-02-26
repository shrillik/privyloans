# PrivyLoans Setup Guide

Complete step-by-step guide to set up and run the React + Flask application.

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] Node.js 16 or higher installed
- [ ] npm (comes with Node.js)
- [ ] Git (optional, for cloning)
- [ ] A code editor (VS Code recommended)

### Check Your Versions

```bash
python --version
node --version
npm --version
```

## 🚀 Quick Start (Windows)

### Option 1: Automated Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Node dependencies:**
   ```bash
   npm install
   ```

3. **Initialize database:**
   ```bash
   python -c "from api import app, db; app.app_context().push(); db.create_all()"
   ```

4. **Run the application:**
   ```bash
   start.bat
   ```

This will open two command windows:
- Backend API on http://localhost:5000
- Frontend React app on http://localhost:3000

### Option 2: Manual Setup

Follow the detailed steps below for more control.

## 📦 Detailed Setup Steps

### Step 1: Backend Setup

1. **Navigate to project directory:**
   ```bash
   cd path/to/privyloans
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize the database:**
   ```bash
   python -c "from api import app, db; app.app_context().push(); db.create_all()"
   ```

6. **Create admin user (optional):**
   ```bash
   python setup_admin.py
   ```
   Default admin credentials:
   - Username: `admin`
   - Password: `admin123`

7. **Start Flask API:**
   ```bash
   python api.py
   ```
   
   You should see:
   ```
   * Running on http://127.0.0.1:5000
   ```

### Step 2: Frontend Setup

Open a **new terminal window** (keep the backend running):

1. **Install Node dependencies:**
   ```bash
   npm install
   ```

2. **Start React development server:**
   ```bash
   npm run dev
   ```
   
   You should see:
   ```
   VITE v5.x.x  ready in xxx ms
   
   ➜  Local:   http://localhost:3000/
   ```

3. **Open browser:**
   Navigate to http://localhost:3000

## 🎯 First Time Usage

### Register a User Account

1. Go to http://localhost:3000
2. Click "User" button in navigation
3. Click "Register here" link
4. Enter username and password
5. Click "Register"

### Setup MFA

1. After registration, you'll see a QR code
2. Install an authenticator app on your phone:
   - Google Authenticator
   - Microsoft Authenticator
   - Authy
3. Scan the QR code with your app
4. Enter the 6-digit code from your app
5. Click "Enable MFA"

### Apply for a Loan

1. You'll be redirected to the application form
2. Fill in all required fields:
   - Full Name
   - Email
   - PAN Number
   - Age (21-60)
   - Purpose
   - Term (months)
   - Annual Income (minimum ₹250,000)
   - Loan Amount
3. Click "Submit Application"
4. Wait for the cryptographic animation
5. You'll see a success page with your Application ID

### View Dashboard

1. Click "My Dashboard" in navigation
2. See all your applications
3. Click "Details" to view application details
4. If approved, click "View Certificate"

### Admin Access

1. Go to http://localhost:3000/admin/login
2. Enter admin credentials
3. View all applications
4. ML model automatically processes pending applications

## 🔧 Configuration

### Change Ports

**Backend (api.py):**
```python
if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Change 5000 to your port
```

**Frontend (vite.config.js):**
```javascript
export default defineConfig({
  server: {
    port: 3000,  // Change 3000 to your port
    proxy: {
      '/api': {
        target: 'http://localhost:5000',  // Update if backend port changed
        changeOrigin: true,
      }
    }
  }
})
```

### Environment Variables

Create `.env` file in root directory:

```env
SECRET_KEY=your-secret-key-here
SQLALCHEMY_DATABASE_URI=sqlite:///privyloans.db
FLASK_ENV=development
```

## 🐛 Common Issues & Solutions

### Issue 1: Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Windows - Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change the port in api.py
```

### Issue 2: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'flask_cors'`

**Solution:**
```bash
pip install flask-cors
```

### Issue 3: Database Locked

**Error:** `database is locked`

**Solution:**
```bash
# Stop all servers
# Delete database
del instance\privyloans.db

# Recreate database
python -c "from api import app, db; app.app_context().push(); db.create_all()"
```

### Issue 4: CORS Errors

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
- Ensure `flask-cors` is installed
- Check `api.py` has `CORS(app, supports_credentials=True)`
- Restart backend server

### Issue 5: npm Install Fails

**Error:** Various npm errors

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules
rmdir /s /q node_modules

# Reinstall
npm install
```

## 📱 Testing the Application

### Test User Flow

1. ✅ Register new account
2. ✅ Setup MFA
3. ✅ Login with MFA
4. ✅ Submit loan application
5. ✅ View dashboard
6. ✅ Check application details
7. ✅ Withdraw pending application

### Test Admin Flow

1. ✅ Login as admin
2. ✅ View all applications
3. ✅ Verify ML processing
4. ✅ Check approval/rejection

### Test Public Features

1. ✅ Check application status (without login)
2. ✅ View home page

## 🏗️ Building for Production

### Build React App

```bash
npm run build
```

This creates optimized files in `dist/` directory.

### Serve with Flask

Update `api.py` to serve React build:

```python
import os
from flask import send_from_directory

# Add this route
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists('dist/' + path):
        return send_from_directory('dist', path)
    return send_from_directory('dist', 'index.html')
```

### Run Production Server

```bash
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

## 📊 Project Structure Overview

```
privyloans/
├── src/                    # React source code
│   ├── components/         # Reusable UI components
│   ├── pages/              # Page components
│   ├── context/            # React Context (Auth)
│   └── App.jsx             # Main app
├── api.py                  # Flask REST API
├── database.py             # Database models
├── crypto_utils.py         # Cryptography
├── package.json            # Node dependencies
├── vite.config.js          # Vite config
└── requirements.txt        # Python dependencies
```

## 🎓 Learning Resources

### React
- [React Documentation](https://react.dev/)
- [React Router](https://reactrouter.com/)

### Flask
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-CORS](https://flask-cors.readthedocs.io/)

### Vite
- [Vite Documentation](https://vitejs.dev/)

## 💡 Tips

1. **Keep both terminals open** - Backend and frontend run separately
2. **Check browser console** - For frontend errors
3. **Check terminal output** - For backend errors
4. **Use incognito mode** - To test without cached data
5. **Clear browser cache** - If seeing old UI

## 🆘 Getting Help

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review error messages carefully
3. Check browser console (F12)
4. Check terminal output
5. Verify all dependencies are installed
6. Try restarting both servers

## ✅ Verification Checklist

After setup, verify:

- [ ] Backend running on http://localhost:5000
- [ ] Frontend running on http://localhost:3000
- [ ] Can access home page
- [ ] Can register new user
- [ ] Can setup MFA
- [ ] Can login
- [ ] Can submit application
- [ ] Can view dashboard
- [ ] Admin can login
- [ ] Admin can see applications

## 🎉 Success!

If all checks pass, your PrivyLoans application is ready to use!

---

**Need more help?** Check README_REACT.md for detailed documentation.
