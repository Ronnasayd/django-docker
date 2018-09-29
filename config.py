
DEBUG=False

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

DATABASE='postgres'


### DATABASE_ENVIROMENTS
# 	POSTGRESS:
# 		USER_NAME = POSTGRES_USER
# 		PASSWORD_NAME = POSTGRES_PASSWORD
# 		DB_NAME = POSTGRES_DB

# 		PGDATA = /tmp
# 	MYSQL:
# 		USER_NAME = MYSQL_USER
# 		PASSWORD_NAME = MYSQL_PASSWORD
# 		DB_NAME = MYSQL_DATABASE
		
# 		ROOT_PASSWORD_NAME = MYSQL_ROOT_PASSWORD
# 	MONGO:
# 		USER_NAME = MONGO_INITDB_ROOT_USERNAME
# 		PASSWORD_NAME = MONGO_INITDB_ROOT_PASSWORD
# 		DB_NAME = ''

DATABASE_DEFAULT_ENVIROMENTS={
	'DATABASE_USER_VALUE':'django_docker_example_user',
	'DATABASE_USER_NAME':'POSTGRES_USER',

	'DATABASE_PASSWORD_VALUE':'!TB2PGy%{PBd)q>E',
	'DATABASE_PASSWORD_NAME':'POSTGRES_PASSWORD',

	'DATABASE_DB_VALUE':'django_docker_example_db',
	'DATABASE_DB_NAME':'POSTGRES_DB',
}


DATABASE_OTHERS_ENVIROMENTS={
	'ANY_ENV':'/tmp',
}


### LOCATION OF DATABASE IN CONTAINER
# POSTGRES_DESTINATION = /var/lib/postgresql/data'
# MYSQL_DESTINATION = /var/lib/mysql/
# MONGO_DESTINATION = /var/lib/mongodb

DATABASE_ROOT={
	'SOURCE':'./databases',
	'DESTINATION':'/var/lib/postgresql/data',
}

### DATABASES DEFAULT PORTS
# POSTGRES_PORT=5432
# MYSQL_PORT=3306
# MONGO_PORT=8081

DATABASE_PORT='5432'
WEB_PORT='8000'

WEB_ENVIROMENT={
	'REDIS_URL':'redis://redis:6379/1',
}


CONTAINERS=['redis']


DOCKER_COMPOSE_VERSION='3.5'

NETWORK_NAME='network_django_docker_example'



### PUT OR UPDATE THIS CODE IN YOUR settings.py ###

# from decouple import config

# DEBUG = config('DEBUG', default=False, cast=bool)
# COMPRESS_OFFLINE = config('DEBUG')
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

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     ...
    
# ]+config('DJANGO_DOCKER_APPS', cast=lambda v: [s.strip() for s in v.split(',')])


# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#	   ...
#     'compressor.finders.CompressorFinder',
# )

# COMPRESS_CSS_FILTERS = ["compressor.filters.cssmin.CSSMinFilter"]
# COMPRESS_JS_FILTERS = ["compressor.filters.jsmin.JSMinFilter"]   


### OPTIONAL CODE IF YOU WILL USE REDIS TO CACHE
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": config('REDIS_URL'),
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }
