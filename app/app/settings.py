"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys
import django_heroku
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_FOLDER = os.path.join(BASE_DIR, 'ml_models/')
OUTPUT_FILE = os.path.join(ML_FOLDER, 'ml_out.csv')
INPUT_FILE = os.path.join(ML_FOLDER, 'ml_input.csv')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'v8sk33sy82!uw3ty=!jjv5vp7=s2phrzw(m(hrn^f7e_#1h2al')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True
if os.environ.get('DEBUG') == 'False':
    DEBUG = False
# DEBUG = bool(os.environ.get('DEBUG', False))
# DEBUG = os.environ.get('DEBUG') == 'TRUE'


# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'server.apps.ServerConfig',
    'widget_tweaks',
    'rest_framework',
    'django_filters',
    'social_django',
    'import_export',
]

MIDDLEWARE = [
    'djdev_panel.middleware.DebugMiddleware',  # <--- this guy
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'applicationinsights.django.ApplicationInsightsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'server/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
            'libraries': {
                'analytics': 'server.templatetags.analytics',
            },
        },
    },
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'server/static'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

WSGI_APPLICATION = 'app.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.azuread_tenant.AzureADTenantOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_GITHUB_KEY = os.getenv('OAUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.getenv('OAUTH_GITHUB_SECRET')

SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY = os.getenv('OAUTH_AAD_KEY')
SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET = os.getenv('OAUTH_AAD_SECRET')
SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID = os.getenv('OAUTH_AAD_TENANT')

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/users/%s/" % u.id,
}

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'posgres_local': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'doccano',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': 5432,
        'CONN_MAX_AGE': 60
    },

    'posgres': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'doccano',
        'USER': 'doccano',
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': 'doccano.pg.research.gongio.net',
        'PORT': 5432,
        'CONN_MAX_AGE': 60
    },

    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}
# DATABASES['default'] = DATABASES['posgres']
DATABASES['default'] = DATABASES['posgres_local']

if "test" in sys.argv:
    DATABASES = {    
         'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'doccano',
            'USER': 'postgres',
            'PASSWORD': 'admin',
            'HOST': 'localhost',
            'PORT': 5432,
            'CONN_MAX_AGE': 60
        }  
    }

if 'TRAVIS' in os.environ:
    DATABASES = {    
         'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'doccano',
            'USER': 'postgres',
            'PASSWORD': 'admin',
            'HOST': 'localhost',
            'PORT': 5433,
            'CONN_MAX_AGE': 60
        }  
    }

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'SEARCH_PARAM': 'q',
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/projects/'
LOGOUT_REDIRECT_URL = '/'

# Change 'default' database configuration with $DATABASE_URL.
DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
# ALLOWED_HOSTS = ['*']

# Size of the batch for creating documents
# on the import phase
IMPORT_BATCH_SIZE = 500

GOOGLE_TRACKING_ID = os.getenv('GOOGLE_TRACKING_ID', 'UA-123456789-9')

AZURE_APPINSIGHTS_IKEY = os.getenv('AZURE_APPINSIGHTS_IKEY')
APPLICATION_INSIGHTS = {
    'ikey': AZURE_APPINSIGHTS_IKEY if AZURE_APPINSIGHTS_IKEY else None,
}

django_heroku.settings(locals(), test_runner=False)
