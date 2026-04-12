import os
from pathlib import Path

import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "faralyar-dev-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "true").lower() == "true"
ALLOWED_HOSTS = [host for host in os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if host]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "accounts",
    "ai_platform",
    "billing",
    "blog",
    "dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "faralyar_project.urls"

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
                "faralyar_project.context_processors.site_context",
            ],
        },
    },
]

WSGI_APPLICATION = "faralyar_project.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fa"
LANGUAGES = [("fa", "فارسی"), ("en", "English")]
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"
AUTHENTICATION_BACKENDS = [
    "faralyar_project.auth_backends.EmailOrMobileBackend",
    "django.contrib.auth.backends.ModelBackend",
]

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "dashboard:home"
LOGOUT_REDIRECT_URL = "core:home"

EMAIL_BACKEND = os.getenv("DJANGO_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@faralyar.ir")

OTP_CODE_LENGTH = int(os.getenv("OTP_CODE_LENGTH", "6"))
OTP_EXPIRY_MINUTES = int(os.getenv("OTP_EXPIRY_MINUTES", "5"))
OTP_PROVIDER_NAME = os.getenv("OTP_PROVIDER_NAME", "")
OTP_PROVIDER_API_KEY = os.getenv("OTP_PROVIDER_API_KEY", "")
OTP_PROVIDER_SENDER = os.getenv("OTP_PROVIDER_SENDER", "")

ZARINPAL_MERCHANT_ID = os.getenv("ZARINPAL_MERCHANT_ID", "")
ZARINPAL_SANDBOX = os.getenv("ZARINPAL_SANDBOX", "true").lower() == "true"
ZARINPAL_START_URL = (
    "https://sandbox.zarinpal.com/pg/StartPay/"
    if ZARINPAL_SANDBOX
    else "https://www.zarinpal.com/pg/StartPay/"
)
ZARINPAL_REQUEST_URL = (
    "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    if ZARINPAL_SANDBOX
    else "https://api.zarinpal.com/pg/v4/payment/request.json"
)
ZARINPAL_VERIFY_URL = (
    "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    if ZARINPAL_SANDBOX
    else "https://api.zarinpal.com/pg/v4/payment/verify.json"
)
