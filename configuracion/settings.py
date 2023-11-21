from pathlib import Path
import os
import configuracion.db as db

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*h=)&1hw^d#n&ti5bs$kvrybs&2s^q!tcn9xv7wr9%m%v3=r75'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['192.168.250.6', '192.168.250.1']
ALLOWED_HOSTS = []

DJANGO_APPS =[
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

PROJECT_APPS = [
    'core.login',
    'core.user',
    'core.security',
    'core.group',
    'core.erp',
    'core.solicitudes',
    'core.inicio',
    'core.reportes',
    'core.audit_log',
    'core.chat',
    'core.notificaciones',
    'core.aprobaciones',
    'core.ui_customizer',
]

THIRD_PARTY_APPS = [
    'widget_tweaks',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'querycount.middleware.QueryCountMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crum.CurrentRequestUserMiddleware',    
]

ROOT_URLCONF = 'configuracion.urls'

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
                'core.ui_customizer.context_processors.global_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'configuracion.wsgi.application'
ASGI_APPLICATION = 'configuracion.asgi.application'
# LEARN CHANNELS
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}
DATABASES = db.SQLITE

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

LANGUAGE_CODE = 'es-eu'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT  = os.path.join(BASE_DIR, 'staticfiles/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

EMAIL_BACKEND= 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'josmer5772@gmail.com'
EMAIL_HOST_PASSWORD = 'ocvpiggdkknibjus'
EMAIL_PORT = 587

AUTH_USER_MODEL= 'user.User'

# CRON_CLASSES = [
#     'myapp.cron.BackupJob',
# ]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# AUTH_GROUP_MODEL= 'group.Group'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MEDIA_URL = '/media/'

LOGIN_REDIRECT_URL = 'index_app:Index'

LOGOUT_REDIRECT_URL = '/'

LOGIN_URL = '/'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:8000',
#     }
# }