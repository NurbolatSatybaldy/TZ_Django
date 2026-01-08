"""Настройки Django проекта."""
import os
from pathlib import Path

from decouple import config

import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent


# Security / env
SECRET_KEY = config("DJANGO_SECRET_KEY", default="dev-secret-key-change-me")

DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)

# ALLOWED_HOSTS
ALLOWED_HOSTS_STR = config(
    "DJANGO_ALLOWED_HOSTS",
    default=".onrender.com,localhost,127.0.0.1",
)
ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS_STR.split(",") if h.strip()]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "shop",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# Локально: SQLite
# На Render/в проде: DATABASE_URL (Postgres) приходит из окружения
DATABASE_URL = config("DATABASE_URL", default="")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static / WhiteNoise
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

static_dirs = []
static_path = BASE_DIR / "static"
if static_path.exists():
    static_dirs.append(static_path)
STATICFILES_DIRS = static_dirs

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Stripe keys
STRIPE_PUBLISHABLE_KEY_RUB = config("STRIPE_PUBLISHABLE_KEY_RUB", default="")
STRIPE_SECRET_KEY_RUB = config("STRIPE_SECRET_KEY_RUB", default="")
STRIPE_PUBLISHABLE_KEY_USD = config("STRIPE_PUBLISHABLE_KEY_USD", default="")
STRIPE_SECRET_KEY_USD = config("STRIPE_SECRET_KEY_USD", default="")


# Production hardening (Render behind proxy)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


    CSRF_TRUSTED_ORIGINS_STR = config("CSRF_TRUSTED_ORIGINS", default="")
    if CSRF_TRUSTED_ORIGINS_STR:
        CSRF_TRUSTED_ORIGINS = [
            x.strip() for x in CSRF_TRUSTED_ORIGINS_STR.split(",") if x.strip()
        ]