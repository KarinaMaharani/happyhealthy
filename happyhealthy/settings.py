"""
Django settings for happyhealthy project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-lq$9%d3p%runkda2o8-#&ht6^9eows35h@cx=vi)5tlaw2gq-$')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
APP_ENV = os.getenv('APP_ENV', 'deployment' if os.getenv('VERCEL') else 'local')
IS_DEPLOYMENT = APP_ENV == 'deployment'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '10.0.2.2', 'happyhealthy.vercel.app', '.vercel.app']

# DrugBank API Configuration
DRUGBANK_API_KEY = os.getenv('DRUGBANK_API_KEY', '')
DRUGBANK_API_URL = 'https://api.drugbank.com/v1'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'authentication',
    'drug_checker',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'happyhealthy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'happyhealthy.wsgi.application'

# Database configuration
# Use PostgreSQL in production (Vercel), SQLite in development
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Whitenoise configuration for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.SessionAuthentication'],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
}

LOGIN_URL = '/auth/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Email Configuration
# Local option:
#   USE_SMTP_EMAIL=False
#   EMAIL_BACKEND will switch to Django's console backend for safe local testing.
# Deployment option:
#   USE_SMTP_EMAIL=True
#   Set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in your environment variables.
USE_SMTP_EMAIL = os.getenv('USE_SMTP_EMAIL', 'True' if IS_DEPLOYMENT else 'False') == 'True'

if USE_SMTP_EMAIL:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')  # Gmail App Password
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER or 'noreply@happyhealthy.local'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 25
    EMAIL_USE_TLS = False
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    DEFAULT_FROM_EMAIL = 'noreply@happyhealthy.local'

# Demo account toggles.
# Local option:
#   DEMO_ACCOUNTS_ENABLED=False to keep auth pages empty.
# Deployment option:
#   DEMO_ACCOUNTS_ENABLED=True to create mock patient/caregiver accounts and autofill login.
DEMO_ACCOUNTS_ENABLED = os.getenv('DEMO_ACCOUNTS_ENABLED', 'True' if IS_DEPLOYMENT else 'False') == 'True'
DEMO_AUTOFILL_ENABLED = os.getenv('DEMO_AUTOFILL_ENABLED', 'True' if DEMO_ACCOUNTS_ENABLED else 'False') == 'True'
SHOW_AUTH_DISCLAIMER = os.getenv('SHOW_AUTH_DISCLAIMER', 'True') == 'True'
DEMO_PATIENT_USERNAME = os.getenv('DEMO_PATIENT_USERNAME', 'demo_patient')
DEMO_PATIENT_PASSWORD = os.getenv('DEMO_PATIENT_PASSWORD', 'PatientDemo123!')
DEMO_PATIENT_EMAIL = os.getenv('DEMO_PATIENT_EMAIL', 'demo.patient@example.com')
DEMO_CAREGIVER_USERNAME = os.getenv('DEMO_CAREGIVER_USERNAME', 'demo_caregiver')
DEMO_CAREGIVER_PASSWORD = os.getenv('DEMO_CAREGIVER_PASSWORD', 'CaregiverDemo123!')
DEMO_CAREGIVER_EMAIL = os.getenv('DEMO_CAREGIVER_EMAIL', 'demo.caregiver@example.com')
EMAIL_VERIFICATION_REQUIRED = True
