#!/usr/bin/env python
# -*- coding: utf-8 -*-

### VERSION: 2.1.1-beta ###

from config import *

ROOT_DIRECTORY="."
PARENT_DIRECTORY=".."

DATABASE_VOLUME = 'database_'+PROJECT_NAME
STATIC_VOLUME = 'static_'+PROJECT_NAME
MEDIA_VOLUME = 'media_'+PROJECT_NAME
LOGS_VOLUME='logs_'+PROJECT_NAME

PROJECT_RENAME = PROJECT_NAME.replace('_','.')
WEB_CONTAINER_NAME='web.'+PROJECT_RENAME
NODE_CONTAINER_NAME='node.'+PROJECT_RENAME
NGINX_CONTAINER_NAME='nginx.'+PROJECT_RENAME
DATABASE_CONTAINER_NAME=DATABASE_IMAGE+'.'+PROJECT_RENAME

OTHERS_CONTAINER_NAME=[container+'.'+PROJECT_RENAME for container in  CONTAINERS]


REQUIREMENTS+=[
'django',
'gunicorn',
'python-decouple',
]

GULP_MODULES=[
 'gulp',
 'node-sass',
 'browser-sync',
 'gulp-sass',
 'gulp-rename',
 'gulp-autoprefixer',
 'gulp-uglify',
 'gulp-sourcemaps',
 'gulp-imagemin',
 ]

STATIC_ROOT='/static-data'
MEDIA_ROOT='/media-data'
LOGS_ROOT='/logs-data'


RUNSERVER_SCRIPT_NAME='runserver.sh'