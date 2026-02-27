# Quick Deployment Checklist for Render

## Before You Deploy

- [ ] All code committed to Git
- [ ] Repository pushed to GitHub
- [ ] `.env` file NOT committed (check .gitignore)
- [ ] All dependencies listed in requirements.txt
- [ ] React app builds successfully locally (`npm run build`)

## Render Setup (Choose One Method)

### Method 1: Blueprint (Easiest)
1. [ ] Push `render.yaml` to your repository
2. [ ] Go to https://dashboard.render.com
3. [ ] Click "New +" → "Blueprint"
4. [ ] Connect your GitHub repository
5. [ ] Click "Apply" - Render will auto-configure everything!

### Method 2: Manual Setup
1. [ ] Go to https://dashboard.render.com
2. [ ] Click "New +" → "Web Service"
3. [ ] Connect your GitHub repository
4. [ ] Configure settings:
   - **Build Command**: `pip install -r requirements.txt && npm install && npm run build`
   - **Start Command**: `gunicorn api:app`
   - **Environment Variables**:
     - `SECRET_KEY`: Generate random value
     - `FLASK_ENV`: `production`

## After Deployment

1. [ ] Wait for build to complete (5-10 minutes)
2. [ ] Open Shell in Render dashboard
3. [ ] Initialize database:
   ```bash
   python -c "from api import app, db; app.app_context().push(); db.create_all()"
   python setup_admin.py
   ```
4. [ ] Visit your app URL
5. [ ] Test login with admin credentials (admin/admin123)
6. [ ] Change admin password immediately!

## Your App URLs

- **Main App**: `https://privyloans.onrender.com`
- **Admin Login**: `https://privyloans.onrender.com/admin/login`
- **User Login**: `https://privyloans.onrender.com/login`

## Common Issues

**Build fails?**
- Check logs in Render dashboard
- Ensure Node.js and Python are both available

**App won't start?**
- Verify `gunicorn` is in requirements.txt
- Check environment variables are set

**Database empty?**
- Run initialization commands in Shell
- Check if commands completed successfully

**Static files 404?**
- Ensure `npm run build` succeeded
- Check `dist/` folder was created

## Free Tier Limitations

⚠️ **Important**: Free tier has limitations:
- App sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- Database resets on restart (ephemeral storage)

**For Production**: Upgrade to Starter ($7/month) for:
- No cold starts
- Persistent disk storage
- Better performance

## Need Help?

See full guide: `RENDER_DEPLOYMENT.md`

---

**Ready to deploy!** 🚀
