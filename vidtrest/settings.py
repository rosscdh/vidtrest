# -*- coding: utf-8 -*-
"""
"""
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = '/'

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
    'vidtrest.apps.public',
    'vidtrest.apps.categories',
    'vidtrest.apps.vid',
]

HELPER_APPS = [
    'crispy_forms',
    'django_extensions',
    'django_select2',
    'taggit',
    'storages',
    'pipeline',
    'haystack',
    'django_rq',
    'spurl',
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
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
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

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vidtrest',
        'HOST': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'twjRbhYbgn',
        'PORT': '5432',
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

LANGUAGE_CODE = 'de'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join('/', 'static')

#MEDIA_URL = '/m/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join('/', 'media')

#
# App Settings
#


# Queue Settings
RQ_QUEUES = {
    'default': {
        'HOST': 'redis',
        'PORT': 6379,
        'DB': 0,
    },
    'high': {
        'HOST': 'redis',
        'PORT': 6379,
        'DB': 0,
    },
    'low': {
        'HOST': 'redis',
        'PORT': 6379,
        'DB': 0,
    }
}

# AWS keys
AWS_USE = False
AWS_SECRET_ACCESS_KEY = ''
AWS_ACCESS_KEY_ID = ''
AWS_STORAGE_BUCKET_NAME = ''

CRISPY_TEMPLATE_PACK = 'bootstrap3'

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
    'freewall#1.0.6',
    'clipboard#1.5.10',
    'owl.carousel#2.1.1',
)

PIPELINE = {
    'PIPELINE_ENABLED': False,
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

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}

#
# Cant use this due to model postsave dependency. Maybe switch to using the meta as the observed model?
#
#HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

#
# Load the environment specific settings
#


def _load_settings(project_environment):
    settings_path = os.getenv('DJANGO_LOCAL_SETTINGS', os.path.join('/config', os.getenv('DJANGO_ENV', 'development') ,'local_settings.py'))
    return open(settings_path).read()

exec(_load_settings(PROJECT_ENVIRONMENT))


#
# Check for test settings
#
for test_app in ['testserver', 'test', 'jenkins']:
    if test_app in sys.argv[1:2]:
        # Hardcode to test
        PROJECT_ENVIRONMENT = 'test'
        exec(_load_settings(PROJECT_ENVIRONMENT))
