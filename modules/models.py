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

# VERSION: 3.4.7-beta #


from config import *
from modules.constants import *


NGINX_MODEL={
	'WEB_CONTAINER_NAME':WEB_CONTAINER_NAME,
	'STATIC_ROOT':STATIC_ROOT,
	'WEB_PORT':WEB_PORT,
	'LOGS_ROOT':LOGS_ROOT,
	'MEDIA_ROOT':MEDIA_ROOT,
	'NGINX_SNIPPET_HTTPS': 'include '+NGINX_SNIPPET_HTTPS_NAME+";" if ENABLE_HTTPS else '',
	

}
NGINX_SNIPPET_HTTPS_MODEL={
	'WEB_ROOT_PATH':WEB_ROOT_PATH,
	'SERVER_DNS_NAMES':SERVER_DNS_NAMES,
}

NGINX_CERT_SCRIPT_MODEL={
	'WEB_ROOT_PATH':WEB_ROOT_PATH,
	'SERVER_NAMES':'-d '+' -d '.join(SERVER_NAMES)
}

GULPFILE_MODEL={
	'WEB_CONTAINER_NAME':WEB_CONTAINER_NAME,
	'WEB_PORT':WEB_PORT,
}

MAKE_AMBIENT_MODEL={
	'FOLDER_NAME':FOLDER_TO_SAVE,
	'RUNSERVER_SCRIPT_NAME':RUNSERVER_SCRIPT_NAME,
	'PROJECT_NAME':PROJECT_NAME,
}

RUNSERVER_SCRIPT_MODEL={
	'WEB_PORT':WEB_PORT,
	'PROJECT_NAME':PROJECT_NAME,
	'SETTINGS_FILE_NAME':SETTINGS_FILE_NAME,
}

MANAGE_MODEL={
	'PROJECT_NAME':PROJECT_NAME,
	'SETTINGS_FILE_NAME':SETTINGS_FILE_NAME
}

DDURLS_MODEL={
	'PROJECT_NAME':PROJECT_NAME,
}

SETTINGS_MODEL={
	'PROJECT_NAME':PROJECT_NAME,
}
