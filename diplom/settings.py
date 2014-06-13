# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from diplom.suit_conf import SUIT_CONFIG

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k#@#wmsxa)@^0u61em8yk6779@5knkt@!b&*g$ywh%ylow6v+n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

production = False

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'dis.chita@gmail.com'
EMAIL_HOST_PASSWORD = 'dis.chita123456'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

TEMPLATE_DIRS = (
    'templates/',
)
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'suit',
    'suit_redactor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'flatpages',
    'south',
    'user',
    'forms_custom',
    'reports',
)

if production:
    INSTALLED_APPS += ('gunicorn',)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'flatpages.middleware.FlatpageFallbackMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'diplom.urls'

WSGI_APPLICATION = 'diplom.wsgi.application'

AUTH_USER_MODEL = 'user.MyUser'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if production:
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'diplom_db',
            'USER': 'django',
            'PASSWORD': 'pass',
            'HOST': 'localhost',
            'PORT': '',
        },
    }
else:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATICFILES_DIRS = (
    "D:/django/first/diplom/static/",
)

STATIC_URL = '/static/'

STATIC_ROOT = 'static'

LOGGING = {
    'version': 1,
}
