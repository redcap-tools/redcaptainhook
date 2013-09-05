"""Development settings and globals."""


from os.path import join, normpath

from common import *


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_var('RCH_DEV_DB_NAME'),
        'USER': get_env_var('RCH_DEV_DB_USER'),
        'PASSWORD': get_env_var('RCH_DEV_DB_PASS'),
        'HOST': get_env_var('RCH_DEV_DB_HOST'),
        'PORT': get_env_var('RCH_DEV_DB_PORT'),
    }
}
########## END DATABASE CONFIGURATION


########## RQ CONFIG
RQ_QUEUES = {
    'switchboard': {
        'URL': get_env_var('RCH_DEV_BROKER_URL'),
        'DB': 0
    },
    'default': {
        'URL': get_env_var('RCH_DEV_BROKER_URL'),
        'DB': 0
    }

}
########## END RQ CONFIG


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION


########## CELERY CONFIGURATION
# See: http://docs.celeryq.org/en/latest/configuration.html#celery-always-eager
# CELERY_ALWAYS_EAGER = True

# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-eager-propagates-exceptions
# CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# See: http://docs.celeryproject.org/en/latest/configuration.html#redis-backend-settings
# BROKER_URL = get_env_var('RCH_BROKER_URL')
########## END CELERY CONFIGURATION


########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    'debug_toolbar',

)

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False, }

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
########## END TOOLBAR CONFIGURATION
