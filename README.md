



<p align="center"><img src="django-docker.png" alt="django-docker" width="200"/></p>

# Django-Docker 
https://ronnasayd.github.io/django-docker/

System to automatically create development and production environments in django with docker and facilitate the development of applications.
## Required Programs

 - Python >= 3
 - Docker
 - Docker compose

## How to use

The files  (***config.py***, ***pydd.py*** e ***dd.sh*** ) and the folder (***modules***) should be in the directory of your django project.

Modify the ***config.py*** settings as you wish, and then run the ***dd.sh*** script. The ***pydd.py*** file will use ***config.py*** settings to mount the desired infrastructure on the system.

The choice of environment between development or production is made by the ***DEBUG*** variable located in the file ***config.py***

In your **settings.py** file modify or add the following lines of code to the values ​​indicated below:
## Put or update this code in your  ***settings.py*** ##

    from decouple import config
    
    DEBUG = config('DEBUG', default=False, cast=bool)
    COMPRESS_OFFLINE = config('DEBUG')
    STATIC_ROOT = config('STATIC_ROOT')
    MEDIA_ROOT = config('MEDIA_ROOT')
    STATIC_URL = config('STATIC_URL')
    MEDIA_URL = config('MEDIA_URL')
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql', ## coloque aqui a engine do banco que você vai utilizar ##
            'HOST': config('DATABASE_HOST'),
            'PORT': config('DATABASE_PORT'),
            'NAME': config('DATABASE_NAME'),
            'USER': config('DATABASE_USER'),
            'PASSWORD': config('DATABASE_PASSWORD')
        }
    }
        
    
    ## OPTIONAL CODE IF YOU WILL USE REDIS TO CACHE
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": config('REDIS_URL'),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }


