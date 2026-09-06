"""
Django settings for config project.
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# =========================================================
# BASE
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# .env fayli har doim project root papkasida (manage.py bilan bir qatorda)
# bo'lishi kerak. Bu yerda aniq yo'l ko'rsatilgani uchun, qaysi joydan
# ishga tushirilishidan qat'iy nazar (systemd, gunicorn, cPanel, va h.k.)
# .env fayli to'g'ri topiladi.
load_dotenv(BASE_DIR / ".env")


# =========================================================
# DEPLOYMENT / ENVIRONMENT SWITCH
# =========================================================

# .env faylida DEPLOYMENT=local  yoki  DEPLOYMENT=production deb yoziladi.
# Shu bitta o'zgaruvchi orqali DEBUG, HTTPS, cookie xavfsizligi va
# boshqa bog'liq sozlamalarning barchasi avtomatik almashadi.
DEPLOYMENT = os.getenv("DEPLOYMENT", "local").strip().lower()

if DEPLOYMENT not in ("local", "production"):
    raise ValueError(
        "DEPLOYMENT environment variable noto'g'ri qiymatga ega: "
        f"'{DEPLOYMENT}'. Faqat 'local' yoki 'production' bo'lishi kerak."
    )

IS_PRODUCTION = DEPLOYMENT == "production"

# DEBUG endi DEPLOYMENT orqali avtomatik belgilanadi.
# Xohlasangiz .env orqali qo'lda ustiga chiqarish uchun DEBUG_OVERRIDE
# qoldirilgan (odatda kerak bo'lmaydi).
_debug_override = os.getenv("DEBUG_OVERRIDE")
if _debug_override is not None:
    DEBUG = _debug_override.strip().lower() in ("true", "1", "yes", "on")
else:
    DEBUG = not IS_PRODUCTION


# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")


ALLOWED_HOSTS = (
    [h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()]
    if os.getenv("ALLOWED_HOSTS")
    else (["localhost", "127.0.0.1"] if not IS_PRODUCTION else [])
)

CSRF_TRUSTED_ORIGINS = (
    [o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]
    if os.getenv("CSRF_TRUSTED_ORIGINS")
    else []
)


# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local apps
    "accounts",
    "dashboard",
    "groups",
    "assignments",
    "reading",
    "listening",
    "videos",
    "progress",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "accounts.middleware.ActiveUntilMiddleware",
]


# =========================================================
# URL / WSGI
# =========================================================

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =========================================================
# DATABASE
# =========================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# =========================================================
# AUTHENTICATION
# =========================================================

AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = [
    "accounts.backends.ActiveUntilModelBackend",
]

LOGIN_URL = "accounts:login"

LOGOUT_REDIRECT_URL = "accounts:login"


# =========================================================
# SESSION / COOKIES
# =========================================================

# Django session stored in database
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# Prevent JavaScript from reading session cookie
SESSION_COOKIE_HTTPONLY = IS_PRODUCTION

# Faqat production (HTTPS) muhitida cookie faqat https orqali yuborilsin
SESSION_COOKIE_SECURE = IS_PRODUCTION

# Cookie is available for normal same-site navigation
SESSION_COOKIE_SAMESITE = "Lax" if IS_PRODUCTION else None


# =========================================================
# CSRF
# =========================================================

# Keep CSRF cookie readable by JavaScript when necessary.
# Django's normal CSRF mechanism does not require HttpOnly.
CSRF_COOKIE_HTTPONLY = IS_PRODUCTION

# HTTPS
CSRF_COOKIE_SECURE = IS_PRODUCTION

CSRF_COOKIE_SAMESITE = "Lax"


# =========================================================
# HTTPS / SECURITY
# =========================================================

if IS_PRODUCTION:
    # Tell Django that HTTPS is being terminated/proxied by the web server.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # Redirect HTTP -> HTTPS
    SECURE_SSL_REDIRECT = True

    # HSTS
    # Start with a small value while testing, keyingi qadamda oshirish mumkin.
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "3600"))

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    # Don't enable preload until you are 100% sure.
    SECURE_HSTS_PRELOAD = False
else:
    # Local rejimda HTTPS majburiy emas, shuning uchun bularning barchasi
    # o'chirilgan holda qoladi (Django default qiymatlari: False / None).
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = None
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# =========================================================
# MEDIA FILES
# =========================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# =========================================================
# EMAIL
# =========================================================

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"