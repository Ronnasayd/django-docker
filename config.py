# -*- coding: utf-8 -*-

# MIT License

# Copyright (c) 2019 Ronnasayd de Sousa Machado

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# VERSION: 3.4.0-beta #

DEBUG = False

FRONT_DEV_TOOLS = True  # turn to True or False to enable disable dev tools
#  like browsersync sass etc

REQUIREMENTS = [
  'channels',
  'channels_redis',
  'django-redis',
  'django-widget-tweaks',
  'djangorestframework',
  'docutils',
  
]

PROJECT_NAME = 'django_docker_example'

PYTHON_VERSION = '3.6'
DJANGO_VERSION = '2.1.5'

WEB_COMMANDS_BUILD = [
  # 'apt-get install wget -y',
  # # 'apt-get install curl -y',
]

DATABASE_IMAGE = 'postgres'
DATABASE_EXTERNAL = False

# DATABASE_ENVIROMENTS FOR DATABASE_IMAGE
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


# DATABASES DEFAULT PORTS
# POSTGRES_PORT=5432
# MYSQL_PORT=3306
# MONGO_PORT=8081


DATABASE_DEFAULT_ENVIROMENTS = {
  'DATABASE_USER': 'django_docker_example_user',
  'DATABASE_USER_NAME': 'POSTGRES_USER',
  'DATABASE_PASSWORD': '!TB2PGy%{PBd)q>E',
  'DATABASE_PASSWORD_NAME': 'POSTGRES_PASSWORD',
  'DATABASE_DB': 'django_docker_example_db',
  'DATABASE_DB_NAME': 'POSTGRES_DB',
  'DATABASE_PORT': '5432',
  'DATABASE_HOST': 'http://10.0.0.1',  # just use in external database
  # connection
}


DATABASE_OTHERS_ENVIROMENTS = {
  'ANY_ENV': '/home',
}


# LOCATION OF DATABASE IN CONTAINER
# POSTGRES_DESTINATION = /var/lib/postgresql/data'
# MYSQL_DESTINATION = /var/lib/mysql/
# MONGO_DESTINATION = /var/lib/mongodb

DATABASE_ROOT = {
  'DESTINATION': '/var/lib/postgresql/data',
}
# USE ONE OF DEFAULT DJANGO DATABASES ENGINES ###
# Database							Django ENGINE value
# ------------------------------------------------------------------------ #
# MySQL							    django.db.backends.mysql
# Oracle							  django.db.backends.oracle
# PostgreSQL						django.db.backends.postgresql_psycopg2
# SQLite							  django.db.backends.sqlite3
DATABASE_ENGINE = 'django.db.backends.postgresql_psycopg2'

WEB_PORT = '8000'
NGINX_PORT = '80'
DATABASE_EXTERNAL_PORT = '5433'

WEB_ENVIROMENT = {
  # all enviroment variables are optional
  'REDIS_URL': 'redis://redis:6379/1',
}


CONTAINERS = [
  # all container are aptional
  'redis',  # redis here is just a example of how to add container in network
]


DOCKER_COMPOSE_VERSION = '3.3'

NETWORK_NAME = "dd_net"

FOLDER_TO_SAVE = "dd_auxfiles"
