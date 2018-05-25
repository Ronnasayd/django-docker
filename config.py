
REQUIREMENTS=[
	'django',
	'gunicorn',
	'channels',
	'channels_redis',
	'psycopg2',
	'Pillow',
]

PROJECT_NAME='exemplo'

IMAGE_BASE:'python:3.6'

DATABASE='postgres'

LOGS_ROOT='/logs'

DATABASE_ROOT={
	'SOURCE':'./databases',
	'DESTINATION':'/var/lib/postgresql/data',
}

WEB_PORT='8000'

WEB_ENVIROMENT={
	'REDIS_URL':'redis://redis:6379/0',
	'REDIS_URL2':'redis://redis:6379/0',
}

CONTAINERS=['redis']

DOCKER_COMPOSE_VERSION='3'
