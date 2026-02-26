# Deployment Checklist

Complete checklist for deploying PrivyLoans React + Flask application to production.

## 📋 Pre-Deployment Checklist

### Code Quality
- [ ] All features tested and working
- [ ] No console errors in browser
- [ ] No Python errors in terminal
- [ ] Code reviewed and cleaned
- [ ] Unused code removed
- [ ] Comments added where needed
- [ ] TODO items resolved

### Security
- [ ] Environment variables configured
- [ ] Secret keys generated (not default)
- [ ] Debug mode disabled
- [ ] CORS configured properly
- [ ] SQL injection prevention verified
- [ ] XSS protection enabled
- [ ] CSRF protection enabled
- [ ] Password hashing verified
- [ ] MFA working correctly
- [ ] API rate limiting configured

### Performance
- [ ] React app built for production
- [ ] Bundle size optimized
- [ ] Images optimized
- [ ] Lazy loading implemented
- [ ] Database queries optimized
- [ ] Caching configured
- [ ] Compression enabled

### Testing
- [ ] All user flows tested
- [ ] All admin flows tested
- [ ] MFA setup tested
- [ ] Application submission tested
- [ ] Certificate generation tested
- [ ] Error handling tested
- [ ] Mobile responsiveness tested
- [ ] Cross-browser testing done

## 🏗️ Build Process

### Frontend Build

1. **Update environment variables:**
   ```bash
   # Create .env.production
   VITE_API_URL=https://your-api-domain.com
   ```

2. **Build React app:**
   ```bash
   npm run build
   ```

3. **Test production build:**
   ```bash
   npm run preview
   ```

4. **Verify build output:**
   - [ ] `dist/` folder created
   - [ ] `dist/index.html` exists
   - [ ] `dist/assets/` contains JS/CSS
   - [ ] No build errors

### Backend Preparation

1. **Update configuration:**
   ```python
   # api.py
   app.config['DEBUG'] = False
   app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
   ```

2. **Create requirements.txt:**
   ```bash
   pip freeze > requirements.txt
   ```

3. **Test with production settings:**
   ```bash
   python api.py
   ```

## 🚀 Deployment Options

### Option 1: Single Server Deployment

Deploy both frontend and backend on same server.

#### Steps:

1. **Setup server:**
   - [ ] Ubuntu/Debian server
   - [ ] Python 3.8+ installed
   - [ ] Node.js 16+ installed
   - [ ] Nginx installed

2. **Upload files:**
   ```bash
   scp -r dist/ user@server:/var/www/privyloans/
   scp -r *.py user@server:/var/www/privyloans/
   scp requirements.txt user@server:/var/www/privyloans/
   ```

3. **Install dependencies:**
   ```bash
   ssh user@server
   cd /var/www/privyloans
   pip install -r requirements.txt
   ```

4. **Configure Nginx:**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       # Serve React app
       location / {
           root /var/www/privyloans/dist;
           try_files $uri $uri/ /index.html;
       }

       # Proxy API requests
       location /api {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **Start backend with Gunicorn:**
   ```bash
   gunicorn -w 4 -b 127.0.0.1:5000 api:app
   ```

6. **Setup systemd service:**
   ```ini
   [Unit]
   Description=PrivyLoans API
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/privyloans
   ExecStart=/usr/local/bin/gunicorn -w 4 -b 127.0.0.1:5000 api:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

### Option 2: Separate Deployment

Deploy frontend and backend separately.

#### Frontend (Vercel/Netlify)

1. **Connect repository:**
   - [ ] Push code to GitHub
   - [ ] Connect to Vercel/Netlify
   - [ ] Configure build settings

2. **Build settings:**
   ```
   Build Command: npm run build
   Output Directory: dist
   ```

3. **Environment variables:**
   ```
   VITE_API_URL=https://your-api-domain.com
   ```

4. **Deploy:**
   - [ ] Trigger deployment
   - [ ] Verify deployment
   - [ ] Test live site

#### Backend (Heroku/AWS/DigitalOcean)

1. **Create Procfile:**
   ```
   web: gunicorn api:app
   ```

2. **Configure environment:**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DATABASE_URL=your-database-url
   ```

3. **Deploy:**
   ```bash
   git push heroku main
   ```

4. **Initialize database:**
   ```bash
   heroku run python -c "from api import app, db; app.app_context().push(); db.create_all()"
   ```

### Option 3: Docker Deployment

Use Docker containers for deployment.

#### Create Dockerfile (Backend)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api:app"]
```

#### Create Dockerfile (Frontend)

```dockerfile
FROM node:16-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

#### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./instance:/app/instance

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

## 🔒 Security Checklist

### SSL/HTTPS
- [ ] SSL certificate installed
- [ ] HTTPS enabled
- [ ] HTTP redirects to HTTPS
- [ ] HSTS header configured

### Environment Variables
- [ ] All secrets in environment variables
- [ ] No hardcoded credentials
- [ ] .env files not committed
- [ ] Production secrets different from dev

### Database
- [ ] Database backups configured
- [ ] Database access restricted
- [ ] Connection pooling configured
- [ ] SQL injection prevention verified

### API Security
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Authentication required
- [ ] Input validation enabled
- [ ] Error messages sanitized

### Headers
- [ ] Security headers configured:
  ```python
  @app.after_request
  def set_security_headers(response):
      response.headers['X-Content-Type-Options'] = 'nosniff'
      response.headers['X-Frame-Options'] = 'DENY'
      response.headers['X-XSS-Protection'] = '1; mode=block'
      response.headers['Strict-Transport-Security'] = 'max-age=31536000'
      return response
  ```

## 📊 Monitoring Setup

### Application Monitoring
- [ ] Error tracking (Sentry)
- [ ] Performance monitoring
- [ ] Uptime monitoring
- [ ] Log aggregation

### Server Monitoring
- [ ] CPU usage monitoring
- [ ] Memory usage monitoring
- [ ] Disk space monitoring
- [ ] Network monitoring

### Alerts
- [ ] Error rate alerts
- [ ] Downtime alerts
- [ ] Performance alerts
- [ ] Security alerts

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Node
      uses: actions/setup-node@v2
      with:
        node-version: '16'
    
    - name: Build Frontend
      run: |
        npm install
        npm run build
    
    - name: Deploy to Server
      run: |
        # Your deployment script
```

## 📝 Post-Deployment Checklist

### Verification
- [ ] Site loads correctly
- [ ] All pages accessible
- [ ] Forms work correctly
- [ ] Authentication works
- [ ] MFA works
- [ ] Applications can be submitted
- [ ] Admin dashboard works
- [ ] Certificates generate correctly

### Performance
- [ ] Page load time < 3s
- [ ] API response time < 500ms
- [ ] No console errors
- [ ] No 404 errors
- [ ] Images load correctly

### SEO (if applicable)
- [ ] Meta tags configured
- [ ] Sitemap generated
- [ ] Robots.txt configured
- [ ] Analytics installed

### Documentation
- [ ] Deployment documented
- [ ] API documentation updated
- [ ] User guide updated
- [ ] Admin guide updated

## 🔧 Maintenance Plan

### Regular Tasks
- [ ] Weekly: Check logs for errors
- [ ] Weekly: Review performance metrics
- [ ] Monthly: Update dependencies
- [ ] Monthly: Database backup verification
- [ ] Quarterly: Security audit
- [ ] Quarterly: Performance optimization

### Backup Strategy
- [ ] Daily database backups
- [ ] Weekly full backups
- [ ] Backup retention policy
- [ ] Backup restoration tested

### Update Strategy
- [ ] Staging environment setup
- [ ] Test updates in staging
- [ ] Scheduled maintenance windows
- [ ] Rollback plan documented

## 📞 Support Plan

### Contact Information
- [ ] Support email configured
- [ ] Emergency contact list
- [ ] Escalation procedures

### Documentation
- [ ] User documentation
- [ ] Admin documentation
- [ ] API documentation
- [ ] Troubleshooting guide

## ✅ Final Verification

Before going live:

- [ ] All checklist items completed
- [ ] Stakeholders notified
- [ ] Backup plan ready
- [ ] Rollback plan ready
- [ ] Support team briefed
- [ ] Monitoring configured
- [ ] Documentation updated

## 🎉 Go Live!

1. **Final checks:**
   - [ ] All systems green
   - [ ] Team ready
   - [ ] Backups verified

2. **Deploy:**
   - [ ] Execute deployment
   - [ ] Monitor logs
   - [ ] Verify functionality

3. **Post-launch:**
   - [ ] Monitor for 24 hours
   - [ ] Address any issues
   - [ ] Collect feedback

---

**Congratulations on your deployment! 🚀**
