# -*- coding: utf-8 -*-
"""
"""
import os
import sys
from pathlib import Path
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_ENVIRONMENT = DJANGO_ENV = os.getenv('DJANGO_ENV', 'development')
TRUTHY = ("True", "true", "y", "1",)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'swaonvcrhy4-yr6$tmfu(hht+c%14!#ut3by7m554ncw12iqo@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

PROJECT_APPS = [
    'vidtrest.apps.public',
    'vidtrest.apps.categories',
    'vidtrest.apps.vid',
]

HELPER_APPS = [
    'crispy_forms',
    'crispy_bootstrap3',
    'django_extensions',
    'django_select2',
    'taggit',
    'storages',
    'compressor',
    'haystack',
    'django_rq',
    'spurl',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + HELPER_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join('./', 'static')

#MEDIA_URL = '/m/'
MEDIA_URL = 'http://localhost:8002/assets/'
MEDIA_ROOT = os.path.join('./', 'media')

#
# App Settings
#


# Queue Settings
RQ_QUEUES = {
    'default': {
        'HOST': 'redis',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 1800,
    },
    'high': {
        'HOST': 'redis',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 1800,
    },
    'low': {
        'HOST': 'redis',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 1800,
    }
}

# AWS keys
AWS_USE = os.getenv("AWS_USE", "False") in TRUTHY
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")

PERFORM_JOBS_SYNCHRONOUSLY = False

FILE_UPLOAD_PERMISSIONS = 0o755
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

CRISPY_TEMPLATE_PACK = 'bootstrap3'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
# STORAGES = {"default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"}}

STATICFILES_DIRS = (
)

# BOWER_INSTALLED_APPS = (
#     'jquery-thumb-preview#0.0.1',
#     'jquery#1.11.0',
#     'plyr#1.5.21',
#     'freewall#1.0.6',
#     'clipboard#1.5.10',
#     'owl.carousel#2.1.1',
# )

HAYSTACK_CONNECTIONS = {
    # 'default': {
    #     'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
    #     'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    # },
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://elasticsearch:9200/',
        'INDEX_NAME': 'vidtrest',
    },
}

#
# Cant use this due to model postsave dependency. Maybe switch to using the meta as the observed model?
#
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

#
# Load the environment specific settings
#
# def _load_settings(project_environment):
#     settings_path = os.getenv('DJANGO_LOCAL_SETTINGS', os.path.join('/config', os.getenv('DJANGO_ENV', 'development') ,'local_settings.py'))
#     return open(settings_path).read()
# exec(_load_settings(PROJECT_ENVIRONMENT))

#
# Check for test settings
#
# for test_app in ['testserver', 'test', 'jenkins']:
#     if test_app in sys.argv[1:2]:
#         # Hardcode to test
#         PROJECT_ENVIRONMENT = 'test'
#         exec(_load_settings(PROJECT_ENVIRONMENT))


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(process)-5d %(thread)d %(name)-50s %(levelname)-8s %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s] %(name)s %(levelname)s %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local7',
            'address': '/dev/log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        # root logger
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'disabled': False
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
