import os.path
from pathlib import Path
import logging
from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^-gcdl5u%c41=tz)$-k&if@)ofdmqnolz_5*$^x&%+8%0i-4!!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ["hopepsbank.com", "www.hopepsbank.com", "hopepsbank.com", "127.0.0.1", "localhost", "89.38.135.41", "hopemail.tm-dev.xyz"]


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'service.apps.ServiceConfig',

    # App config
    'rest_framework',
    "corsheaders",
    "i_gree.apps.IGreeConfig"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hopeps_bank_email_backend.urls'

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

WSGI_APPLICATION = 'hopeps_bank_email_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': config('DATABASE_ENGINE', None),
        'NAME': config('DATABASE_NAME', None),
        'USER': config('DATABASE_USER', None),
        'PASSWORD': config('DATABASE_PASSWORD', None),
        'HOST': config('DATABASE_HOST', None),
        'PORT': config('DATABASE_PORT', None),
    }
}

# screen shot of the detail and header.
# showing that we are done with the implementation and we need to move production.

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

logging.basicConfig(
    filename='EmailService.log',
    filemode='a',
    level=logging.DEBUG,
    format='[{asctime}] {levelname} {module} {thread:d} - {message}',
    datefmt='%d-%m-%Y %H:%M:%S',
    style='{',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {module} {thread:d} - {message}',
            'style': '{',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'EmailService.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:8080",
    "https://www.hopepsbank.com",
    "http://localhost"
]

CORS_ALLOW_ALL_ORIGINS = True

API_KEY = config("API_KEY", None)
EMAIL_TO = config("EMAIL_TO", None)
EMAIL_FROM = config("EMAIL_FROM", None)


# NIBSS SETTINGS
CLIENT_ID = config("CLIENT_ID", None)
MY_CALL_BACK = config("MY_CALL_BACK", None)
IDP_INITIATOR_URL = config("IDP_INITIATOR_URL", None)
CLIENT_SECRET = config("CLIENT_SECRET", None)

GET_ACCESS_TOKEN_URL = config("GET_ACCESS_TOKEN_URL", None)
GET_BVN_DETAIL_URL = config("GET_BVN_DETAIL_URL", None)
FRONTEND_REDIRECT_URL = config("FRONTEND_REDIRECT_URL", None)
