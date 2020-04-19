import os
import sys

from django.contrib.messages import constants as message_constants

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APPS_DIR = os.path.join(BASE_DIR, 'apps')
sys.path.insert(0, APPS_DIR)

# Debugging.
# ------------------------------------------------------------------------------

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Security.
# ------------------------------------------------------------------------------

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nmhzmtcg4124w@8b24+f=q+k$_j)onr2o(c&-t$$lqe!=xm^=9'

ALLOWED_HOSTS = ['127.0.0.1']

# Urls.
# ------------------------------------------------------------------------------

ROOT_URLCONF = 'root.urls'

APPEND_SLASH = True

# Application settings.
# ------------------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts.apps.AccountsConfig',
    'profiles.apps.ProfilesConfig',
    'tickets',
    'quiz',
    'forum',
]

# HTTP.
# ------------------------------------------------------------------------------

# Django’s built-in servers (e.g. runserver) will use this.
WSGI_APPLICATION = 'root.wsgi.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # For sessions
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Template engine settings.
# ------------------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Look for templates in these directories.
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(APPS_DIR, 'templates')],
        # Look for templates inside installed applications.
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'accounts.context_processors.url_names',
                'profiles.context_processors.url_names',
            ],
        },
    },
]

# Database settings.
# ------------------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation.
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        # Check if password meets a minimum length.
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Check if password occurs in a list of common passwords.
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Check if password isn't entirely numeric.
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        # Check if password has at least one digit and one special character.
        'NAME': 'accounts.validators.CustomPasswordValidator',
    }
]

# Internationalization.
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'

# Server timezone.
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

# Display numbers and dates using the format of the current locale.
USE_L10N = True

# Datetimes are timezone-aware.
USE_TZ = True

# Static files.
# ------------------------------------------------------------------------------

# URL to use when referring to static files.
STATIC_URL = '/static/'

# Additional locations of static files directories.
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files.
# ------------------------------------------------------------------------------

# Absolute path to the directory that will hold USER-UPLOADED files.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/media/'

# Authentication.
# ------------------------------------------------------------------------------

# The model to use to represent a User.
AUTH_USER_MODEL = 'auth.User'

# The named URL pattern where requests are redirected for registration.
REGISTER_URL = 'signup'

# The named URL pattern where requests are redirected for login.
LOGIN_URL = 'signin'

# The named URL pattern where requests are redirected for logout.
LOGOUT_URL = 'signout'

# The named URL pattern where requests are redirected after login.
LOGIN_REDIRECT_URL = 'profile-redirect'

# The URL or named URL pattern where requests are redirected after logout.
LOGOUT_REDIRECT_URL = 'index'

# Messages.
# ------------------------------------------------------------------------------

MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'error',
}

# Session.
# ------------------------------------------------------------------------------

SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
