# Vercel Deployment Guide for Happy Healthy

## 🚀 Quick Deploy to Vercel

### Prerequisites
- GitHub account with your code pushed
- Vercel account (sign up at https://vercel.com)

### Step 1: Connect to Vercel

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Click "Add New..." → "Project"

2. **Import GitHub Repository**
   - Click "Import Git Repository"
   - Select `KarinaMaharani/happyhealthy`
   - Click "Import"

### Step 2: Configure Environment Variables

In the Vercel project settings, add these environment variables:

```
DJANGO_SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=False
EMAIL_HOST_USER=karinamaharani.mipa2023@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

**To generate a new SECRET_KEY:**
```python
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Step 3: Deploy Settings

Vercel will auto-detect the configuration from `vercel.json`. Just click **"Deploy"**!

### Step 4: After Deployment

1. **Your app will be live at:** `https://happyhealthy.vercel.app`

2. **Important: Database Note**
   - Vercel uses serverless functions - SQLite won't persist
   - You need to use a hosted database like:
     - **Neon** (PostgreSQL): https://neon.tech (Free tier available)
     - **PlanetScale** (MySQL): https://planetscale.com (Free tier)
     - **Supabase** (PostgreSQL): https://supabase.com (Free tier)

### Step 5: Set Up PostgreSQL (Recommended)

#### Using Neon (Free PostgreSQL)

1. **Create Neon Account**
   - Go to https://neon.tech
   - Sign up and create a new project

2. **Get Database URL**
   - Copy the connection string (looks like: `postgresql://user:pass@host/db`)

3. **Update requirements.txt**
   Add to your requirements.txt:
   ```
   psycopg2-binary
   dj-database-url
   ```

4. **Add to Vercel Environment Variables**
   ```
   DATABASE_URL=postgresql://your-connection-string
   ```

5. **Update settings.py**
   I'll add the database configuration for you.

## ⚠️ Important Limitations

### DrugBank XML File
- The 1.8GB XML file **cannot** be deployed to Vercel (size limit)
- **Solutions:**
  1. Use external storage (AWS S3, Cloudinary)
  2. Use DrugBank API instead of XML file
  3. Extract and store data in PostgreSQL database

### Recommended Architecture for Production

```
┌─────────────────┐
│   Vercel App    │ ← Django app (serverless)
└────────┬────────┘
         │
         ├─→ PostgreSQL (Neon/Supabase) ← User data
         │
         └─→ AWS S3 / Cloudinary ← DrugBank XML
```

## 🔧 Post-Deployment Checklist

- [ ] Environment variables set
- [ ] Database connected (PostgreSQL)
- [ ] Static files collecting properly
- [ ] Email sending working
- [ ] DrugBank data accessible
- [ ] Test user registration
- [ ] Test caregiver-patient workflow

## 🐛 Troubleshooting

### "Application Error"
- Check Vercel logs in dashboard
- Verify all environment variables are set
- Check database connection

### Static files not loading
- Run `python manage.py collectstatic` locally
- Check `STATIC_ROOT` configuration
- Verify Whitenoise is installed

### Database errors
- Make sure `DATABASE_URL` is set
- Run migrations: `python manage.py migrate`
- Check PostgreSQL connection string

## 📱 Alternative: Deploy to Railway

If Vercel doesn't work well (serverless limitations), consider Railway:
- Better for Django apps (not serverless)
- Includes PostgreSQL database
- Easier file storage
- Visit: https://railway.app

## 🔗 Useful Links

- Vercel Dashboard: https://vercel.com/dashboard
- Vercel Docs: https://vercel.com/docs
- Django on Vercel Guide: https://vercel.com/guides/deploying-django-with-vercel

---

**After deployment, update your README with the live URL!** 🎉
