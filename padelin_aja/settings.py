"""
Django settings for padelin_aja project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# ───────────────────────────────────────────────
# Base setup
# ───────────────────────────────────────────────
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-#*l_#)k$hz4-zjn(adcl@brg98i+56)^%$kieyfit6k7_zd)u8")
PRODUCTION = os.getenv("PRODUCTION", "False").lower() == "true"

DEBUG = not PRODUCTION

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "roben-joseph-padelinaja.pbp.cs.ui.ac.id",
]

# ───────────────────────────────────────────────
# Applications
# ───────────────────────────────────────────────
INSTALLED_APPS = [
    'main',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "padelin_aja.urls"

# ───────────────────────────────────────────────
# Templates
# ───────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = "padelin_aja.wsgi.application"

# ───────────────────────────────────────────────
# Database (PostgreSQL for production / SQLite local)
# ───────────────────────────────────────────────
if PRODUCTION:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT"),
            "OPTIONS": {
                "options": f"-c search_path={os.getenv('SCHEMA', 'public')}"
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ───────────────────────────────────────────────
# Authentication & Login flow
# ───────────────────────────────────────────────
LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/"        # after logout
LOGIN_REDIRECT_URL = "/"         # after login success
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend"
]

# ───────────────────────────────────────────────
# Email backend (for dev; used by password reset later if added)
# ───────────────────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ───────────────────────────────────────────────
# Password validators
# ───────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ───────────────────────────────────────────────
# Internationalization
# ───────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Jakarta"  # change from UTC to local for convenience
USE_I18N = True
USE_TZ = True

# ───────────────────────────────────────────────
# Static files (CSS, JS, images)
# ───────────────────────────────────────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "main" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# ───────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
