# Phase 13: Cloud Deployment Guide

## Deployment Options

We'll deploy to **TWO** services:
1. **Backend API** → Render.com (Free tier)
2. **Frontend Dashboard** → Streamlit Cloud (Free tier)

---

## OPTION 1: Streamlit Cloud (Easiest - Recommended for Hackathon)

### What Gets Deployed
Your **complete app** (frontend + backend) in one click!

### Step-by-Step

#### 1. Push Code to GitHub

```powershell
# Initialize git (if not already done)
cd E:\disaster_management\disaster-warning-platform
git init

# Create .gitignore
echo "venv/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
echo "*.pkl" >> .gitignore
echo "outputs/" >> .gitignore

# Add all files
git add .

# Commit
git commit -m "Complete AI Flood Warning System - Ready for deployment"

# Create GitHub repo and push
# (Follow GitHub's instructions to create a new repo)
git remote add origin https://github.com/YOUR_USERNAME/flood-warning-system.git
git branch -M main
git push -u origin main
```

#### 2. Deploy to Streamlit Cloud

1. **Go to:** https://streamlit.io/cloud
2. **Click:** "Sign up" (use GitHub account)
3. **Click:** "New app"
4. **Configure:**
   - Repository: `YOUR_USERNAME/flood-warning-system`
   - Branch: `main`
   - Main file path: `src/frontend/user_flow_app.py`
5. **Click:** "Deploy!"

#### 3. Wait 2-3 Minutes

Your app will be live at:
```
https://YOUR_APP_NAME.streamlit.app
```

**That's it!** ✅

---

## OPTION 2: Render.com (API Backend)

### For API Backend Only

#### 1. Create Account
- Go to: https://render.com
- Sign up with GitHub

#### 2. Create New Web Service
- Click "New +" → "Web Service"
- Connect your GitHub repo
- Configure:
  - **Name:** `flood-warning-api`
  - **Environment:** Python 3
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT`
  - **Plan:** Free

#### 3. Add Environment Variables (Optional)
- `OPENWEATHER_API_KEY`: Your API key
- `TWILIO_ACCOUNT_SID`: For SMS alerts
- `TWILIO_AUTH_TOKEN`: For SMS alerts

#### 4. Deploy
- Click "Create Web Service"
- Wait 3-5 minutes

Your API will be live at:
```
https://flood-warning-api.onrender.com
```

---

## OPTION 3: Railway (Alternative)

### Quick Deploy

#### 1. Install Railway CLI
```powershell
npm install -g @railway/cli
# OR use web interface at railway.app
```

#### 2. Deploy
```powershell
# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

Your app will be live at a Railway URL!

---

## OPTION 4: Vercel (Frontend Only)

### For Streamlit Dashboard

1. Go to: https://vercel.com
2. Import your GitHub repo
3. Configure:
   - Framework: Other
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: Leave blank
   - Install Command: `streamlit run src/frontend/user_flow_app.py`

---

## Post-Deployment Checklist

After deploying:

- [ ] Visit your live URL
- [ ] Test city input
- [ ] Make a prediction
- [ ] Check alerts display
- [ ] Test on mobile device
- [ ] Share link with judges!

---

## Troubleshooting

### Issue: App won't start
**Solution:** Check build logs for errors
- Missing dependencies → Add to requirements.txt
- Port issues → Use `$PORT` environment variable

### Issue: Model not found
**Solution:** Upload model files
- Ensure `data/models/flood_model.pkl` is in repo
- Check file paths are relative, not absolute

### Issue: Slow loading
**Solution:** This is normal for free tiers
- First load: 30-60 seconds (cold start)
- Subsequent loads: Fast

---

## Custom Domain (Optional)

### Streamlit Cloud
1. Go to app settings
2. Add custom domain
3. Update DNS records

### Render
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS with provided CNAME

---

## Your Live URLs

After deployment, you'll have:

```
Frontend (Streamlit):
https://your-app.streamlit.app

Backend API (Render):
https://your-api.onrender.com

API Docs:
https://your-api.onrender.com/docs
```

**Share these links in your hackathon submission!** 🚀

---

## For Hackathon Judges

### Demo Links to Share

```
🌐 Live Demo: https://your-app.streamlit.app
📚 API Docs: https://your-api.onrender.com/docs
📂 GitHub: https://github.com/YOUR_USERNAME/flood-warning-system
📹 Video Demo: [Optional - record a quick walkthrough]
```

### What to Say

> "Our AI flood warning system is deployed and live at [URL]. 
> Anyone can access it right now and check flood risk for their city. 
> The backend API is hosted on Render, frontend on Streamlit Cloud, 
> and the entire codebase is on GitHub. It's production-ready and 
> scalable to handle thousands of users."

---

## Maintenance & Monitoring

### Free Tier Limits

**Streamlit Cloud (Free):**
- 1 app
- Unlimited visitors
- Sleep after 7 days inactive

**Render (Free):**
- 750 hours/month
- Sleeps after 15 min inactive
- 100GB bandwidth

**Solution for Sleep:** 
- Use UptimeRobot.com (free) to ping your app every 5 minutes
- Keeps it awake during hackathon judging!

---

## Quick Deploy Checklist

**Before deploying:**
- [ ] Code pushed to GitHub
- [ ] requirements.txt up to date
- [ ] Model files included
- [ ] No hardcoded paths
- [ ] Environment variables documented

**After deploying:**
- [ ] Test live URL
- [ ] Check all features work
- [ ] Test on mobile
- [ ] Share link with team
- [ ] Add to hackathon submission

---

**Ready to go live?** Choose your deployment option and let's deploy! 🚀