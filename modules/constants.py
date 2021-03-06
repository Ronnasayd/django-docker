#!/usr/bin/env python
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

# VERSION: 5.1.1-beta #

from config import *

ROOT_DIRECTORY = "."
PARENT_DIRECTORY = ".."
PROJECT_NAME_LOWER = PROJECT_NAME.lower()

DATABASE_VOLUME = 'database_'+PROJECT_NAME_LOWER
STATIC_VOLUME = 'static_'+PROJECT_NAME_LOWER
MEDIA_VOLUME = 'media_'+PROJECT_NAME_LOWER
LOGS_VOLUME = 'logs_'+PROJECT_NAME_LOWER
PROJECT_VOLUME = 'app_'+PROJECT_NAME_LOWER

WEB_ROOT_VOLUME = "web_root_"+PROJECT_NAME_LOWER
CERTBOT_ETC_VOLUME = "certbot_etc_"+PROJECT_NAME_LOWER
CERTBOT_VAR_VOLUME = "certbot_var_"+PROJECT_NAME_LOWER

PROJECT_RENAME = PROJECT_NAME.replace('_', '.')
WEB_CONTAINER_NAME = 'web-'+PROJECT_RENAME
NODE_CONTAINER_NAME = 'node-'+PROJECT_RENAME
NGINX_CONTAINER_NAME = 'nginx-'+PROJECT_RENAME


OTHERS_CONTAINER_NAME = [container+'-' +
                         PROJECT_RENAME for container in CONTAINERS]

DATABASE_EXTERNAL = not 'DB_IMAGE' in DATABASE_DATA
if not DATABASE_EXTERNAL:
    DATABASE_CONTAINER_NAME = DATABASE_DATA['DB_IMAGE']+'-'+PROJECT_RENAME


STATIC_ROOT = '/tmp/static-data'
MEDIA_ROOT = '/tmp/media-data'
LOGS_ROOT = '/tmp/logs-data'


RUNSERVER_SCRIPT_NAME = 'runserver.sh'
SETTINGS_FILE_NAME = 'ddsettings'

WEB_ROOT_PATH = '/var/www/html'
SERVER_DNS_NAMES = ' '.join(SERVER_NAMES)

NGINX_SNIPPET_HTTPS_NAME = 'nginx-snippet-https.conf'

WEB_ROOT = "/var/www/html"
CERTBOT_ETC = "/etc/letsencrypt"
CERTBOT_VAR = "/var/lib/letsencrypt"

NUMBER_WEB_INSTANCES = NUMBER_WEB_INSTANCES

WEB_IS_BIGGER_THAN_ONE = (NUMBER_WEB_INSTANCES > 1)

ENABLE_HTTPS = (len(SERVER_NAMES) >= 1)
