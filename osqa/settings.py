# coding:utf-8

import os
import sys


def rel(*x):
    """
    Returns the absolute path of *x from relatively the project root
    """
    return os.path.normpath(os.path.join(os.path.dirname(__file__), '..', *x))


def install_app(app, debug_only=None, middlewares=[]):
    """
    Safely adds application into INSTALLED_APPS
    """
    try:
        if debug_only is not None:
            if DEBUG != debug_only:
                return
        __import__(app)
    except ImportError:
        return

    INSTALLED_APPS.append(app)
    MIDDLEWARE_CLASSES.extend(middlewares)



SITE_ID = 1

SECRET_KEY = '$oo^&_m&qwbib=(_4m_n*zn-d=g#s0he5fx9xonnym#8p6yigm'

CACHE_MAX_KEY_LENGTH = 235

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'forum.middleware.django_cookies.CookiePreHandlerMiddleware',
    'forum.middleware.extended_user.ExtendedUser',
    'forum.middleware.anon_user.ConnectToSessionMessagesMiddleware',
    'forum.middleware.request_utils.RequestUtils',
    'forum.middleware.cancel.CancelActionMiddleware',
    'forum.middleware.admin_messages.AdminMessagesMiddleware',
    'forum.middleware.custom_pages.CustomPagesFallbackMiddleware',
    'forum.middleware.django_cookies.CookiePostHandlerMiddleware',
    'django.middleware.transaction.TransactionMiddleware',

    ]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'forum.context.application_settings',
    'forum.user_messages.context_processors.user_messages',
]

ROOT_URLCONF = 'osqa.urls'
APPEND_SLASH = True

TEMPLATE_DIRS = (
    rel('forum', 'skins'),
)


STATIC_URL = '/static/'
STATICFILES_DIRS = (
    rel('forum/skins/common/static'),
    rel('forum/skins/default/static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)




MEDIA_URL = '/media/'

FILE_UPLOAD_TEMP_DIR = rel('tmp')

FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

ALLOW_FILE_TYPES = ('.jpg', '.jpeg', '.gif', '.bmp', '.png', '.tiff')
ALLOW_MAX_FILE_SIZE = 1024 * 1024

# User settings
from settings_local import *

if DEBUG:
    TEMPLATE_LOADERS = [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'forum.modules.template_loader.ModulesTemplateLoader',
        'forum.skins.SkinsTemplateLoader',
    ]
else:
    TEMPLATE_LOADERS = [
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
            'forum.modules.template_loader.ModulesTemplateLoader',
            'forum.skins.SkinsTemplateLoader',
        )),
    ]

try:
    if len(FORUM_SCRIPT_ALIAS) > 0:
        APP_URL = '%s/%s' % (APP_URL, FORUM_SCRIPT_ALIAS[:-1])
except NameError:
    pass

app_url_split = APP_URL.split("://")

APP_PROTOCOL = app_url_split[0]
APP_DOMAIN = app_url_split[1].split('/')[0]
APP_BASE_URL = '%s://%s' % (APP_PROTOCOL, APP_DOMAIN)

FORCE_SCRIPT_NAME = ''

for path in app_url_split[1].split('/')[1:]:
    FORCE_SCRIPT_NAME = FORCE_SCRIPT_NAME + '/' + path

if FORCE_SCRIPT_NAME.endswith('/'):
    FORCE_SCRIPT_NAME = FORCE_SCRIPT_NAME[:-1]

#Module system initialization
MODULES_PACKAGE = 'forum_modules'
MODULES_FOLDER = rel(MODULES_PACKAGE)

MODULE_LIST = filter(lambda m: getattr(m, 'CAN_USE', True), [
        __import__('forum_modules.%s' % f, globals(), locals(), ['forum_modules'])
        for f in os.listdir(MODULES_FOLDER)
        if os.path.isdir(os.path.join(MODULES_FOLDER, f)) and
           os.path.exists(os.path.join(MODULES_FOLDER, "%s/__init__.py" % f)) and
           not f in DISABLED_MODULES
])

[MIDDLEWARE_CLASSES.extend(
        ["%s.%s" % (m.__name__, mc) for mc in getattr(m, 'MIDDLEWARE_CLASSES', [])]
                          ) for m in MODULE_LIST]

[TEMPLATE_LOADERS.extend(
        ["%s.%s" % (m.__name__, tl) for tl in getattr(m, 'TEMPLATE_LOADERS', [])]
                          ) for m in MODULE_LIST]


INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.markup',
    'django.contrib.messages',
    'messages_extends',
    'forum',
]
#from messages_extends.models import Message
##
##
##
install_app('debug_toolbar', debug_only=True, middlewares=['debug_toolbar.middleware.DebugToolbarMiddleware'])
install_app('south')
install_app('gunicorn')
install_app('rosetta', debug_only=False)


AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',]
