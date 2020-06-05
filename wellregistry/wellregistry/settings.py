"""
Django settings for wellregistry project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import ast
import os
import sys

from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'DEBUG' in os.environ

allowed_hosts = os.getenv('ALLOWED_HOSTS', '[]')

try:
    ALLOWED_HOSTS = ast.literal_eval(allowed_hosts)
    if not isinstance(ALLOWED_HOSTS, list):
        raise TypeError('ALLOWED_HOSTS must be a list.')
except ValueError:
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'postgres',
    'registry',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django'
]

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'allow_cidr.middleware.AllowCIDRMiddleware'
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.keycloak.KeycloakOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# custom
LOGIN_URL = '/accounts/login/'
LOGOUT_REDIRECT_URL = ''
LOGIN_REDIRECT_URL = '/profile/'

# python-social-auth settings - See the keycloak.py backend in social-core for guidance on setting these.
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_KEYCLOAK_KEY = os.getenv('SOCIAL_AUTH_KEYCLOAK_KEY', '')
SOCIAL_AUTH_KEYCLOAK_SECRET = os.getenv('SOCIAL_AUTH_KEYCLOAK_SECRET', '')
SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY = os.getenv('SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY', '')
SOCIAL_AUTH_KEYCLOAK_AUTHORIZATION_URL = os.getenv('SOCIAL_AUTH_KEYCLOAK_AUTHORIZATION_URL')
SOCIAL_AUTH_KEYCLOAK_ACCESS_TOKEN_URL = os.getenv('SOCIAL_AUTH_KEYCLOAK_ACCESS_TOKEN_URL')

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['email']

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'wellregistry.custom_social_pipeline.change_usgs_user_to_staff',
    'wellregistry.custom_social_pipeline.set_superuser_permission',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Custom setting which is a list of user's who are granted superuser status
SOCIAL_AUTH_DJANGO_SUPERUSERS = os.getenv('SOCIAL_AUTH_DJANGO_SUPERUSERS', [])

ROOT_URLCONF = 'wellregistry.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect'
            ],
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters':{
        'basic': {
            'format': '%(asctime)s [%(levelname)-8s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'basic'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'INFO'
    }
}

# use the AllowCIDRMiddleware to support a CIDR range to ensure that an AWS health check can work
CIDR_RANGES = os.getenv('CIDR_RANGES', None)
if CIDR_RANGES is not None:
    CIDR_RANGES = ast.literal_eval(CIDR_RANGES)
    ALLOWED_CIDR_NETS = CIDR_RANGES

WSGI_APPLICATION = 'wellregistry.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
ENVIRONMENT = {
    'DATABASE_NAME': os.getenv('DATABASE_NAME', 'postgres'),
    'DATABASE_HOST': os.getenv('DATABASE_HOST'),
    'DATABASE_PORT': os.getenv('DATABASE_PORT', default='5432'),
    'DATABASE_USERNAME': os.getenv('DATABASE_USERNAME', 'postgres'),  # not necessary the same name
    'DATABASE_PASSWORD': os.getenv('DATABASE_PASSWORD'),

    'APP_DATABASE_NAME': os.getenv('APP_DATABASE_NAME'),
    'APP_DB_OWNER_USERNAME': os.getenv('APP_DB_OWNER_USERNAME'),
    'APP_DB_OWNER_PASSWORD': os.getenv('APP_DB_OWNER_PASSWORD'),
}

# short alias
env = ENVIRONMENT

if 'test' in sys.argv:
    DATABASES = {
        'default': {  # used for integration tests
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    }
else:
    DATABASES = {
        'default': {# used by the migrations and backend code.
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env['APP_DATABASE_NAME'],
            'HOST': env['DATABASE_HOST'],
            'PORT': env['DATABASE_PORT'],
            'USER': env['APP_DB_OWNER_USERNAME'],
            'PASSWORD': env['APP_DB_OWNER_PASSWORD'],
        }
    }
    if 'migration' in sys.argv:
        DATABASES['postgres']: {  # only needed for Django migration 0001_create_db_users
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env['DATABASE_NAME'],
            'HOST': env['DATABASE_HOST'],
            'PORT': env['DATABASE_PORT'],
            'USER': env['DATABASE_USERNAME'],
            'PASSWORD': env['DATABASE_PASSWORD'],
        }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
