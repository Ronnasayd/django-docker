
DEBUG=True

REQUIREMENTS=[
	'channels',
	'channels_redis',
	'psycopg2-binary',
	'Pillow',
	'django-widget-tweaks',
	'djangorestframework',
	'django_compressor',
]

PROJECT_NAME='exemplo'

PYTHON_VERSION='3.6'

WEB_COMMANDS_BUILD=[
	# 'apt-get install wget -y',
	# 'apt-get install curl -y',
]

DATABASE='postgres'

'''
DATABASE_ENVIROMENTS
	POSTGRESS:
		USER_NAME = POSTGRES_USER
		PASSWORD_NAME = POSTGRES_PASSWORD
		DB_NAME = POSTGRES_DB

		PGDATA = /tmp
	MYSQL:
		USER_NAME = MYSQL_USER
		PASSWORD_NAME = MYSQL_PASSWORD
		DB_NAME = MYSQL_DATABASE
		
		ROOT_PASSWORD_NAME = MYSQL_ROOT_PASSWORD
	MONGO:
		USER_NAME = MONGO_INITDB_ROOT_USERNAME
		PASSWORD_NAME = MONGO_INITDB_ROOT_PASSWORD
		DB_NAME = ''
'''
DATABASE_DEFAULT_ENVIROMENTS={
	'DATABASE_USER_VALUE':'exemplouser',
	'DATABASE_USER_NAME':'POSTGRES_USER',

	'DATABASE_PASSWORD_VALUE':'!TB2PGy%{PBd)q>E',
	'DATABASE_PASSWORD_NAME':'POSTGRES_PASSWORD',

	'DATABASE_DB_VALUE':'exemplodb',
	'DATABASE_DB_NAME':'POSTGRES_DB',
}


DATABASE_OTHERS_ENVIROMENTS={
	'ANY_ENV':'/tmp',
}

'''
POSTGRES_DESTINATION = /var/lib/postgresql/data'
MYSQL_DESTINATION = /var/lib/mysql/
MONGO_DESTINATION = /var/lib/mongodb
'''
DATABASE_ROOT={
	'SOURCE':'./databases',
	'DESTINATION':'/var/lib/postgresql/data',
}
'''
POSTGRES_PORT=5432
MYSQL_PORT=3306
MONGO_PORT=8081
'''
DATABASE_PORT='5432'
WEB_PORT='8000'

WEB_ENVIROMENT={
	'REDIS_URL':'redis://redis:6379/0',
	'REDIS_URL2':'redis://redis:6379/0',
}


CONTAINERS=['redis']


DOCKER_COMPOSE_VERSION='3.5'

NETWORK_NAME='network_exemplo'


STATIC_ROOT='/static-data'
MEDIA_ROOT='/media-data'
LOGS_ROOT='/logs-data'


### PUT THIS CODE IN YOUR settings.py ###

# from decouple import config
# DEBUG = config('DEBUG', default=False, cast=bool)
# STATIC_ROOT = config('STATIC_ROOT')
# MEDIA_ROOT = config('MEDIA_ROOT')
# STATIC_URL = /static/
# MEDIA_URL = /media/

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
