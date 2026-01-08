"""Настройки Django проекта."""
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY", default="dev-secret-key-change-me")

DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)

# ALLOWED_HOSTS настройка
ALLOWED_HOSTS_STR = config("DJANGO_ALLOWED_HOSTS", default="")
if ALLOWED_HOSTS_STR:
    ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS_STR.split(",") if h.strip()]
else:
    # По умолчанию разрешаем все хосты для упрощения деплоя
    ALLOWED_HOSTS = ["*"]

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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Создаем список директорий только если они существуют
static_dirs = []
if os.path.exists(BASE_DIR / "static"):
    static_dirs.append(BASE_DIR / "static")
STATICFILES_DIRS = static_dirs

# WhiteNoise для обслуживания статических файлов в production
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Настройки Stripe через переменные окружения
STRIPE_PUBLISHABLE_KEY_RUB = config("STRIPE_PUBLISHABLE_KEY_RUB", default="")
STRIPE_SECRET_KEY_RUB = config("STRIPE_SECRET_KEY_RUB", default="")
STRIPE_PUBLISHABLE_KEY_USD = config("STRIPE_PUBLISHABLE_KEY_USD", default="")
STRIPE_SECRET_KEY_USD = config("STRIPE_SECRET_KEY_USD", default="")

# Для production: если DEBUG=False, используем более строгие настройки
if not DEBUG:
    # В production лучше указать конкретный домен, но для тестирования оставляем *
    pass




