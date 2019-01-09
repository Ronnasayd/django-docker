#!/usr/bin/env python
# -*- coding: utf-8 -*-

### VERSION: 2.2.2-beta ###

DEBUG=False

BROWSERSYNC_GULP_DEV_TOOLS=True # turn to True or False to enable disable dev tools like browsersync sass etc

# folder to use in developer mode
SCSS_TO_CSS_FOLDERS=["dd_scss","dd_css"]
JS_TO_JSMIN_FOLDERS=["dd_js","dd_jsmin"]
IMAGEMIN_FOLDERS=["dd_images"]


REQUIREMENTS=[
	'channels',
	'channels_redis',
	'django-redis',
	'psycopg2-binary',
	'Pillow',
	'django-widget-tweaks',
	'djangorestframework',
]

PROJECT_NAME='django_docker_example'

PYTHON_VERSION='3.6'

WEB_COMMANDS_BUILD=[
	# 'apt-get install wget -y',
	# 'apt-get install curl -y',
]



DATABASE_IMAGE='postgres'

DATABASE_EXTERNAL=False

### DATABASE_ENVIROMENTS FOR DATABASE_IMAGE
# 	POSTGRESS:
# 		USER_NAME = POSTGRES_USER
# 		PASSWORD_NAME = POSTGRES_PASSWORD
# 		DB_NAME = POSTGRES_DB

# 	MYSQL:
# 		USER_NAME = MYSQL_USER
# 		PASSWORD_NAME = MYSQL_PASSWORD
# 		DB_NAME = MYSQL_DATABASE
		
# 		ROOT_PASSWORD_NAME = MYSQL_ROOT_PASSWORD
# 	MONGO:
# 		USER_NAME = MONGO_INITDB_ROOT_USERNAME
# 		PASSWORD_NAME = MONGO_INITDB_ROOT_PASSWORD
# 		DB_NAME = ''


### DATABASES DEFAULT PORTS
# POSTGRES_PORT=5432
# MYSQL_PORT=3306
# MONGO_PORT=8081


DATABASE_DEFAULT_ENVIROMENTS={

	'DATABASE_USER':'django_docker_example_user',
	'DATABASE_USER_NAME':'POSTGRES_USER',

	'DATABASE_PASSWORD':'!TB2PGy%{PBd)q>E',
	'DATABASE_PASSWORD_NAME':'POSTGRES_PASSWORD',

	'DATABASE_DB':'django_docker_example_db',
	'DATABASE_DB_NAME':'POSTGRES_DB',

	'DATABASE_PORT':'5432',
	'DATABASE_HOST':'http://10.0.0.1', # just use in external database connection
}


DATABASE_OTHERS_ENVIROMENTS={
	'ANY_ENV':'/tmp',
}


### LOCATION OF DATABASE IN CONTAINER
# POSTGRES_DESTINATION = /var/lib/postgresql/data'
# MYSQL_DESTINATION = /var/lib/mysql/
# MONGO_DESTINATION = /var/lib/mongodb

DATABASE_ROOT={
	'DESTINATION':'/var/lib/postgresql/data',
}

WEB_PORT='8000'
NGINX_PORT='80'

WEB_ENVIROMENT={
	# all enviroment variables are optional
	'REDIS_URL':'redis://redis:6379/1',
}


CONTAINERS=[
	# all container are aptional
	'redis', # redis here is just a example of how to add container in network
]


DOCKER_COMPOSE_VERSION='3.5'

NETWORK_NAME='network_dd'



FOLDER_TO_SAVE="dd_generated_files"

ROOT_PASSWD="toor"




# ## PUT OR UPDATE THIS CODE IN YOUR settings.py ###

# from decouple import config

# DEBUG = config('DEBUG', default=False, cast=bool)
# STATIC_ROOT = config('STATIC_ROOT')
# MEDIA_ROOT = config('MEDIA_ROOT')
# STATIC_URL = config('STATIC_URL')
# MEDIA_URL = config('MEDIA_URL')

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql', ## coloque aqui a engine do banco que você vai utilizar ##
#         'HOST': config('DATABASE_HOST'),
#         'PORT': config('DATABASE_PORT'),
#         'NAME': config('DATABASE_NAME'),
#         'USER': config('DATABASE_USER'),
#         'PASSWORD': config('DATABASE_PASSWORD')
#     }
# }


# ## OPTIONAL CODE IF YOU WILL USE REDIS TO CACHE
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": config('REDIS_URL'),
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }
