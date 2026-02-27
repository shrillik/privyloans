# PrivyLoans - Render Deployment Guide

This guide will help you deploy the PrivyLoans application on Render.

## Prerequisites

1. A GitHub account
2. A Render account (sign up at https://render.com)
3. Your code pushed to a GitHub repository

## Step 1: Prepare Your Repository

Make sure all files are committed and pushed to GitHub:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

## Step 2: Create a New Web Service on Render

1. Go to https://dashboard.render.com
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Select the PrivyLoans repository

## Step 3: Configure the Web Service

Fill in the following settings:

### Basic Settings
- **Name**: `privyloans` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave empty
- **Runtime**: `Python 3`

### Build Settings
- **Build Command**:
  ```bash
  pip install -r requirements.txt && npm install && npm run build
  ```

- **Start Command**:
  ```bash
  gunicorn api:app
  ```

### Advanced Settings

#### Environment Variables
Add these environment variables:

1. **SECRET_KEY**
   - Click "Generate" to create a secure random key
   - Or set your own: any long random string

2. **FLASK_ENV**
   - Value: `production`

3. **PYTHON_VERSION** (optional)
   - Value: `3.11.0`

#### Instance Type
- Select **Free** tier for testing
- Upgrade to **Starter** or higher for production use

## Step 4: Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Install Python dependencies
   - Install Node dependencies
   - Build the React frontend
   - Start the Flask backend with Gunicorn
3. Wait for the deployment to complete (5-10 minutes)

## Step 5: Initialize Database

After first deployment, you need to initialize the database:

1. Go to your service dashboard on Render
2. Click on "Shell" tab
3. Run these commands:

```bash
python -c "from api import app, db; app.app_context().push(); db.create_all()"
python setup_admin.py
```

This will create the database tables and set up the admin user.

## Step 6: Access Your Application

Your app will be available at:
```
https://privyloans.onrender.com
```
(Replace `privyloans` with your actual service name)

## Default Credentials

### Admin Login
- Username: `admin`
- Password: `admin123`
- URL: `https://your-app.onrender.com/admin/login`

**Important**: Change the admin password after first login!

## Troubleshooting

### Build Fails
- Check the build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt` and `package.json`
- Verify Python version compatibility

### App Crashes on Start
- Check the logs in Render dashboard
- Ensure `gunicorn` is in `requirements.txt`
- Verify environment variables are set correctly

### Database Issues
- Run the database initialization commands in the Shell
- Check if `instance/` directory has write permissions

### Static Files Not Loading
- Ensure `npm run build` completed successfully
- Check that `dist/` folder was created during build
- Verify Flask is configured to serve from `dist/` folder

### CORS Errors
- The app is configured with CORS support
- If issues persist, check browser console for specific errors

## Updating Your Deployment

Render automatically deploys when you push to your connected branch:

```bash
git add .
git commit -m "Update application"
git push origin main
```

Render will detect the push and redeploy automatically.

## Manual Redeploy

To manually trigger a redeploy:
1. Go to your service dashboard
2. Click "Manual Deploy"
3. Select "Clear build cache & deploy" if needed

## Database Persistence

**Important**: The free tier uses ephemeral storage. Your SQLite database will be reset on:
- Service restarts
- Redeployments
- Inactivity (after 15 minutes)

For production, consider:
1. Upgrading to a paid plan with persistent disk
2. Using Render's PostgreSQL database
3. Using an external database service

## Adding PostgreSQL (Recommended for Production)

1. Create a PostgreSQL database on Render
2. Copy the Internal Database URL
3. Add to environment variables:
   - Key: `DATABASE_URL`
   - Value: Your PostgreSQL connection string
4. Install psycopg2: Add `psycopg2-binary` to `requirements.txt`
5. Redeploy

## Performance Optimization

For better performance:
1. Upgrade from Free to Starter tier (no cold starts)
2. Enable "Auto-Deploy" for automatic updates
3. Set up health checks in Render dashboard
4. Monitor logs and metrics regularly

## Security Checklist

- [ ] Change default admin password
- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS (automatic on Render)
- [ ] Review CORS settings
- [ ] Set up proper environment variables
- [ ] Don't commit `.env` file to Git
- [ ] Use PostgreSQL for production
- [ ] Enable rate limiting (already configured)
- [ ] Regular security updates

## Support

If you encounter issues:
1. Check Render documentation: https://render.com/docs
2. Review application logs in Render dashboard
3. Check GitHub repository issues
4. Contact Render support

## Cost Estimate

- **Free Tier**: $0/month (with limitations)
- **Starter**: $7/month (recommended for production)
- **PostgreSQL**: $7/month (for persistent database)

Total recommended: ~$14/month for production deployment

---

**Deployment Status**: Ready for deployment
**Last Updated**: February 2026
