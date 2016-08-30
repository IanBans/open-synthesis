"""
Django settings for openintel project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

# http://bruno.im/2013/may/18/django-stop-writing-settings-files/

import os
import dj_database_url
import environ
import logging
import sys

logger = logging.getLogger(__name__)


# https://stackoverflow.com/questions/4088253/django-how-to-detect-test-environment
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Set defaults and read .env file from root directory
# Defaults should be "safe" from a security perspective
env = environ.Env(
    DEBUG=(bool, False),
    DJANGO_LOG_LEVEL=(str, "ERROR"),
    APP_LOG_LEVEL=(str, "ERROR"),
    CERTBOT_PUBLIC_KEY=(str, None),
    CERTBOT_SECRET_KEY=(str, None),
    SECURE_SSL_REDIRECT=(bool, True),
    SECURE_BROWSER_XSS_FILTER=(bool, True),
    SECURE_CONTENT_TYPE_NOSNIFF=(bool, True),
    SECURE_HSTS_INCLUDE_SUBDOMAINS=(bool, True),
    SECURE_HSTS_SECONDS=(int, 31536000),  # default to maximum age in seconds
    ROLLBAR_ACCESS_TOKEN=(str, None),
    ACCOUNT_EMAIL_REQUIRED=(bool, True),
    SENDGRID_USERNAME=(str, None),
    SENDGRID_PASSWORD=(str, None),
    SLUG_MAX_LENGTH=(int, 72),
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# TODO: update to os.environ['ALLOWED_HOSTS'].split()
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'bootstrapform',
    'openach',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

# This is using the pre-Django 1.10 middleware API. We'll need to update once the 3rd-party libraries are updated
# to use the new API: https://docs.djangoproject.com/en/1.10/topics/http/middleware

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'csp.middleware.CSPMiddleware',
    # MinifyHTMLMiddleware needs to be after all middleware that may modify the HTML
    'pipeline.middleware.MinifyHTMLMiddleware',
    # Rollbar middleware needs to be last
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]

ROOT_URLCONF = 'openintel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            # Template debugging is required for coverage testing
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'openintel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT')
SECURE_BROWSER_XSS_FILTER = env('SECURE_BROWSER_XSS_FILTER')
SECURE_CONTENT_TYPE_NOSNIFF = env('SECURE_CONTENT_TYPE_NOSNIFF')
SECURE_HSTS_INCLUDE_SUBDOMAINS = env('SECURE_HSTS_INCLUDE_SUBDOMAINS')
SECURE_HSTS_SECONDS = env('SECURE_HSTS_SECONDS')

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# https://docs.djangoproject.com/en/1.10/ref/contrib/sites/
SITE_ID = 1

# Update database configuration with $DATABASE_URL.
# TODO: migrate db config to use environ?
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Logging configuration
# cf. https://chrxr.com/django-error-logging-configuration-heroku/
# cf. https://stackoverflow.com/questions/18920428/django-logging-on-heroku
# TODO: make django/gunicorn log formatting consistent
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': env('DJANGO_LOG_LEVEL'),
        },
        'openach': {
            'handlers': ['console'],
            'level': env('APP_LOG_LEVEL'),
        }
    },
}

# Email Options using sendgrid-django
if env('SENDGRID_USERNAME') and env('SENDGRID_PASSWORD'):  # pragma: no cover
    EMAIL_BACKEND = "sgbackend.SendGridBackend"
    # NOTE: django library uses _USER while Heroku uses _USERNAME
    SENDGRID_USER = env('SENDGRID_USERNAME')
    SENDGRID_PASSWORD = env('SENDGRID_PASSWORD')
else:
    logger.warning("Email not configured: SENDGRID_USER, SENDGRID_PASSWORD")

# Authentication Options:
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = env('ACCOUNT_EMAIL_REQUIRED')
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
# https://stackoverflow.com/questions/22700041/django-allauth-sends-verification-emails-from-webmasterservername
DEFAULT_FROM_EMAIL = "info@opensynthesis.org"

# Challenge/Response for Let's Encrypt. In the future, we may want to support challenge/response for multiple domains.
CERTBOT_PUBLIC_KEY = env('CERTBOT_PUBLIC_KEY')
CERTBOT_SECRET_KEY = env('CERTBOT_SECRET_KEY')

# Rollbar Error tracking: https://rollbar.com/docs/notifier/pyrollbar/#django
# Rollbar endpoint via 'endpoint' configuration is not working. For now just use the default.
ROLLBAR = {
    'enabled': not TESTING,
    'access_token': env('ROLLBAR_ACCESS_TOKEN'),
    'environment': 'development' if DEBUG else 'production',
    'root': PROJECT_ROOT,
    # TODO: read branch and version information from git, potentially using gitpython
    'branch': 'master',
    # 'code_version': git sha
}

# Content Security Policy (CSP) Header configuration
# https://django-csp.readthedocs.io/en/latest/configuration.html
# http://www.html5rocks.com/en/tutorials/security/content-security-policy/

CSP_DEFAULT_SRC = ["'self'"]
CSP_SCRIPT_SRC = [
    "'self'", 'https://maxcdn.bootstrapcdn.com',
    'https://code.jquery.com', 'https://cdnjs.cloudflare.com'
]
CSP_STYLE_SRC = ["'self'", 'https://maxcdn.bootstrapcdn.com', 'https://cdnjs.cloudflare.com']
CSP_FONT_SRC = ["'self'", 'https://maxcdn.bootstrapcdn.com']

# SEO Configuration
SLUG_MAX_LENGTH = env('SLUG_MAX_LENGTH')

# django-pipeline configuration for static files
# https://django-pipeline.readthedocs.io/en/latest/configuration.html
# We're currently just using it for its HTML minification middleware
PIPELINE = {
    'PIPELINE_ENABLED': not DEBUG,
}
