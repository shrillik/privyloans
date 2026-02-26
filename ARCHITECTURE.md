# PrivyLoans Architecture

Complete architectural overview of the PrivyLoans React + Flask application.

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Browser                              │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              React Application (SPA)                  │ │
│  │                                                       │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │ │
│  │  │  Pages   │  │Components│  │  Context (Auth)  │  │ │
│  │  └──────────┘  └──────────┘  └──────────────────┘  │ │
│  │                                                       │ │
│  │  ┌──────────────────────────────────────────────┐   │ │
│  │  │         React Router (Client-side)           │   │ │
│  │  └──────────────────────────────────────────────┘   │ │
│  └───────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTP/JSON (Axios)
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Flask REST API                            │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Auth Routes  │  │  App Routes  │  │  Admin Routes   │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Business Logic Layer                    │  │
│  │  • Authentication  • Validation  • ML Processing     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            Cryptography Layer                        │  │
│  │  • Signatures  • ZKP  • Encryption  • Blind Sigs    │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ SQLAlchemy ORM
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   SQLite Database                           │
│                                                             │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │  Users   │  │ Applications │  │      Admins          │ │
│  └──────────┘  └──────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Component Architecture

### Frontend Components

```
src/
├── App.jsx                          # Main application
│   ├── Router                       # React Router setup
│   └── AuthProvider                 # Authentication context
│
├── pages/                           # Page-level components
│   ├── Home.jsx                     # Landing page
│   ├── Login.jsx                    # User login
│   ├── Register.jsx                 # User registration
│   ├── Dashboard.jsx                # User dashboard
│   ├── Apply.jsx                    # Loan application
│   ├── Status.jsx                   # Status checker
│   ├── ApplicationDetails.jsx       # Application details
│   ├── Certificate.jsx              # Approval certificate
│   ├── AdminLogin.jsx               # Admin login
│   ├── AdminDashboard.jsx           # Admin panel
│   ├── SetupMFA.jsx                 # MFA setup
│   ├── VerifyMFA.jsx                # MFA verification
│   └── Success.jsx                  # Success page
│
├── components/                      # Reusable components
│   ├── Navbar.jsx                   # Navigation bar
│   └── Alert.jsx                    # Alert messages
│
└── context/                         # State management
    └── AuthContext.jsx              # Authentication state
```

### Backend Structure

```
Backend/
├── api.py                           # Main API file
│   ├── Auth Routes                  # /api/auth/*
│   ├── MFA Routes                   # /api/mfa/*
│   ├── Application Routes           # /api/applications/*
│   ├── Admin Routes                 # /api/admin/*
│   └── Public Routes                # /api/status/*
│
├── database.py                      # Database models
│   ├── User                         # User model
│   ├── Admin                        # Admin model
│   └── Application                  # Application model
│
├── crypto_utils.py                  # Cryptography
│   ├── generate_keys()              # Key generation
│   ├── sign_data()                  # Digital signatures
│   └── verify_signature()           # Signature verification
│
├── zkp_utils.py                     # Zero-knowledge proofs
│   ├── pedersen_commit()            # Commitment
│   ├── prove_pedersen_opening()     # Proof generation
│   └── verify_pedersen_opening()    # Proof verification
│
├── encryption_utils.py              # Encryption
│   ├── encrypt_data()               # Data encryption
│   └── decrypt_data()               # Data decryption
│
└── blind_signature_utils.py         # Blind signatures
    ├── generate_blind_keys()        # Key generation
    ├── blind_message()              # Message blinding
    ├── sign_blinded_message()       # Signing
    └── unblind_signature()          # Unblinding
```

## 🔄 Data Flow

### User Registration Flow

```
1. User fills registration form
   ↓
2. React validates input
   ↓
3. POST /api/auth/register
   ↓
4. Flask validates data
   ↓
5. Hash password (Bcrypt)
   ↓
6. Create user in database
   ↓
7. Return user data (JSON)
   ↓
8. React updates auth state
   ↓
9. Redirect to MFA setup
```

### Loan Application Flow

```
1. User fills application form
   ↓
2. React validates input
   ↓
3. Show crypto animation
   ↓
4. POST /api/applications/apply
   ↓
5. Flask validates eligibility
   ↓
6. Generate cryptographic proofs:
   • Pedersen commitment
   • Zero-knowledge proof
   • Digital signature
   • Blind signature
   ↓
7. Encrypt sensitive data
   ↓
8. Store in database
   ↓
9. Return application ID
   ↓
10. React shows success page
```

### Admin Approval Flow

```
1. Admin logs in
   ↓
2. GET /api/admin/applications
   ↓
3. Flask fetches all applications
   ↓
4. For each PENDING application:
   • Verify cryptographic proofs
   • Decrypt data
   • Run ML model
   • Update status (APPROVED/REJECTED)
   • Generate blind signature (if approved)
   ↓
5. Return applications with status
   ↓
6. React displays in admin dashboard
```

## 🔐 Security Architecture

### Authentication Flow

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ 1. Login credentials
       ▼
┌─────────────┐
│    React    │
└──────┬──────┘
       │ 2. POST /api/auth/login
       ▼
┌─────────────┐
│    Flask    │
│             │
│ 3. Verify  │
│ password   │
│ (Bcrypt)   │
└──────┬──────┘
       │ 4. If MFA enabled
       ▼
┌─────────────┐
│   PyOTP     │
│             │
│ 5. Verify  │
│ TOTP code  │
└──────┬──────┘
       │ 6. Create session
       ▼
┌─────────────┐
│   Session   │
│   Cookie    │
└─────────────┘
```

### Cryptographic Protection

```
Application Data
       ↓
┌──────────────────┐
│  1. Encryption   │  ← AES encryption
└────────┬─────────┘
         ↓
┌──────────────────┐
│  2. Commitment   │  ← Pedersen commitment
└────────┬─────────┘
         ↓
┌──────────────────┐
│  3. ZK Proof     │  ← Zero-knowledge proof
└────────┬─────────┘
         ↓
┌──────────────────┐
│  4. Signature    │  ← Digital signature
└────────┬─────────┘
         ↓
┌──────────────────┐
│  5. Blind Sig    │  ← Blind signature
└────────┬─────────┘
         ↓
    Database
```

## 🗄️ Database Schema

```sql
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    mfa_secret VARCHAR(32),
    mfa_enabled BOOLEAN DEFAULT FALSE,
    blind_N TEXT,
    created_at TIMESTAMP
);

-- Admins Table
CREATE TABLE admins (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    mfa_secret VARCHAR(32),
    mfa_enabled BOOLEAN DEFAULT FALSE,
    blind_priv_N TEXT,
    blind_priv_d TEXT,
    created_at TIMESTAMP
);

-- Applications Table
CREATE TABLE applications (
    id VARCHAR(36) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    encrypted_email TEXT,
    encrypted_phone TEXT,
    encrypted_pan TEXT,
    encrypted_age TEXT,
    encrypted_purpose TEXT,
    encrypted_term TEXT,
    encrypted_income TEXT,
    signature TEXT,
    commitment TEXT,
    proof_t TEXT,
    proof_s1 TEXT,
    proof_s2 TEXT,
    status VARCHAR(20) DEFAULT 'PENDING',
    blind_signature TEXT,
    blinding_factor_r TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 🌐 API Architecture

### RESTful Endpoints

```
Authentication
├── POST   /api/auth/register        # Register user
├── POST   /api/auth/login           # User login
├── POST   /api/auth/admin/login     # Admin login
├── POST   /api/auth/logout          # Logout
└── GET    /api/auth/me              # Current user

MFA
├── GET    /api/mfa/setup            # Get QR code
├── POST   /api/mfa/setup            # Enable MFA
└── POST   /api/mfa/verify           # Verify code

Applications
├── GET    /api/applications         # List user apps
├── POST   /api/applications/apply   # Submit app
├── GET    /api/applications/:id     # Get details
├── POST   /api/applications/:id/withdraw  # Withdraw
└── GET    /api/applications/:id/certificate  # Certificate

Admin
└── GET    /api/admin/applications   # All apps (admin)

Public
└── POST   /api/status/check         # Check status
```

### Request/Response Format

```json
// Request
POST /api/auth/login
{
  "username": "john",
  "password": "secret123"
}

// Response (Success)
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "john",
    "type": "user",
    "mfa_enabled": true
  }
}

// Response (Error)
{
  "message": "Invalid credentials"
}
```

## 🎨 Frontend Architecture

### State Management

```
AuthContext
├── user (current user)
├── loading (loading state)
├── login() (login function)
├── register() (register function)
├── logout() (logout function)
└── checkAuth() (verify auth)
```

### Routing Structure

```
/                           → Home
/login                      → Login
/register                   → Register
/dashboard                  → Dashboard (protected)
/apply                      → Apply (protected)
/setup-mfa                  → Setup MFA (protected)
/verify-mfa                 → Verify MFA (protected)
/success                    → Success (protected)
/application/:id            → Details (protected)
/application/:id/certificate → Certificate (protected)
/admin/login                → Admin Login
/admin                      → Admin Dashboard (protected, admin only)
/status                     → Public Status
```

## 🔄 Build Process

### Development

```
Source Code (src/)
       ↓
   Vite Dev Server
       ↓
   Hot Module Replacement
       ↓
   Browser (localhost:3000)
```

### Production

```
Source Code (src/)
       ↓
   Vite Build
       ↓
   Optimization
   • Minification
   • Tree shaking
   • Code splitting
       ↓
   dist/ folder
       ↓
   Static Files
   • index.html
   • assets/*.js
   • assets/*.css
```

## 🚀 Deployment Architecture

### Single Server

```
┌─────────────────────────────────┐
│         Nginx (Port 80)         │
│                                 │
│  ┌──────────────────────────┐  │
│  │   Static Files (React)   │  │
│  │   /var/www/privyloans/   │  │
│  └──────────────────────────┘  │
│                                 │
│  ┌──────────────────────────┐  │
│  │   Proxy to Backend       │  │
│  │   /api → localhost:5000  │  │
│  └──────────────────────────┘  │
└─────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│    Gunicorn (Port 5000)         │
│    Flask API                    │
└─────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│    SQLite Database              │
└─────────────────────────────────┘
```

### Separate Deployment

```
┌─────────────────────────────────┐
│   Vercel/Netlify (Frontend)    │
│   React SPA                     │
└──────────────┬──────────────────┘
               │ HTTPS
               ▼
┌─────────────────────────────────┐
│   Heroku/AWS (Backend)          │
│   Flask REST API                │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   PostgreSQL/MySQL              │
│   Production Database           │
└─────────────────────────────────┘
```

## 📊 Performance Considerations

### Frontend Optimization
- Code splitting by route
- Lazy loading components
- Image optimization
- CSS minification
- Gzip compression

### Backend Optimization
- Database indexing
- Query optimization
- Caching (Redis)
- Connection pooling
- Rate limiting

### Network Optimization
- CDN for static assets
- HTTP/2
- Compression
- Caching headers
- Minification

## 🔒 Security Layers

```
Layer 1: Transport Security
├── HTTPS/TLS
└── Secure cookies

Layer 2: Authentication
├── Password hashing (Bcrypt)
├── MFA (TOTP)
└── Session management

Layer 3: Authorization
├── Role-based access
├── Route protection
└── API authentication

Layer 4: Data Protection
├── Encryption (AES)
├── Digital signatures
├── Zero-knowledge proofs
└── Blind signatures

Layer 5: Application Security
├── CSRF protection
├── XSS prevention
├── SQL injection prevention
├── Rate limiting
└── Input validation
```

## 📈 Scalability

### Horizontal Scaling

```
Load Balancer
       │
       ├─→ Flask Instance 1
       ├─→ Flask Instance 2
       └─→ Flask Instance 3
              │
              ▼
       Shared Database
```

### Vertical Scaling

```
Increase Resources
├── More CPU cores
├── More RAM
├── Faster storage
└── Better network
```

## 🎯 Future Architecture

### Microservices

```
API Gateway
    │
    ├─→ Auth Service
    ├─→ Application Service
    ├─→ Crypto Service
    ├─→ ML Service
    └─→ Notification Service
```

### Event-Driven

```
Application Submitted
       ↓
   Message Queue
       ↓
   ├─→ Crypto Processing
   ├─→ ML Processing
   └─→ Notification
```

---

**This architecture provides a solid foundation for a scalable, secure, and maintainable application.**
