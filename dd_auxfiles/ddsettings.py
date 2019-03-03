from .settings import *
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
STATIC_ROOT = config('STATIC_ROOT')
MEDIA_ROOT = config('MEDIA_ROOT')
STATIC_URL = config('STATIC_URL')
MEDIA_URL = config('MEDIA_URL')

try:
    DATABASES['default']['ENGINE']=config('DATABASE_ENGINE'),
    DATABASES['default']['HOST']=config('DATABASE_HOST'),
    DATABASES['default']['PORT']=config('DATABASE_PORT'),
    DATABASES['default']['NAME']=config('DATABASE_NAME'),
    DATABASES['default']['USER']=config('DATABASE_USER'),
    DATABASES['default']['PASSWORD']=config('DATABASE_PASSWORD'),
except:
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
except:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR,"static"),
    ]