# Happy Healthy - Quick Start Guide

## ⚠️ IMPORTANT: DrugBank XML File Not Included

The DrugBank XML database file (`full database.xml`) is **NOT included** in this repository because:
- File size: 1.8 GB (exceeds GitHub's 100 MB limit)
- Contains licensed data that shouldn't be publicly distributed
- Too large for version control

### How to Download Database
Please refer to DRUGBANK_SETUP_REQUIRED.md Document   
You may use the following Google Drive to download the XML : https://go.drugbank.com/releases/5-1-14/downloads/all-full-database   
After downloading the file please extract the xml into the "static/" folder  
The project should have the mapping "static/full database.xml"

## 🎉 Your Django Application is Ready!

A curative-focused mobile application to tackle psychiatric medication challenges built with Django and DrugBank Database

## 📋 What's Been Created

### 1. **Logout System** ✓
- Added logout button in header (visible when logged in)
- Custom logout view that clears session and redirects properly
- Shows success message after logout

### 2. **Search Button** ✓
- Changed from text "Search" to clean 🔍 icon
- Added gradient background (blue-500 to blue-600)
- Improved hover effects with scale animation
- Better shadow and visual appeal

### 3. **Guest Access** ✓
- New landing page at root URL (`/`)
- Three options: Continue as Guest, Login, or Register
- Beautiful gradient purple background
- Guest session tracked separately
- Limited features for guests (can't save drugs or view history)

### 4. **Patient/Caregiver Roles** ✓
- Added `UserProfile` model with role field
- Registration form now asks: "I am a:" with visual cards
  - 🤒 Patient
  - 👨‍⚕️ Caregiver
- Role displayed in header next to username
- Database migration applied successfully

## 🎨 New Features

### Landing Page (`/`)
- Beautiful welcome screen
- Three buttons:
  1. **Continue as Guest** - Quick access, limited features
  2. **Login** - For existing users
  3. **Create Account** - For new users (Patient/Caregiver)
- Features preview section

### Enhanced Registration
- Visual role selection with cards
- Email field required
- Better form styling with focus states
- Password validation
- Clean, modern UI

### Header Improvements
- Shows username and role for logged-in users
- Logout button with hover effects
- "Guest Mode" indicator for guests

### Install Dependencies (if not already done)
```bash
pip install -r requirements.txt
```

### Start the Server
```bash
python manage.py runserver
```

### 5. Access the Application
Open your browser and go to:
- **Home Page**: http://127.0.0.1:8000/
- **Search Drugs**: http://127.0.0.1:8000/drugs/search/
- **Check Interactions**: http://127.0.0.1:8000/drugs/interaction/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 🔑 Create Admin User (Optional)
```bash
python manage.py createsuperuser
```

## 📱 Features Implemented

### ✅ Core Features
- **Drug Search**: Search DrugBank's database for medications
- **Interaction Checker**: Check drug-drug interactions
- **Drug Details**: View comprehensive drug information
- **User Authentication**: Register, login, logout
- **Save Favorites**: Bookmark frequently used drugs (requires login)
- **Search History**: Track previous searches (requires login)

### ✅ Mobile-Like Interface
- Fixed 400px width container
- Centered on desktop
- Bottom navigation bar
- Touch-friendly buttons
- Card-based design
- Responsive layout

### ✅ Technical Features
- Django 5.1.3 framework
- SQLite database
- DrugBank API integration
- RESTful architecture
- CSRF protection
- Session authentication

## 📂 Key Files to Know

### Database Models (`drug_checker/models.py`)
- `DrugSearch`: Stores search history
- `DrugInteractionCheck`: Stores interaction check history
- `SavedDrug`: User's saved favorite drugs

### API Service (`drug_checker/services.py`)
- `DrugBankAPIService`: Handles all DrugBank API calls
  - `search_drugs()`: Search for drugs
  - `get_drug_details()`: Get detailed drug info
  - `check_drug_interactions()`: Check interactions
  - `get_drug_indications()`: Get drug uses
  - `get_adverse_effects()`: Get side effects

### Views (`drug_checker/views.py`)
- `search_drugs`: Drug search page
- `drug_detail`: Drug information page
- `interaction_checker`: Interaction checker page
- `history`: User search history
- `saved_drugs`: User's saved drugs

## 🎨 Customization

### Colors (in `templates/base.html`)
Current color scheme:
- Primary: Blue (`bg-blue-500`)
- Warning: Red (`bg-red-500`)
- Success: Green (`bg-green-500`)

### Mobile Width
Change `.mobile-container max-width` in `templates/base.html`:
```css
.mobile-container {
    max-width: 400px;  /* Change this value */
}
```

## 🔧 Common Tasks

### Add New Pages
1. Create view in `app/views.py`
2. Add URL pattern in `app/urls.py`
3. Create template in `templates/app/`

### Modify Navigation
Edit the bottom nav section in `templates/base.html`

### Add More API Features
Extend `drug_checker/services.py` with new DrugBank endpoints

## ⚠️ Important Notes

1. **API Key Required**: The app won't work without a valid DrugBank API key
2. **Development Mode**: DEBUG=True in settings (change for production)
3. **Database**: Using SQLite (consider PostgreSQL for production)
4. **Mobile-Like**: Designed for PC but with mobile interface aesthetics

## 🐛 Troubleshooting

### "API error: 401"
- Check your DrugBank API key in `.env` file
- Verify the key is active on DrugBank website

### "No module named..."
- Run: `pip install -r requirements.txt`

### Templates not found
- Ensure `templates/` folder exists
- Check `TEMPLATES` setting in `settings.py`

### Static files not loading
- Run: `python manage.py collectstatic` (for production)
- Check `STATIC_URL` in settings.py

## 📚 Next Steps

### To Add:
1. More templates (history.html, saved_drugs.html, drug_detail.html)
2. JavaScript for enhanced UX
3. More DrugBank API endpoints
4. Data export features
5. Advanced search filters
6. Notifications system

### For Production:
1. Set `DEBUG=False`
2. Use PostgreSQL database
3. Set up proper `ALLOWED_HOSTS`
4. Configure static file serving
5. Enable HTTPS
6. Set up logging

## 🤝 Support

- Django Documentation: https://docs.djangoproject.com/
- DrugBank API Docs: https://docs.drugbank.com/v1/
- Tailwind CSS: https://tailwindcss.com/docs

## ✨ Created With
- Django 5.1.3
- Tailwind CSS
- DrugBank Clinical API v1
- SQLite3

---

**Happy Coding! 🚀**

*Remember to never commit your `.env` file or share your API keys!*


---

# Email Verification & Caregiver-Patient Monitoring System

## 🎯 New Features Implemented

### 1. **Email Verification System** ✓
- **Automatic email on registration** - Users receive verification link via email
- **24-hour token validity** - Links expire after 24 hours for security
- **Resend verification** - Users can request new verification emails
- **Visual indicator** - Unverified users see warning in header
- **Console backend** - For development, emails print to console (easy to switch to SMTP for production)

### 2. **Caregiver-Patient Monitoring** ✓
- **Username + Email verification** - Both must match to prevent spam/unauthorized access
- **Request/Approval workflow**:
  1. Caregiver requests to monitor using patient's username AND email
  2. Patient receives email notification
  3. Patient approves or rejects request
  4. Only after approval can caregiver see patient data
- **Relationship statuses**: Pending, Active, Rejected, Removed
- **Email notifications** sent at each step

### 3. **Role-Based Dashboards** ✓

#### **Caregiver Dashboard** (`/auth/caregiver-dashboard/`)
- View all patients (active, pending, rejected)
- Add new patients to monitor
- View patient activity (drugs, searches, interactions)
- Remove patients from monitoring
- Statistics: Active patients, pending requests

#### **Patient Requests** (`/auth/patient-requests/`)
- View all caregiver requests
- Approve or reject monitoring requests
- See active caregivers
- Notification badge for pending requests

### 4. **Patient Activity Monitoring** (`/auth/patient-activity/<id>/`)
Caregivers can view:
- ✅ Saved medications with notes
- ✅ Recent interaction checks with severity levels
- ✅ Search history
- ✅ Statistics summary

## 📊 Database Models

### **UserProfile** (updated)
```python
- email_verified (Boolean)
- verification_token (String, 100 chars)
- verification_token_created (DateTime)
```

### **CaregiverPatientRelationship** (new)
```python
- caregiver (FK to User)
- patient (FK to User)
- status (pending/active/rejected/removed)
- request_date (DateTime)
- approved_date (DateTime, nullable)
- notes (Text)
```

## 🔐 Security Features

1. **Double verification**: Username AND email must match
2. **Email notifications**: Both parties notified of all actions
3. **Approval required**: Caregiver can't see data until patient approves
4. **Token expiration**: Verification tokens expire in 24 hours
5. **Unique relationships**: Can't duplicate caregiver-patient pairs
6. **Status tracking**: Full audit trail of relationship changes

## 🎨 UI Updates

### **Bottom Navigation**
- **Caregivers** see: Home | Search | Check | 👨‍⚕️ Patients | Saved
- **Patients** see: Home | Search | Check | 👥 Caregivers | Saved

### **Header**
- Shows verification status (⚠️ Unverified)
- Yellow banner prompts unverified users to verify email
- Role displayed next to username

## 📧 Email Configuration

### **Development** (Current)
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
Emails print to console/terminal - easy for testing!

### **Production** (To enable)
Uncomment in `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
```

Then add to `.env`:
```
EMAIL_HOST_USER=hostemail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🚀 User Flows

### **Caregiver Flow**
1. Register as Caregiver
2. Navigate to 👨‍⚕️ Patients (bottom nav)
3. Click "Add Patient"
4. Enter patient's exact username AND email
5. Wait for patient approval
6. Once approved, view patient's medication activity

### **Patient Flow**
1. Register as Patient
2. Receive email: "Caregiver wants to monitor you"
3. Navigate to 👥 Caregivers (bottom nav)
4. See pending request with Approve/Reject buttons
5. Click Approve
6. Caregiver can now see your drug activity

### **Email Verification Flow**
1. Register account
2. See yellow warning banner
3. Check email (or console in dev mode)
4. Click verification link
5. Email marked as verified
6. Warning banner disappears

## 🔗 New URL Routes

```
/auth/verify-email/<token>/          - Verify email with token
/auth/resend-verification/           - Resend verification email
/auth/add-patient/                   - Add patient to monitor (caregiver only)
/auth/caregiver-dashboard/           - Caregiver dashboard
/auth/patient-requests/              - Patient's caregiver requests
/auth/approve-caregiver/<id>/        - Approve monitoring request
/auth/reject-caregiver/<id>/         - Reject monitoring request
/auth/remove-patient/<id>/           - Remove patient from monitoring
/auth/patient-activity/<patient_id>/ - View patient activity
```

## 🎉 Ready to Use!

All migrations applied successfully. The app now has:
- ✅ Full email verification system
- ✅ Secure caregiver-patient monitoring
- ✅ Role-based dashboards
- ✅ Email notifications
- ✅ Activity tracking

Start the server and test it out!


---


# DrugBank Setup Guide

The application now uses direct XML file loading (no buggy downloader needed!).

## Setup Steps

1. **Download DrugBank XML**
   - Go to: https://go.drugbank.com/releases/latest
   - Login with credentials (check your email for "DrugBank Account Confirmation")
   - Click "Full Database" under Downloads
   - Download: `drugbank_all_full_database.xml.zip` (~100MB)

2. **Extract and Place File**
   
   **Option A (Recommended):**
   - Create folder: `C:\Users\<YourUsername>\.data\drugbank\`
   - Extract the ZIP file
   - Copy `full database.xml` to the folder above
   - Rename to `drugbank.xml` (or keep as `full database.xml`)

   **Option B (Project folder):**
   - Create folder: `happyhealthy\data\`
   - Place extracted XML file there

3. **Restart Server**
   ```
   python manage.py runserver
   ```

4. **Test**
   - Search for any drug (e.g., "lansoprazole")
   - First load takes ~30 seconds (parsing 2GB XML file)
   - Subsequent searches are instant (cached in memory)

## File Locations Checked

The app automatically checks these locations:
1. `C:\Users\<YourUsername>\.data\drugbank\drugbank.xml`
2. `C:\Users\<YourUsername>\.data\drugbank\full database.xml`
3. `happyhealthy\data\drugbank.xml`
4. `happyhealthy\data\full database.xml`

## Status

- ✅ Direct XML loading (no buggy package)
- ✅ Email verification working
- ✅ User profiles auto-created
- ✅ Autocomplete working
- 📝 Just need to download XML file once


---


# Gmail Email Setup Instructions

## Steps to Enable Email Sending

### 1. Generate Gmail App Password
Since Google disabled "less secure apps", you need to use an App Password:

1. Go to your Google Account: https://myaccount.google.com/security
2. **Enable 2-Step Verification** (required for App Passwords)
   - Click "2-Step Verification"
   - Follow the setup process
3. **Create App Password**
   - Go back to Security settings
   - Search for "App Passwords" or go to https://myaccount.google.com/apppasswords
   - Click "Select app" → Choose "Mail"
   - Click "Select device" → Choose "Windows Computer" (or "Other")
   - Click "Generate"
   - **Copy the 16-character password** (it will look like: `abcd efgh ijkl mnop`)

### 2. Configure Your Application

#### Option A: Using Environment Variables (Recommended)
1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` file and add your credentials:
   ```
   EMAIL_HOST_USER=hostemail@gmail.com
   EMAIL_HOST_PASSWORD=abcdefghijklmnop
   ```
   ⚠️ **Remove all spaces from the app password!**

3. Install python-decouple to load .env:
   ```powershell
   pip install python-decouple
   ```

#### Option B: Direct Configuration (Not Recommended for Production)
The app password is already set in `settings.py`, but you need to add it as an environment variable:

```powershell
$env:EMAIL_HOST_PASSWORD="your-app-password-here"
python manage.py runserver
```

### 3. Test Email Sending

After configuration, try adding a patient to trigger an email notification.

## Troubleshooting

### "Authentication Failed" Error
- Make sure 2-Step Verification is enabled
- Use App Password, not your regular Gmail password
- Remove all spaces from the app password
- Make sure EMAIL_HOST_USER matches the Gmail account that generated the App Password

### Emails Not Arriving
- Check spam folder
- Verify the recipient email is correct
- Check Django console for error messages
- Try sending a test email from Django shell:
  ```python
  from django.core.mail import send_mail
  send_mail('Test', 'This is a test', 'hostemail@gmail.com', ['recipient@example.com'])
  ```

### Rate Limiting
Gmail has sending limits:
- 500 emails per day for regular Gmail
- 2000 emails per day for Google Workspace

## Security Notes

⚠️ **Never commit `.env` file to Git!**
- The `.env` file is already in `.gitignore`
- App Passwords should be kept secret
- Rotate App Passwords periodically
- Revoke unused App Passwords from your Google Account


---



