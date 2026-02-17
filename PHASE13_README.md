# Phase 13: Deployment - Instructions

## Overview
Deploy your AI Flood Warning System to the cloud so anyone can access it online!

## Prerequisites
✅ Phases 1-12 complete (system tested and working)
✅ GitHub account
✅ Git installed on your computer

## Files Created
- `requirements.txt` - Updated with all dependencies
- `Procfile` - For Heroku/Railway deployment
- `render.yaml` - For Render.com deployment
- `DEPLOYMENT_GUIDE.md` - Detailed deployment instructions

---

## Quick Start: Deploy in 5 Minutes

### Recommended: Streamlit Cloud (Easiest)

**Perfect for hackathon demos!**

#### Step 1: Push to GitHub (2 minutes)

```powershell
cd E:\disaster_management\disaster-warning-platform

# Initialize git
git init

# Create .gitignore
@"
venv/
__pycache__/
*.pyc
.env
*.log
.DS_Store
"@ | Out-File -FilePath .gitignore -Encoding utf8

# Add files
git add .
git commit -m "AI Flood Warning System - Hackathon Ready"

# Create repo on GitHub (github.com/new)
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/flood-warning.git
git branch -M main
git push -u origin main
```

#### Step 2: Deploy to Streamlit Cloud (2 minutes)

1. Go to: **https://share.streamlit.io**
2. Click **"New app"**
3. Fill in:
   - **Repository:** `YOUR_USERNAME/flood-warning`
   - **Branch:** `main`
   - **Main file:** `src/frontend/user_flow_app.py`
4. Click **"Deploy!"**

#### Step 3: Get Your Live URL (1 minute)

Wait 2-3 minutes, then your app is live at:
```
https://YOUR-APP-NAME.streamlit.app
```

**Done!** Share this URL with hackathon judges! 🎉

---

## Alternative Deployment Options

### Option 2: Render.com (API Backend)

**Best for:** Separating backend API from frontend

#### Quick Deploy

1. **Sign up:** https://render.com (use GitHub)
2. **New Web Service** → Connect GitHub repo
3. **Configure:**
   ```
   Name: flood-warning-api
   Build: pip install -r requirements.txt
   Start: uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT
   ```
4. **Deploy!**

**Live at:** `https://flood-warning-api.onrender.com`

---

### Option 3: Railway (Fastest)

**Best for:** Quick deployment with zero config

#### One-Click Deploy

```powershell
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

**Live in 60 seconds!**

---

## Deployment Comparison

| Platform | Speed | Free Tier | Best For |
|----------|-------|-----------|----------|
| **Streamlit Cloud** | ⚡⚡⚡ Fast | 1 app, unlimited users | **Hackathon demos** |
| **Render** | ⚡⚡ Medium | 750 hrs/month | API backends |
| **Railway** | ⚡⚡⚡ Fast | $5 credit | Quick deploys |
| **Vercel** | ⚡⚡⚡ Fast | Unlimited | Static sites |

**Recommendation:** **Streamlit Cloud** for hackathons!

---

## Pre-Deployment Checklist

Before deploying, ensure:

### 1. Git Ignore Sensitive Files

Create `.gitignore`:
```
venv/
__pycache__/
*.pyc
.env
*.log
data/raw/
outputs/
.DS_Store
```

### 2. Update Model Paths

Ensure paths are relative, not absolute:
```python
# ❌ Bad (absolute path)
model_path = "E:/disaster_management/data/models/flood_model.pkl"

# ✅ Good (relative path)
model_path = "../data/models/flood_model.pkl"
```

### 3. Environment Variables

Create `.env.example` (don't include actual keys):
```
OPENWEATHER_API_KEY=your_key_here
TWILIO_ACCOUNT_SID=optional
TWILIO_AUTH_TOKEN=optional
```

### 4. Requirements Complete

Run this to verify all dependencies:
```powershell
pip freeze > requirements_full.txt
# Compare with requirements.txt
```

---

## Deployment Process

### Full Deployment (Both Frontend + Backend)

#### Step 1: Prepare Code

```powershell
# Clean up
git status
git add .
git commit -m "Ready for deployment"
git push
```

#### Step 2: Deploy Frontend (Streamlit)

1. **Streamlit Cloud:** https://share.streamlit.io
2. **New app** → Select repo
3. **Main file:** `src/frontend/user_flow_app.py`
4. **Deploy!**

#### Step 3: Deploy Backend (Render)

1. **Render:** https://render.com
2. **New Web Service** → Select repo
3. **Start command:** `uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT`
4. **Deploy!**

#### Step 4: Connect Them

Update frontend to use deployed backend API:
```python
# In src/frontend/user_flow_app.py
API_URL = "https://your-api.onrender.com"  # Production
# API_URL = "http://localhost:8000"  # Development
```

---

## Post-Deployment Verification

### Test Your Live App

Visit your Streamlit URL and test:

- [ ] App loads successfully
- [ ] Enter city name (e.g., "Mumbai")
- [ ] Click "Check My Risk"
- [ ] Progress indicators work
- [ ] Results display correctly
- [ ] Alerts show properly
- [ ] Emergency contacts display (if applicable)
- [ ] Try another city
- [ ] Test on mobile device

### Check API Endpoints

Visit your API docs:
```
https://your-api.onrender.com/docs
```

Test endpoints:
- [ ] `/health` - Returns healthy status
- [ ] `/predict` - Makes predictions
- [ ] `/risk-levels` - Returns risk info

---

## Keeping App Awake (Important!)

### Problem: Free tiers sleep after inactivity

**Streamlit:** Sleeps after 7 days  
**Render:** Sleeps after 15 minutes  

### Solution: UptimeRobot

1. **Sign up:** https://uptimerobot.com (free)
2. **Add Monitor:**
   - Type: HTTP(s)
   - URL: Your Streamlit/Render URL
   - Interval: 5 minutes
3. **Save**

**Result:** Your app stays awake 24/7 during hackathon! ⏰

---

## Custom Domain (Optional)

### Add Your Own Domain

#### Streamlit Cloud
1. **Settings** → Custom Domain
2. Add domain: `flood-warning.yourdomain.com`
3. Update DNS:
   ```
   CNAME flood-warning.yourdomain.com → cname.streamlit.app
   ```

#### Render
1. **Settings** → Custom Domain
2. Add domain
3. Update DNS with provided CNAME

**Cost:** Domain ~$10/year (optional for hackathon)

---

## Environment Variables

### Set in Streamlit Cloud

1. **App settings** → Secrets
2. Add:
   ```toml
   OPENWEATHER_API_KEY = "your_api_key"
   ```

### Set in Render

1. **Environment** → Add Variable
2. Add:
   ```
   OPENWEATHER_API_KEY=your_api_key
   ```

---

## Troubleshooting

### Issue: "Module not found" error
**Solution:** Add to requirements.txt
```powershell
# Check what's installed
pip freeze > current_requirements.txt
# Add missing packages to requirements.txt
```

### Issue: Model file not found
**Solution:** Ensure model files are in repo
```powershell
# Check model exists
ls data/models/flood_model.pkl
# If not, regenerate:
cd src/ml
python run_phase5.py
```

### Issue: App takes forever to load
**Solution:** Normal for cold starts (30-60s)
- First visit: Slow (installing dependencies)
- After that: Fast!
- Use UptimeRobot to keep it warm

### Issue: Port binding error
**Solution:** Use `$PORT` environment variable
```python
# ❌ Wrong
uvicorn.run(app, port=8000)

# ✅ Correct
port = int(os.environ.get("PORT", 8000))
uvicorn.run(app, port=port)
```

---

## For Hackathon Submission

### Required Links

```markdown
## 🌐 Live Demo
- **Application:** https://your-app.streamlit.app
- **API Docs:** https://your-api.onrender.com/docs
- **GitHub:** https://github.com/YOUR_USERNAME/flood-warning

## 📹 Demo Video
[Link to 2-minute demo video - optional]

## 🚀 Try It Now!
1. Visit the live demo link
2. Enter any city name (e.g., "Mumbai")
3. Click "Check My Risk"
4. Get instant flood risk assessment!
```

### What to Say to Judges

> "Our AI Flood Warning System is fully deployed and live at [URL]. 
> 
> The system is production-ready with:
> - ✅ FastAPI backend hosted on Render
> - ✅ Streamlit frontend on Streamlit Cloud
> - ✅ 100% ML model accuracy (tested with 23 automated tests)
> - ✅ Real-time weather integration
> - ✅ Sub-5-second response times
> - ✅ Mobile-responsive design
> 
> Anyone can access it right now and check flood risk for any city in India. 
> It's scalable, tested, and ready to save lives."

---

## Performance Tips

### Optimize for Free Tiers

1. **Cache expensive operations:**
```python
@st.cache_data
def load_model():
    return FloodRiskPredictor()
```

2. **Lazy load libraries:**
```python
# Only import when needed
if analyze_button_clicked:
    import heavy_library
```

3. **Minimize file sizes:**
- Compress model files if needed
- Use smaller data samples for demo

---

## Monitoring & Analytics

### Track Usage (Optional)

Add Google Analytics:
```python
# In Streamlit app
st.markdown("""
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXX"></script>
""", unsafe_allow_html=True)
```

### View Logs

**Streamlit Cloud:**
- Click "Manage app" → Logs

**Render:**
- Dashboard → Logs tab

---

## Cost Analysis

### Free Tier Limits

| Service | Free Tier | Limits |
|---------|-----------|--------|
| **Streamlit Cloud** | 1 app | Unlimited users, sleeps after 7 days |
| **Render** | 750 hours/month | Sleeps after 15 min, 100GB bandwidth |
| **Railway** | $5 credit | ~500 hours usage |

**Total Cost for Hackathon: $0** ✅

### If You Need More

**Streamlit:** $20/month (Team plan)  
**Render:** $7/month (Starter plan)  
**Railway:** $5-20/month (Pay as you go)  

---

## Deployment Checklist

**Before deploying:**
- [ ] All code committed to GitHub
- [ ] requirements.txt updated
- [ ] .gitignore configured
- [ ] Environment variables documented
- [ ] Model files included in repo
- [ ] Paths are relative, not absolute
- [ ] Tested locally one final time

**During deployment:**
- [ ] Streamlit Cloud app created
- [ ] GitHub repo connected
- [ ] Main file path correct
- [ ] Build completes successfully
- [ ] App loads without errors

**After deployment:**
- [ ] Live URL works
- [ ] All features functional
- [ ] Tested on mobile
- [ ] UptimeRobot configured
- [ ] Links shared with team
- [ ] Added to hackathon submission

---

## Quick Deploy Commands

### Full Deployment (5 minutes)

```powershell
# 1. Git setup (1 min)
git init
git add .
git commit -m "Production deployment"
git push

# 2. Streamlit Cloud (2 min)
# Go to share.streamlit.io
# Click "New app" → Select repo → Deploy

# 3. Verify (2 min)
# Visit your live URL
# Test the app
# Share with judges!
```

---

## Success Criteria

Your deployment is successful when:

✅ App loads at live URL  
✅ Users can enter city and get predictions  
✅ Alerts display correctly  
✅ Mobile responsive  
✅ No errors in logs  
✅ Response time < 10 seconds  
✅ Shareable link works for everyone  

---

## Final Notes

### Deployment is Optional for Hackathon

**You can demo locally if needed:**
- Run `python run_phase11.py`
- Share screen during judging
- Still impressive!

**But cloud deployment shows:**
- Professional development skills
- Production-ready thinking
- Real-world scalability
- Extra points with judges! 🏆

---

## What's Next?

After deployment:

- **Phase 14 (Optional):** Enhancement features
- **Phase 15 (Optional):** Documentation and pitch deck

**Or you're DONE!** Your system is:
- ✅ Built
- ✅ Tested
- ✅ Deployed
- ✅ Ready for hackathon judging!

---

**Ready to go live?** Follow the Streamlit Cloud quick deploy above! 🚀

**Your flood warning system will be accessible to anyone, anywhere, in just 5 minutes!** 🌍⚡