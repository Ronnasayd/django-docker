from config import *
import os, importlib

settings = importlib.import_module(PROJECT_NAME+'.'+PROJECT_NAME+'.settings')

########################################################################

RUNSERVER_SCRIPT_NAME='runserver'

REQUIREMENTS+=['django','gunicorn'] # adiciona django e gunicorn a requirements

#######################################################################
# Dicionario base
DOCKER={
	'REQUIREMENTS':REQUIREMENTS,
	'PROJECT_NAME':PROJECT_NAME,
	'RUNSERVER_SCRIPT_NAME':RUNSERVER_SCRIPT_NAME,
	'STATIC_ROOT':settings.STATIC_ROOT,
  'MEDIA_ROOT':settings.MEDIA_ROOT,
	'WEB_PORT':WEB_PORT,
	'DATABASE':DATABASE,
	'WEB_ENVIROMENT':WEB_ENVIROMENT,
	'DATABASE_ROOT_SOURCE':DATABASE_ROOT['SOURCE'],
	'DATABASE_ROOT_DESTINATION':DATABASE_ROOT['DESTINATION'],
	'LOGS_ROOT':LOGS_ROOT,
	'DEBUG':settings.DEBUG,
  'DOCKER_COMPOSE_VERSION':DOCKER_COMPOSE_VERSION,
  'PYTHON_VERSION':PYTHON_VERSION,
}
########################################################################
DEPENDS_ON='''
  depends_on:
   - {DATABASE}
 '''.format(**DOCKER)

for container in CONTAINERS:
	DEPENDS_ON+='''
   - {}'''.format(container)

DOCKER['DEPENDS_ON']=DEPENDS_ON
##########################################################################
ENVIROMENT='''
  environment:
'''
for key in WEB_ENVIROMENT:
	ENVIROMENT+='''
   - {}:{}'''.format(key,WEB_ENVIROMENT[key])
DOCKER['ENVIROMENT']=ENVIROMENT
#########################################################################3
#arquivo dockerfile
DOCKERFILE='''FROM python:{PYTHON_VERSION}

USER root

ENV PYTHONUNBUFFERED 1

RUN set -ex && apt-get update

COPY ./requirements.txt ./requirements.txt

RUN set -ex && pip install -r requirements.txt

ADD ./{PROJECT_NAME} /{PROJECT_NAME}
WORKDIR /{PROJECT_NAME}

CMD chmod +x {RUNSERVER_SCRIPT_NAME}.sh'''.format(**DOCKER)

##########################################################################
#brosersync dockerfile
BROWSERSYNC_DOCKERFILE='''
FROM node
RUN set -ex && apt-get update
ADD ./{PROJECT_NAME} /{PROJECT_NAME}
WORKDIR /{PROJECT_NAME}
RUN set -ex && npm install --global browser-sync --save-dev
'''.format(**DOCKER)
#################################################################
#browse-sync compose
BROWSER_SYNC_DOCKERCOMPOSE='''
 browsersync:
  container_name: browsersync
  build:
   context: .
   dockerfile: browsersync.Dockerfile
  restart: always
  ports:
   - 3000:3000
   - 3001:3001
  volumes:
   - ./{PROJECT_NAME}:/{PROJECT_NAME}:rw
   - ./media:{MEDIA_ROOT}:rw
  depends_on:
   - web
  working_dir: /{PROJECT_NAME}
  command: browser-sync start --proxy "web:{WEB_PORT}" --files "**/*"
  stdin_open: true
  tty: true
  '''.format(**DOCKER)
#############################################################################

RUNSERVER_SCRIPT='''#!/bin/bash
python manage.py makemigrations
python manage.py migrate'''

#############################################################################
# arquivo yml para docker compose
DOCKERCOMPOSE='''
version: '{DOCKER_COMPOSE_VERSION}'
services:
 web:
  container_name: web
  build:
   context: .
   dockerfile: {PROJECT_NAME}.Dockerfile
  restart: always
  #ports:
  # - {WEB_PORT}:{WEB_PORT}
  expose:
   - {WEB_PORT}
  working_dir: /{PROJECT_NAME}
  volumes:
   - ./{PROJECT_NAME}:/{PROJECT_NAME}:rw 
   - ./static:{STATIC_ROOT}:rw
   - ./media:{MEDIA_ROOT}:rw
  command: /bin/bash {RUNSERVER_SCRIPT_NAME}.sh

  {DEPENDS_ON}
  {ENVIROMENT}

  stdin_open: true
  tty: true

 {DATABASE}:
  image: {DATABASE}
  container_name: {DATABASE}
  volumes:
   - {DATABASE_ROOT_SOURCE}:{DATABASE_ROOT_DESTINATION}:rw
   '''.format(**DOCKER)

##########################################################################33
# adiciona containers
for container in CONTAINERS:
  CONTAINERS_STRUCT='''
 {}:
  image: {}
  container_name: {}
  restart: always
  '''.format(container,container,container)
  DOCKERCOMPOSE+=CONTAINERS_STRUCT
###########################################################################
#script make ambinte
MAKE_AMBIENT='''
cp ./{RUNSERVER_SCRIPT_NAME}.sh ./{PROJECT_NAME}
mkdir nginx
mv nginx.conf nginx
docker stop $(docker ps -a -q) 
docker system prune --force
docker-compose -f {PROJECT_NAME}.yml build  
'''.format(**DOCKER)
#############################################################################
# Verifica modo produção ou desenvolvimento
if settings.DEBUG:
  MAKE_AMBIENT+='''COMPOSE_HTTP_TIMEOUT=200 docker-compose -f {PROJECT_NAME}.yml up'''.format(**DOCKER)

  
  RUNSERVER_SCRIPT+='''
python manage.py runserver 0.0.0.0:{WEB_PORT}
  '''.format(**DOCKER)

  DOCKERCOMPOSE+=BROWSER_SYNC_DOCKERCOMPOSE
else:
  MAKE_AMBIENT+='''docker-compose -f {PROJECT_NAME}.yml up -d'''.format(**DOCKER)

  RUNSERVER_SCRIPT+='''
python manage.py collectstatic --noinput
gunicorn --bind=0.0.0.0:{WEB_PORT} {PROJECT_NAME}.wsgi
	'''.format(**DOCKER)

  NGINX='''
 nginx:
  container_name: nginx
  restart: always
  image: nginx
  volumes:
   - ./nginx/nginx.conf:/etc/nginx/nginx.conf
   - ./static:{STATIC_ROOT}:rw 
   - ./media:{MEDIA_ROOT}:rw
   - ./logs:{LOGS_ROOT}:rw
  depends_on:
   - web
  ports:
   - 80:{WEB_PORT}
  '''.format(**DOCKER)
  DOCKERCOMPOSE+=NGINX


#########################################################################
#cria arquivos requirements
requirements=open('requirements.txt','w')
for requirement in REQUIREMENTS:
  requirements.write(requirement+'\n')
requirements.close()

###########################################################################
#Arquivo de configuração nginx
NGINX_CONF='''
worker_processes 1;

events {{

    worker_connections 1024;

}}

http {{

    default_type  application/octet-stream;
    include       /etc/nginx/mime.types;

    log_format compression '$remote_addr - $remote_user [$time_local] '
                           '"$request" $status $body_bytes_sent '
                           '"$http_referer" "$http_user_agent" "$gzip_ratio"';
   




    sendfile on;

    gzip              on;
    gzip_http_version 1.0;
    gzip_proxied      any;
    gzip_min_length   500;
    gzip_disable      "MSIE [1-6]\.";
    gzip_types        text/plain text/xml text/css
                      text/comma-separated-values
                      text/javascript
                      application/x-javascript
                      application/atom+xml;

    # Configuration containing list of application servers
    upstream app_servers {{
        ip_hash;
        server web:{WEB_PORT};

    }}

    # Configuration for Nginx
    server {{

        #access_log {LOGS_ROOT}/access.log compression;
        error_log {LOGS_ROOT}/error.log warn;
        

        # Running port
        listen {WEB_PORT};

        # Settings to serve static files 
        location /static/  {{

            # Example:
            # root /full/path/to/application/static/file/dir;
            autoindex on;
            alias {STATIC_ROOT}/;

        }}

        location /media/ {{

            autoindex on;
            alias {MEDIA_ROOT}/;
        }}

       

        # Proxy connections to the application servers
        # app_servers
        location / {{

            proxy_pass         http://app_servers;
            proxy_redirect     off;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Host $server_name;


        }}
    }}
}}

'''.format(**DOCKER)
###########################################################################
#Criando arquivos
dockerfile=open('{PROJECT_NAME}.Dockerfile'.format(**DOCKER),'w')
dockerfile.write(DOCKERFILE)
dockerfile.close()


runserver=open('{RUNSERVER_SCRIPT_NAME}.sh'.format(**DOCKER),'w')
runserver.write(RUNSERVER_SCRIPT)
runserver.close()

dockercompose = open('{PROJECT_NAME}.yml'.format(**DOCKER),'w')
dockercompose.write(DOCKERCOMPOSE)
dockercompose.close()

makeambient=open('make_ambient.sh','w')
makeambient.write(MAKE_AMBIENT)
makeambient.close()


nginxconf = open('nginx.conf','w')
nginxconf.write(NGINX_CONF)
nginxconf.close()

brosersync = open('browsersync.Dockerfile','w')
brosersync.write(BROWSERSYNC_DOCKERFILE)
brosersync.close()