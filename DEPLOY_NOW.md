# 🚀 Deploy Happy Healthy to Vercel - Quick Guide

## Step-by-Step Deployment

### 1. Go to Vercel
Visit: https://vercel.com/new

### 2. Import Your GitHub Repository
- Click "Import Git Repository"
- Search for: `KarinaMaharani/happyhealthy`
- Click "Import"

### 3. Configure Project

**Framework Preset:** Other
**Root Directory:** ./
**Build Command:** (leave default)
**Output Directory:** (leave default)

### 4. Add Environment Variables

Click "Environment Variables" and add:

```
DJANGO_SECRET_KEY
```
Value: Generate using:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

```
DEBUG
```
Value: `False`

```
EMAIL_HOST_USER
```
Value: `karinamaharani.mipa2023@gmail.com`

```
EMAIL_HOST_PASSWORD
```
Value: Your Gmail App Password (from GMAIL_SETUP.md)

### 5. Set Up Database (REQUIRED)

#### Option A: Neon PostgreSQL (Recommended - Free)

1. Go to https://neon.tech
2. Sign up and create a new project
3. Copy the connection string
4. Add to Vercel:
   ```
   DATABASE_URL
   ```
   Value: `postgresql://username:password@host/database`

#### Option B: Supabase PostgreSQL (Alternative - Free)

1. Go to https://supabase.com
2. Create new project
3. Go to Settings → Database
4. Copy "Connection string" (URI format)
5. Add to Vercel as `DATABASE_URL`

### 6. Deploy!

Click **"Deploy"** button

### 7. Wait for Deployment
- First deployment: ~2-5 minutes
- Vercel will build and deploy automatically

### 8. Your App is Live! 🎉

Visit: **https://happyhealthy.vercel.app**

---

## ⚠️ Important Notes

### DrugBank XML File Limitation
The 1.8GB XML file **cannot** be deployed to Vercel. You have two options:

#### Option 1: Upload to Cloud Storage
1. Upload `full database.xml` to AWS S3 or Cloudinary
2. Update `drug_checker/services.py` to download from URL
3. Cache in memory on first load

#### Option 2: Import to PostgreSQL
1. Parse XML locally
2. Import drug data into PostgreSQL database
3. Update queries to use database instead of XML

**For now, the app will deploy but drug search won't work until you implement one of these solutions.**

---

## 🔧 Post-Deployment Tasks

1. **Run Migrations**
   - Vercel automatically runs migrations in `build.sh`
   - Check deployment logs to verify

2. **Create Superuser** (Admin Access)
   - Can't run interactively on Vercel
   - Options:
     a) Create via Django admin after deploying
     b) Use Railway/Render instead (they support shell access)

3. **Test Features**
   - User registration ✓
   - Login/Logout ✓
   - Email sending ✓
   - Drug search ✗ (needs XML solution)

---

## 🐛 Troubleshooting

### Deployment Failed
- Check Vercel deployment logs
- Verify all environment variables are set
- Make sure `DATABASE_URL` is correct

### 500 Internal Server Error
- Check Vercel function logs
- Verify `SECRET_KEY` is set
- Check database connection

### Static Files Not Loading
- Should work automatically with Whitenoise
- Check `STATIC_ROOT` in settings

### Database Connection Error
- Verify `DATABASE_URL` format
- Check PostgreSQL database is running
- Ensure IP whitelist includes Vercel IPs

---

## 📱 Alternative: Deploy to Railway (Easier for Django)

If Vercel is too complicated, try Railway:

1. Go to https://railway.app
2. "New Project" → "Deploy from GitHub repo"
3. Select `KarinaMaharani/happyhealthy`
4. Railway automatically provisions PostgreSQL
5. No serverless limitations!

Railway is better for Django apps with large files.

---

## ✅ Deployment Checklist

- [ ] GitHub repository pushed
- [ ] Vercel account created
- [ ] Repository imported to Vercel
- [ ] Environment variables set
- [ ] PostgreSQL database created (Neon/Supabase)
- [ ] DATABASE_URL added to Vercel
- [ ] First deployment successful
- [ ] Website accessible at happyhealthy.vercel.app
- [ ] User registration working
- [ ] Email notifications working
- [ ] Drug search solution implemented

---

**Need help?** Check VERCEL_DEPLOYMENT.md for detailed instructions!
