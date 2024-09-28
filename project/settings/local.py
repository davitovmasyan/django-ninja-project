import os
from datetime import timedelta

from .base import ENV, BASE_DIR, PROJECT_DIR

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV.str('SECRET_KEY', 'Keep it secret!')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV.bool('DEBUG', True)

ALLOWED_HOSTS = ENV.list('ALLOWED_HOSTS', default=['*'])
INTERNAL_IPS = ENV.list('INTERNAL_IPS', default=('127.0.0.1',))

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

EXTERNAL_APPS = [
    'corsheaders',
    'ninja_extra',
    'ninja_jwt',
    'django_extensions',
    'django_countries',
]

# Local Application definition

LOCAL_APPS = [
    'core',
    'accounts',
]

if DEBUG:
    EXTERNAL_APPS.append('debug_toolbar')

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': ENV.db_url('DATABASE_URL', default='sqlite://:memory:'),
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        },
    },
]

# User settings
AUTH_USER_MODEL = 'accounts.User'

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = "True"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600

# https://github.com/vintasoftware/safari-samesite-cookie-issue
CSRF_COOKIE_SAMESITE = None
SESSION_COOKIE_SAMESITE = None
CSRF_TRUSTED_ORIGINS = [
    'http://project.localhost:8000',
]
CSRF_COOKIE_DOMAIN = '.example.com'

CORS_ALLOWED_ORIGINS = ENV.list('CORS_ALLOWED_ORIGINS', default=[
    "http://localhost:3000",
])

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{filename} {levelname} {asctime} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': os.getenv('LOG_LEVEL', 'DEBUG'),
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    },
}

NINJA_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

APPEND_SLASH = True

NINJA_PAGINATION_PER_PAGE = 20
NINJA_PAGINATION_MAX_LIMIT = 100

# Email settings
DEFAULT_FROM_EMAIL = ENV.str("DEFAULT_FROM_EMAIL", "from@example.com")
EMAIL_BASE_TEMPLATE = "email/base.html"
EMAIL_HOST = ENV.str("EMAIL_HOST", "localhost")
EMAIL_PORT = ENV.int("EMAIL_PORT", 25)
EMAIL_BACKEND = ENV.str("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST_USER = ENV.str('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = ENV.str('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = ENV.bool('EMAIL_USE_TLS', False)
EMAIL_REPLY_TO = 'contact@project.com'

SITE_NAME = 'Django Ninja Project'

DEFAULT_CLIENT_DOMAIN = 'localhost:3000'
CLIENT_DOMAIN = ENV.str('CLIENT_DOMAIN', DEFAULT_CLIENT_DOMAIN)
if not CLIENT_DOMAIN:
    CLIENT_DOMAIN = DEFAULT_CLIENT_DOMAIN
URL_SCHEME = 'https'
