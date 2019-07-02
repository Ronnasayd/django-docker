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
#

# VERSION: 5.0.1-beta #

DEBUG = False

FRONT_DEV_TOOLS = False  # turn to True or False to enable disable dev tools
#  like browsersync sass etc

PROJECT_NAME = 'django_docker_example'

# DATABASES DEFAULT PORTS
# POSTGRES_PORT=5432
# MYSQL_PORT=3306
DATABASE_DATA = {
    'USERNAME': 'django_docker_example_user',
    'PASSWORD': '!TB2PGy%{PBd)q>E',
    'NAME': 'django_docker_example_db',
    'HOST': 'http://10.0.0.1',
    'PORT': '5432',
}

PYTHON_VERSION = '3.6'
DJANGO_VERSION = '2.2.3'

WEB_COMMANDS_BUILD = [
    # 'apt-get install wget -y',
    # 'apt-get install curl -y',
]

CONTAINER_DATABASES = {
    'POSTGRESQL': {
        'DB_IMAGE': 'postgres',
        'DB_USER': 'POSTGRES_USER',
        'DB_PASSWORD': 'POSTGRES_PASSWORD',
        'DB_NAME': 'POSTGRES_DB',
        'DB_DESTINATION': '/var/lib/postgresql/data'
    },
    'MYSQL': {
        'DB_IMAGE': 'mysql',
        'DB_USER': 'MYSQL_USER',
        'DB_PASSWORD': 'MYSQL_PASSWORD',
        'DB_NAME': 'MYSQL_DATABASE',
        'DB_DESTINATION': '/var/lib/mysql'
    }
}


DATABASE_ENGINES = {
    'POSTGRESQL': {
        'DB_ENGINE': 'django.db.backends.postgresql_psycopg2',
    },
    'MYSQL': {
        'DB_ENGINE': 'django.db.backends.mysql'
    },
}


# Concat DATABASE_ENGINE TO DATABASE DATA
DATABASE_DATA.update(DATABASE_ENGINES['POSTGRESQL'])


# RUN DATABASE CONTAINER IN DEVELOPMENT
if DEBUG:
    DATABASE_DATA.update(CONTAINER_DATABASES['POSTGRESQL'])

# This line is used to travis-ci only comment in production
DATABASE_DATA.update(CONTAINER_DATABASES['POSTGRESQL'])

DATABASE_OTHERS_ENVIROMENTS = {
    'ANY_ENV': '/home',
}

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

SERVER_NAMES = ['8faebb1e.ngrok.io ']

NUMBER_WEB_INSTANCES = 1
