# 🚀 Deploy to Render in 5 Minutes

## Step 1: Push to GitHub
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

## Step 2: Deploy on Render

### Option A: Blueprint (Easiest) ⭐
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repo
4. Click **"Apply"**
5. Done! ✅

### Option B: Manual
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo
4. Set:
   - **Build**: `pip install -r requirements.txt && npm install && npm run build`
   - **Start**: `gunicorn api:app`
   - **Add env var**: `SECRET_KEY` (click Generate)
   - **Add env var**: `FLASK_ENV` = `production`
5. Click **"Create Web Service"**

## Step 3: Initialize Database
After deployment completes:
1. Click **"Shell"** tab in Render dashboard
2. Run:
```bash
python -c "from api import app, db; app.app_context().push(); db.create_all()"
python setup_admin.py
```

## Step 4: Access Your App
- **URL**: `https://your-app-name.onrender.com`
- **Admin**: `https://your-app-name.onrender.com/admin/login`
- **Login**: admin / admin123

## ⚠️ Important
- Change admin password after first login!
- Free tier: app sleeps after 15 min (cold start ~30s)
- For production: upgrade to Starter ($7/month)

## 📚 Need More Help?
- Full guide: `RENDER_DEPLOYMENT.md`
- Checklist: `DEPLOY_CHECKLIST.md`
- Summary: `DEPLOYMENT_SUMMARY.md`

---
**That's it!** Your app is live! 🎉
