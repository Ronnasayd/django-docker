#!/usr/bin/env python
# -*- coding: utf-8 -*-

### VERSION: 1.1.2-beta ###


from config import *


NGINX_MODEL={
	'STATIC_ROOT':STATIC_ROOT,
	'WEB_PORT':WEB_PORT,
	'LOGS_ROOT':LOGS_ROOT,
	'MEDIA_ROOT':MEDIA_ROOT
}

GULPFILE_MODEL={
	'WEB_PORT':WEB_PORT,
	'SCSS_FOLDERS':SCSS_TO_CSS_FOLDERS[0],
	'CSS_FOLDERS':SCSS_TO_CSS_FOLDERS[1],
	'JS_FOLDERS':JS_TO_JSMIN_FOLDERS[0],
	'JSMIN_FOLDERS':JS_TO_JSMIN_FOLDERS[1],
	'IMAGE_FOLDERS':IMAGEMIN_FOLDERS[0]
}

MAKE_AMBIENT_MODEL={
	'FOLDER_NAME':FOLDER_TO_SAVE,
	'RUNSERVER_SCRIPT_NAME':RUNSERVER_SCRIPT_NAME,
	'PROJECT_NAME':PROJECT_NAME,
}

RUNSERVER_SCRIPT_MODEL={
	'WEB_PORT':WEB_PORT,
	'PROJECT_NAME':PROJECT_NAME
}

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