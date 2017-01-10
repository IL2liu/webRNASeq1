"""
Django settings for mimir project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import pyexcel.ext.xlsx  # This is required for tmp file handlers.

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w9pir37-hec5g45gy7kw&uo_v8+v5$1609f$0#)dxgoo7cne!#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django_cassandra_engine',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_nose',
    'reporting',
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = 'mimir.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./templates'],
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

WSGI_APPLICATION = 'mimir.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

CQLENG_ALLOW_SCHEMA_MANAGEMENT = 'CQLENG_ALLOW_SCHEMA_MANAGEMENT'

if not os.getenv(CQLENG_ALLOW_SCHEMA_MANAGEMENT):
    os.environ[CQLENG_ALLOW_SCHEMA_MANAGEMENT] = '1'

DATABASES = {
    'default': {
        'ENGINE': 'django_cassandra_engine',
        'NAME': 'db',
        'HOST': ','.join([
            'ec2-54-152-155-172.compute-1.amazonaws.com',
            'ec2-52-91-53-23.compute-1.amazonaws.com',
        ]),
        'OPTIONS': {
            'replication': {
                'strategy_class': 'NetworkTopologyStrategy',
                'us-east': 2,
            },
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = '/www/mimir/static'

STATICFILES_DIRS = [
     os.path.join(BASE_DIR, './static'),
]

STATIC_URL = '/static/'


# File upload settings

FILE_UPLOAD_TEMP_DIR = './tmp/'

FILE_UPLOAD_HANDLERS = [
    'django_excel.ExcelMemoryFileUploadHandler',
    'django_excel.TemporaryExcelFileUploadHandler',
]
