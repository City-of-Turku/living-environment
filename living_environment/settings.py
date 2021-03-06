import os

import environ
import raven
from django.utils.translation import ugettext_lazy as _

checkout_dir = environ.Path(__file__) - 2
assert os.path.exists(checkout_dir('manage.py'))

parent_dir = checkout_dir.path('..')
if os.path.isdir(parent_dir('etc')):
    env_file = parent_dir('etc/env')
    default_var_root = parent_dir('var')
else:
    env_file = checkout_dir('.env')
    default_var_root = checkout_dir('var')

env = environ.Env(
    DEBUG=(bool, True),
    TIER=(str, 'dev'),  # one of: prod, qa, stage, test, dev
    SECRET_KEY=(str, ''),
    VAR_ROOT=(str, default_var_root),
    ALLOWED_HOSTS=(list, []),
    DATABASE_URL=(str, 'postgres://living_environment:living_environment@localhost/living_environment'),
    CACHE_URL=(str, 'locmemcache://'),
    EMAIL_URL=(str, 'consolemail://'),
    SENTRY_DSN=(str, ''),
    CORS_ORIGIN_WHITELIST=(list, []),
    FEEDBACK_SYSTEM_URL=(str, ''),
    FEEDBACK_SERVICE_CODE=(str, ''),
    FEEDBACK_API_KEY=(str, ''),
    FRONTEND_APP_URL=(str, ''),
    STATIC_URL=(str, '/static/'),
    MEDIA_URL=(str, '/media/'),
)
if os.path.exists(env_file):
    env.read_env(env_file)

try:
    version = raven.fetch_git_sha(checkout_dir())
except Exception:
    version = None

DEBUG = env.bool('DEBUG')
TIER = env.str('TIER')
SECRET_KEY = env.str('SECRET_KEY')
if DEBUG and not SECRET_KEY:
    SECRET_KEY = 'xxx'

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

DATABASES = {'default': env.db()}
CACHES = {'default': env.cache()}
vars().update(env.email_url())  # EMAIL_BACKEND etc.
RAVEN_CONFIG = {'dsn': env.str('SENTRY_DSN'), 'release': version}

var_root = env.path('VAR_ROOT')
MEDIA_ROOT = var_root('media')
MEDIA_URL = '{}/'.format(env.str('MEDIA_URL').rstrip('/'))
STATIC_ROOT = var_root('static')
STATIC_URL = '{}/'.format(env.str('STATIC_URL').rstrip('/'))

ROOT_URLCONF = 'living_environment.urls'
WSGI_APPLICATION = 'living_environment.wsgi.application'

LANGUAGE_CODE = 'fi'
TIME_ZONE = 'Europe/Helsinki'
USE_I18N = True
USE_L10N = True
USE_TZ = True
CKEDITOR_UPLOAD_PATH = "uploads/"
STATICFILES_DIRS = [checkout_dir('static')]
LEAFLET_CONFIG = {
    'TILES': [],
    'DEFAULT_CENTER': [60.451389, 22.266667],
    'DEFAULT_ZOOM': 12,
}


INSTALLED_APPS = [
    'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    'assignments',
    'leaflet',
    'djgeojson',
    'django_extensions',
    'rest_framework',
    'rest_framework_extensions',
    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',
    'polymorphic',
    'sortedm2m',
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

LANGUAGES = [
  ('fi', _('Finnish')),
  ('en', _('English')),
]

LOCALE_PATHS = (
    os.path.join(checkout_dir(), "locale"),
)

# Setup Django Debug Toolbar
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    INTERNAL_IPS = ['127.0.0.1', 'localhost']
    MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [checkout_dir('templates')],
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

# CORS
CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST')

# VOLUNTARY TASKS
FEEDBACK_SYSTEM_URL = env.str('FEEDBACK_SYSTEM_URL')
FEEDBACK_SERVICE_CODE = env.str('FEEDBACK_SERVICE_CODE')
FEEDBACK_API_KEY = env.str('FEEDBACK_API_KEY')

FRONTEND_APP_URL = env.str('FRONTEND_APP_URL').rstrip('/')

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

# Enable Browsable API only in debug mode
if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')
