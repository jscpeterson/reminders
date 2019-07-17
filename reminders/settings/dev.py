from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '**17fu_6c506av2h)+f)m$4hl=o)mkbtys!@k)(ng6hnl(cyw0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

BASE_URL = os.environ.get('BASE_URL')

INSTALLED_APPS += [
    'debug_toolbar',
]

# MIDDLEWARE += [
#     'debug_toolbar.middleware.DebugToolbarMiddleware'
# ]

INTERNAL_IPS = [
    '127.0.0.1',
]

# Celery Settings
# https://docs.celeryproject.org/en/latest/userguide/configuration.html

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_BEAT_SCHEDULE = {
    'check_all_deadlines': {
        'task': 'remind.tasks.check_all_deadlines',
        'schedule': 10,
    }
}

# CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    "http://127.0.0.1",
    "http://localhost",
)

CSRF_TRUSTED_ORIGINS = (
    "127.0.0.1",
    "localhost",
)
