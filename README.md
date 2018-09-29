



<p align="center"><img src="django-docker.png" alt="django-docker" width="200"/></p>

# Django-Docker
System to automatically create development and production environments in django with docker and facilitate the development of applications.
## Required Programs

 - Python >= 3
 - Docker
 - Docker compose

## How to use

The files  (***wait-for-it.sh***, ***config.py***, ***djangodocker.py*** e ***djangodocker.sh*** ) should be in the directory of your django project.

Modify the ***config.py*** settings as you wish, and then run the djangodocker.sh script. The djangodocker.py file will use config.py settings to mount the desired infrastructure on the system.

The choice of environment between development or production is made by the ***DEBUG*** variable located in the file ***config.py***

In your **settings.py** file modify or add the following lines of code to the values ​​indicated below:
## Put or update this code in your  settings.py ##

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
    
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        ...
        
    ]+config('DJANGO_DOCKER_APPS', cast=lambda v: [s.strip() for s in v.split(',')])
    
    
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        ...
        'compressor.finders.CompressorFinder',
    )
    
    COMPRESS_CSS_FILTERS = ["compressor.filters.cssmin.CSSMinFilter"]
    COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]   
    
    
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


