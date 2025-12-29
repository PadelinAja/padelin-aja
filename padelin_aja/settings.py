"""
Django settings for padelin_aja project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-#*l_#)k$hz4-zjn(adcl@brg98i+56)^%$kieyfit6k7_zd)u8")
PRODUCTION = os.getenv("PRODUCTION", "False").lower() == "true"

# NOTE: For better safety set DEBUG via env var; here we default to True for local dev.
DEBUG = not PRODUCTION

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "roben-joseph-padelinaja.pbp.cs.ui.ac.id",
]

CSRF_TRUSTED_ORIGINS = [
    'https://roben-joseph-padelinaja.pbp.cs.ui.ac.id',
]

INSTALLED_APPS = [
    # local apps
    'main',
    'authentication',

    # third-party
    'corsheaders',  # <--- added for CORS handling; install `django-cors-headers`
    'rest_framework',

    # contrib
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    # corsheaders middleware must be placed before CommonMiddleware
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "padelin_aja.urls"

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


LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend"
]


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Jakarta"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ----------------------
# REST Framework / JWT
# ----------------------
# Install: pip install djangorestframework djangorestframework-simplejwt
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}


# ----------------------
# CORS Configuration
# ----------------------
# Install: pip install django-cors-headers
#
# Secure practice:
# - In production, list only the allowed origins in CORS_ALLOWED_ORIGINS.
# - Avoid CORS_ALLOW_ALL_ORIGINS = True in production unless you understand the implications.
#

# Start with the production host(s) (scheme included)
CORS_ALLOWED_ORIGINS = [
    "https://roben-joseph-padelinaja.pbp.cs.ui.ac.id",
]

# Add common local development origins when DEBUG is True
# ... existing DEBUG block ...
if DEBUG:
    CORS_ALLOWED_ORIGINS += [
        "http://localhost:61658",
        "http://127.0.0.1:61658",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        # Add your flutter web dev ports
        "http://localhost:64524",
        "http://127.0.0.1:64524",
        "http://localhost:54174",
        "http://127.0.0.1:54174",
        "https://localhost:62638",
        "https://127.0.1:62638",
    ]

# If you need credentials (cookies, session auth) from the browser:
CORS_ALLOW_CREDENTIALS = True

# Allow common headers (authorization for token auth, content-type, etc.)
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Optionally allow additional methods (defaults include GET/POST/OPTIONS)
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

# Optional: if you want to allow all origins during quick local testing only
# (NOT recommended for production). You can toggle it via an env var:
if os.getenv("CORS_ALLOW_ALL_ORIGINS", "False").lower() == "true":
    CORS_ALLOW_ALL_ORIGINS = True