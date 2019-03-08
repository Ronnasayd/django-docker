
from .settings import *
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
STATIC_ROOT = config('STATIC_ROOT')
MEDIA_ROOT = config('MEDIA_ROOT')
STATIC_URL = config('STATIC_URL')
MEDIA_URL = config('MEDIA_URL')

try:
    if 'default' not in DATABASES:
        DATABASES['default']['ENGINE'] = config('DATABASE_ENGINE'),
        DATABASES['default']['HOST'] = config('DATABASE_HOST'),
        DATABASES['default']['PORT'] = config('DATABASE_PORT'),
        DATABASES['default']['NAME'] = config('DATABASE_NAME'),
        DATABASES['default']['USER'] = config('DATABASE_USER'),
        DATABASES['default']['PASSWORD'] = config('DATABASE_PASSWORD'),
    else:
        raise KeyError("Dont use 'default' as DATABASES key. Django-Docker will override it")

except (KeyError, NameError) as err:
    DATABASES = {
        'default': {
            'ENGINE':config('DATABASE_ENGINE'), ## coloque aqui a engine do banco que você vai utilizar ##
            'HOST': config('DATABASE_HOST'),
            'PORT': config('DATABASE_PORT'),
            'NAME': config('DATABASE_NAME'),
            'USER': config('DATABASE_USER'),
            'PASSWORD': config('DATABASE_PASSWORD')
        }
    }

## CODE IF YOU WILL USE REDIS TO CACHE
if config('REDIS_URL',default=None) != None:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": config('REDIS_URL'),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }

try:
    STATICFILES_DIRS += [
        os.path.join(BASE_DIR,"static"),
    ]
except NameError as err:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR,"static"),
    ]

if DEBUG:
    def custom_show_toolbar(request):
        return True  # Always show toolbar, for example purposes only.

    INSTALLED_APPS += [
        "debug_toolbar",
        "autofixture",
    ]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': 'django_docker_example.ddsettings.custom_show_toolbar',
    }
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ]
    ROOT_URLCONF = "django_docker_example.ddurls"
