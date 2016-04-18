# -*- coding: utf-8 -*-
"""
"""
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ENVIRONMENT = DJANGO_ENV = os.getenv('DJANGO_ENV', 'development')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'swaonvcrhy4-yr6$tmfu(hht+c%14!#ut3by7m554ncw12iqo@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'vidtrest.apps.categories',
    'vidtrest.apps.vid',
]

HELPER_APPS = [
    'django_extensions',
    'django_select2',
    'taggit',
    'storages',
    'pipeline',
    'django_rq',
    'djangobower',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + HELPER_APPS


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vidtrest.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'vidtrest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# STATIC_URL = '/static/'
STATIC_URL = 'http://192.168.50.5/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# MEDIA_URL = '/m/'
MEDIA_URL = 'http://192.168.50.5/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#
# App Settings
#


# Queue Settings
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    },
    'high': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    },
    'low': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    }
}

# AWS keys
AWS_USE = False
AWS_SECRET_ACCESS_KEY = ''
AWS_ACCESS_KEY_ID = ''
AWS_STORAGE_BUCKET_NAME = ''


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
    'pipeline.finders.CachedFileFinder',
    'pipeline.finders.PipelineFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

BOWER_COMPONENTS_ROOT = BASE_DIR

STATICFILES_DIRS = (
    os.path.join(BOWER_COMPONENTS_ROOT, 'bower_components'),
)

BOWER_INSTALLED_APPS = (
    'jquery-thumb-preview#0.0.1',
    'jquery#1.11.0',
    'plyr#1.5.21',
    'waterfall#1.0.3',
    'clipboard#1.5.10',
)

PIPELINE = {
    'PIPELINE_ENABLED': True,
    'CSS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.uglifyjs.UglifyJSCompressor',
    'COMPILERS': ('pipeline.compilers.sass.SASSCompiler',),
    'STYLESHEETS': {
    },
    'JAVASCRIPT': {
        'thumbpreview': {
            'source_filenames': (
                'jquery/src/jquery.js',
                'jQuery-Thumb-Preview/jquery.thumb.preview.js',
            ),
            'output_filename': 'dist/thumbpreview.js',
        }
    }
}

#
# Load the environment specific settings
#


def _load_settings(project_environment):
    settings_path = os.path.join(BASE_DIR, '../', 'config/environments/{DJANGO_ENV}/vidtrest/local_settings.py'.format(DJANGO_ENV=project_environment))
    return open(settings_path)

try:
    exec(_load_settings(PROJECT_ENVIRONMENT))
except Exception as e:
    print('An exception trying to import env specific settings occrrred: %s' % e)


#
# Load specific local_settings.py settings in case we want to override something for an env
#
try:
    from .local_settings import *
except ImportError:
    # no local_settings.py found
    pass

#
# Check for test settings
#
for test_app in ['testserver', 'test', 'jenkins']:
    if test_app in sys.argv[1:2]:
        # Hardcode to test
        PROJECT_ENVIRONMENT = 'test'
        exec(_load_settings(PROJECT_ENVIRONMENT))
