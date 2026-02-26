# PrivyLoans - React + Flask Application

A modern, privacy-preserving loan application system built with React frontend and Flask API backend.

## 🏗️ Architecture

- **Frontend**: React 18 with Vite, React Router, Axios
- **Backend**: Flask REST API with SQLAlchemy
- **Styling**: Modern CSS with CSS Variables
- **Authentication**: Flask-Login with MFA support
- **Cryptography**: Digital Signatures, Zero-Knowledge Proofs, Blind Signatures

## 📁 Project Structure

```
privyloans/
├── src/                      # React frontend source
│   ├── components/           # Reusable components
│   │   ├── Navbar.jsx
│   │   ├── Alert.jsx
│   │   └── *.css
│   ├── pages/                # Page components
│   │   ├── Home.jsx
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Apply.jsx
│   │   ├── Status.jsx
│   │   ├── ApplicationDetails.jsx
│   │   ├── Certificate.jsx
│   │   ├── AdminLogin.jsx
│   │   ├── AdminDashboard.jsx
│   │   ├── SetupMFA.jsx
│   │   ├── VerifyMFA.jsx
│   │   ├── Success.jsx
│   │   └── *.css
│   ├── context/              # React Context
│   │   └── AuthContext.jsx
│   ├── App.jsx               # Main app component
│   ├── main.jsx              # Entry point
│   └── index.css             # Global styles
├── api.py                    # Flask REST API backend
├── app.py                    # Original Flask app (legacy)
├── database.py               # Database models
├── crypto_utils.py           # Cryptographic utilities
├── zkp_utils.py              # Zero-knowledge proof utilities
├── encryption_utils.py       # Encryption utilities
├── blind_signature_utils.py  # Blind signature utilities
├── package.json              # Node dependencies
├── vite.config.js            # Vite configuration
├── index.html                # HTML entry point
└── requirements.txt          # Python dependencies

```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install flask-cors
   ```

2. **Initialize the database:**
   ```bash
   python -c "from api import app, db; app.app_context().push(); db.create_all()"
   ```

3. **Create admin user (optional):**
   ```bash
   python setup_admin.py
   ```

4. **Start the Flask API server:**
   ```bash
   python api.py
   ```
   The API will run on `http://localhost:5000`

### Frontend Setup

1. **Install Node dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```
   The React app will run on `http://localhost:3000`

3. **Build for production:**
   ```bash
   npm run build
   ```
   Production files will be in the `dist/` directory

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
SQLALCHEMY_DATABASE_URI=sqlite:///privyloans.db
```

### API Endpoints

The Flask backend exposes the following REST API endpoints:

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/admin/login` - Admin login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

#### MFA
- `GET /api/mfa/setup` - Get MFA QR code
- `POST /api/mfa/setup` - Verify and enable MFA
- `POST /api/mfa/verify` - Verify MFA code

#### Applications
- `GET /api/applications` - Get user's applications
- `POST /api/applications/apply` - Submit new application
- `GET /api/applications/:id` - Get application details
- `POST /api/applications/:id/withdraw` - Withdraw application
- `GET /api/applications/:id/certificate` - Get approval certificate

#### Admin
- `GET /api/admin/applications` - Get all applications (admin only)

#### Public
- `POST /api/status/check` - Check application status (public)

## 🎨 Features

### User Features
- ✅ Secure registration and login
- ✅ Two-factor authentication (MFA)
- ✅ Loan application with cryptographic protection
- ✅ Application dashboard
- ✅ Real-time status tracking
- ✅ Cryptographic approval certificates
- ✅ Application withdrawal

### Admin Features
- ✅ Admin dashboard
- ✅ ML-based loan approval/rejection
- ✅ Transparent rejection explanations
- ✅ Cryptographic verification

### Security Features
- 🔒 Digital signatures
- 🔒 Zero-knowledge proofs
- 🔒 Blind signatures
- 🔒 End-to-end encryption
- 🔒 MFA authentication

## 🎯 Usage

### For Users

1. **Register**: Create an account at `/register`
2. **Setup MFA**: Scan QR code with authenticator app
3. **Login**: Login with credentials and MFA code
4. **Apply**: Fill out loan application form
5. **Track**: View application status in dashboard
6. **Certificate**: Download approval certificate if approved

### For Admins

1. **Login**: Use admin credentials at `/admin/login`
2. **Review**: View all applications in admin dashboard
3. **Auto-Process**: ML model automatically processes pending applications

## 🔄 Migration from HTML Templates

The original Flask app used server-side rendering with Jinja2 templates. This React version:

- ✅ Separates frontend and backend concerns
- ✅ Provides better user experience with SPA
- ✅ Enables easier scaling and deployment
- ✅ Maintains all original functionality
- ✅ Improves code maintainability

### Key Changes

1. **Templates → React Components**: All HTML templates converted to React components
2. **Flask Routes → REST API**: Server routes now return JSON instead of HTML
3. **Session Management**: Client-side auth state with React Context
4. **Form Handling**: Client-side validation and submission
5. **Styling**: Modular CSS with component-level styles

## 📦 Deployment

### Production Build

1. **Build React app:**
   ```bash
   npm run build
   ```

2. **Serve with Flask:**
   Update `api.py` to serve the React build:
   ```python
   from flask import send_from_directory
   
   @app.route('/', defaults={'path': ''})
   @app.route('/<path:path>')
   def serve(path):
       if path and os.path.exists(app.static_folder + '/' + path):
           return send_from_directory(app.static_folder, path)
       return send_from_directory(app.static_folder, 'index.html')
   ```

3. **Deploy to production server** (Heroku, AWS, DigitalOcean, etc.)

## 🐛 Troubleshooting

### CORS Issues
If you encounter CORS errors, ensure `flask-cors` is installed and configured in `api.py`

### Port Conflicts
- Backend default: `5000`
- Frontend default: `3000`
Change ports in `api.py` and `vite.config.js` if needed

### Database Issues
Delete `privyloans.db` and reinitialize:
```bash
rm instance/privyloans.db
python -c "from api import app, db; app.app_context().push(); db.create_all()"
```

## 📝 License

This project is for educational purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ using React and Flask**
