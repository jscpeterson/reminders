from .base import *
from celery.schedules import crontab

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS += [os.environ.get('SERVER_IP'), os.environ.get('SERVER_NAME')]

BASE_URL = 'http://' + os.environ.get('SERVER_NAME')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
    }
}

#INSTALLED_APPS += [
#    'debug_toolbar',
#]

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
        'schedule': crontab(minute=0, hour=8, day_of_week='mon,tue,wed,thu,fri'),
    }
}

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# LDAP settings
import ldap
from django_auth_ldap.config import LDAPSearch, NestedActiveDirectoryGroupType
# Server information
LDAP_SERVER_FQDN = os.getenv('LDAP_SERVER_FQDN')
AUTH_LDAP_SERVER_URI = 'ldap://' + LDAP_SERVER_FQDN
# Binding information
AUTH_LDAP_BIND_DN = os.getenv('AUTH_LDAP_BIND_DN')
AUTH_LDAP_BIND_PASSWORD = os.getenv('AUTH_LDAP_BIND_PASSWORD')
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_DEBUG_LEVEL: 1,
    ldap.OPT_REFERRALS: 0,
}
# User and group search objects and types
LDAP_SEARCH_BASE_DN = os.getenv('LDAP_SEARCH_BASE_DN')
LDAP_SEARCH_FILTER_STRING = os.getenv('LDAP_SEARCH_FILTER_STRING')
LDAP_GROUP_SEARCH_BASE_DN = os.getenv('LDAP_GROUP_SEARCH_BASE_DN')
LDAP_GROUP_SEARCH_FILTER_STRING = os.getenv('LDAP_GROUP_SEARCH_FILTER_STRING')
AUTH_LDAP_USER_SEARCH = LDAPSearch(LDAP_SEARCH_BASE_DN,
                                   ldap.SCOPE_SUBTREE,
                                   LDAP_SEARCH_FILTER_STRING)
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(LDAP_GROUP_SEARCH_BASE_DN,
                                    ldap.SCOPE_SUBTREE,
                                    LDAP_GROUP_SEARCH_FILTER_STRING)
AUTH_LDAP_GROUP_TYPE = NestedActiveDirectoryGroupType()
# Cache settings
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 300
# Information that is extracted from ldap to django user database
AUTH_LDAP_USER_ATTR_MAP = {'username': 'sAMAccountName',
                           'first_name': 'givenName',
                           'last_name': 'sn',
                           'email': 'mail',
                           }
AUTH_LDAP_FIND_GROUP_PERMS = True

# TODO Add production whitelist

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
