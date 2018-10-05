from config import *
import os, importlib

# settings = importlib.import_module(PROJECT_NAME+'.'+PROJECT_NAME+'.settings')
########################################################################
STATIC_ROOT='/static-data'
MEDIA_ROOT='/media-data'
LOGS_ROOT='/logs-data'

WEB_ENVIROMENT['DEBUG']=str(DEBUG)
WEB_ENVIROMENT['STATIC_ROOT']=STATIC_ROOT
WEB_ENVIROMENT['MEDIA_ROOT']=MEDIA_ROOT
WEB_ENVIROMENT['DATABASE_HOST']=DATABASE
WEB_ENVIROMENT['DATABASE_PORT']=DATABASE_PORT
WEB_ENVIROMENT['DATABASE_NAME'] = DATABASE_DEFAULT_ENVIROMENTS['DATABASE_DB_VALUE']
WEB_ENVIROMENT['DATABASE_USER'] = DATABASE_DEFAULT_ENVIROMENTS['DATABASE_USER_VALUE']
WEB_ENVIROMENT['DATABASE_PASSWORD'] = DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PASSWORD_VALUE']
WEB_ENVIROMENT['STATIC_URL']='/static/'
WEB_ENVIROMENT['MEDIA_URL']='/media/'
WEB_ENVIROMENT['DJANGO_DOCKER_APPS']="compressor,cssmin,jsmin"
RUNSERVER_SCRIPT_NAME='runserver'

REQUIREMENTS+=[
'django',
'gunicorn',
'python-decouple',
'django_compressor',
'cssmin',
'jsmin',

] # adiciona django e gunicorn a requirements

#######################################################################
# Dicionario base
DOCKER={
	'REQUIREMENTS':REQUIREMENTS,
	'PROJECT_NAME':PROJECT_NAME,
	'RUNSERVER_SCRIPT_NAME':RUNSERVER_SCRIPT_NAME,
	'STATIC_ROOT':STATIC_ROOT,
  'MEDIA_ROOT':MEDIA_ROOT,
	'WEB_PORT':WEB_PORT,
	'DATABASE':DATABASE,
	'WEB_ENVIROMENT':WEB_ENVIROMENT,
#	'DATABASE_ROOT_SOURCE':DATABASE_ROOT['SOURCE'],
	'DATABASE_ROOT_DESTINATION':DATABASE_ROOT['DESTINATION'],
	'LOGS_ROOT':LOGS_ROOT,
  'DOCKER_COMPOSE_VERSION':DOCKER_COMPOSE_VERSION,
  'PYTHON_VERSION':PYTHON_VERSION,
  'DATABASE_DB_NAME':DATABASE_DEFAULT_ENVIROMENTS['DATABASE_DB_NAME'],
  'DATABASE_USER_NAME':DATABASE_DEFAULT_ENVIROMENTS['DATABASE_USER_NAME'],
  'DATABASE_PASSWORD_NAME':DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PASSWORD_NAME'],
  'DATABASE_DB_VALUE':DATABASE_DEFAULT_ENVIROMENTS['DATABASE_DB_VALUE'],
  'DATABASE_USER_VALUE':DATABASE_DEFAULT_ENVIROMENTS['DATABASE_USER_VALUE'],
  'DATABASE_PASSWORD_VALUE':DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PASSWORD_VALUE'],
  'DATABASE_PORT':DATABASE_PORT,
  'NETWORK_NAME':NETWORK_NAME
}
########################################################################
DEPENDS_ON='''depends_on:
   - {DATABASE}
 '''.format(**DOCKER)
if len(CONTAINERS) >= 1:
  for container in CONTAINERS:
    DEPENDS_ON+='''  - {}'''.format(container)

DOCKER['DEPENDS_ON']=DEPENDS_ON
##########################################################################
if len(WEB_ENVIROMENT) >= 1:
  ENVIROMENT='''environment:'''
  for key in WEB_ENVIROMENT:
  	ENVIROMENT+='''
   - {}={}'''.format(key,WEB_ENVIROMENT[key])
  DOCKER['ENVIROMENT']=ENVIROMENT
else:
  DOCKER['ENVIROMENT']=''
#########################################################################
NETWORK='''
volumes:
 database:
networks:
 {NETWORK_NAME}:
'''.format(**DOCKER)
##########################################################################
#arquivo dockerfile
DOCKERFILE='''FROM python:{PYTHON_VERSION}
ENV PYTHONUNBUFFERED 1
RUN set -ex && apt-get update
COPY ./requirements.txt ./requirements.txt
RUN set -ex && pip install -r requirements.txt
ADD ./{PROJECT_NAME} /{PROJECT_NAME}
WORKDIR /{PROJECT_NAME}
RUN set -ex && chmod +x ./wait-for-it.sh
'''.format(**DOCKER)
if len(WEB_COMMANDS_BUILD) >= 1:
  for command in WEB_COMMANDS_BUILD:
    DOCKERFILE+='RUN set -ex && '+command+'\n'
DOCKERFILE_FINAL_LINE='''CMD chmod +x {RUNSERVER_SCRIPT_NAME}.sh'''.format(**DOCKER)
DOCKERFILE+=DOCKERFILE_FINAL_LINE

##########################################################################
#brosersync dockerfile
BROWSERSYNC_DOCKERFILE='''
FROM node
RUN set -ex && apt-get update
RUN set -ex && npm install --global browser-sync --save
ADD ./{PROJECT_NAME} /{PROJECT_NAME}
WORKDIR /{PROJECT_NAME}
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
   - 3002:3002
  volumes:
   - ./{PROJECT_NAME}:/{PROJECT_NAME}:rw
  depends_on:
   - web
  working_dir: /{PROJECT_NAME}
  command: browser-sync start --proxy "web:{WEB_PORT}" --files "**/*" --ws "true"
  stdin_open: true
  tty: true
  networks:
   - {NETWORK_NAME}
  '''.format(**DOCKER)
############################################################################

RUNSERVER_SCRIPT='''#!/bin/bash
python manage.py makemigrations
python manage.py migrate'''

#############################################################################
# arquivo yml para docker compose
DOCKERCOMPOSE_BASE='''
version: '{DOCKER_COMPOSE_VERSION}'
services:
 web:
  container_name: web
  build:
   context: .
   dockerfile: {PROJECT_NAME}.Dockerfile
  restart: always
  ports:
   - {WEB_PORT}:{WEB_PORT}
  expose:
   - {WEB_PORT}
  working_dir: /{PROJECT_NAME}
  command: ./wait-for-it.sh {DATABASE}:{DATABASE_PORT} --timeout=15 --strict -- /bin/bash {RUNSERVER_SCRIPT_NAME}.sh
  {DEPENDS_ON}
  {ENVIROMENT}
  stdin_open: true
  tty: true
  networks:
   - {NETWORK_NAME}'''.format(**DOCKER)
###################################################################################
VOLUMES_DEVELOPMENT='''
  volumes:
   - ./{PROJECT_NAME}:/{PROJECT_NAME}:rw 
   - ./media:{MEDIA_ROOT}:rw
'''.format(**DOCKER)

VOLUMES_PRODUCTION='''
  volumes:
   - ./static:{STATIC_ROOT}:rw
   - ./media:{MEDIA_ROOT}:rw
'''.format(**DOCKER)

DATABASE_BASE=''' 

 {DATABASE}:
  image: {DATABASE}
  container_name: {DATABASE}
  restart: always
  networks:
   - {NETWORK_NAME}
  volumes:
   - database:{DATABASE_ROOT_DESTINATION}
  environment:
   - {DATABASE_USER_NAME}={DATABASE_USER_VALUE}
   - {DATABASE_PASSWORD_NAME}={DATABASE_PASSWORD_VALUE}
   - {DATABASE_DB_NAME}={DATABASE_DB_VALUE}
   '''.format(**DOCKER)

DOCKERCOMPOSE_DEVELOPMENT = DOCKERCOMPOSE_BASE + VOLUMES_DEVELOPMENT + DATABASE_BASE
DOCKERCOMPOSE_PRODUCTION = DOCKERCOMPOSE_BASE + VOLUMES_PRODUCTION + DATABASE_BASE
##########################################################################
if len(DATABASE_OTHERS_ENVIROMENTS) >= 1:
  DOE=''
  for key in DATABASE_OTHERS_ENVIROMENTS:
    DOE+='''- {}={}'''.format(key,DATABASE_OTHERS_ENVIROMENTS[key])
  DOCKERCOMPOSE_DEVELOPMENT+=DOE
  DOCKERCOMPOSE_PRODUCTION+=DOE

###########################################################################
# adiciona containers
for container in CONTAINERS:
  CONTAINERS_STRUCT='''
  
 {}:
  image: {}
  container_name: {}
  restart: always
  networks:
   - {}
  '''.format(container,container,container,NETWORK_NAME)
  DOCKERCOMPOSE_DEVELOPMENT+=CONTAINERS_STRUCT
  DOCKERCOMPOSE_PRODUCTION+=CONTAINERS_STRUCT
###########################################################################
#script make ambinte
MAKE_AMBIENT='''
sed -i "s/\\r$//" ./{RUNSERVER_SCRIPT_NAME}.sh
sed -i "s/\\r$//" ./wait-for-it.sh
cp ./{RUNSERVER_SCRIPT_NAME}.sh ./{PROJECT_NAME}
cp ./wait-for-it.sh ./{PROJECT_NAME}
mkdir nginx
mv nginx.conf nginx  
'''.format(**DOCKER)
#############################################################################
NGINX='''
 nginx:
  container_name: nginx
  restart: always
  image: nginx
  networks:
   - {NETWORK_NAME} 
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
#############################################################################
DOCKERCOMPOSE_DEVELOPMENT +=BROWSER_SYNC_DOCKERCOMPOSE+NETWORK
DOCKERCOMPOSE_PRODUCTION +=NGINX+NETWORK
#############################################################################
# Verifica modo produção ou desenvolvimento
if DEBUG:
  MAKE_AMBIENT+='''docker-compose -f {PROJECT_NAME}_development.yml stop
docker-compose -f {PROJECT_NAME}_production.yml stop
docker-compose -f {PROJECT_NAME}_development.yml down
docker-compose -f {PROJECT_NAME}_production.yml down
docker system prune --force
docker-compose -f {PROJECT_NAME}_development.yml build
COMPOSE_HTTP_TIMEOUT=200 docker-compose -f {PROJECT_NAME}_development.yml up --remove-orphans --force-recreate'''.format(**DOCKER)

  
  RUNSERVER_SCRIPT+='''
python manage.py runserver 0.0.0.0:{WEB_PORT}
  '''.format(**DOCKER)
  # DOCKERCOMPOSE+=BROWSER_SYNC_DOCKERCOMPOSE
else:
  MAKE_AMBIENT+='''docker-compose -f {PROJECT_NAME}_production.yml stop
docker-compose -f {PROJECT_NAME}_development.yml stop
docker-compose -f {PROJECT_NAME}_production.yml down
docker-compose -f {PROJECT_NAME}_development.yml down
docker system prune --force
docker-compose -f {PROJECT_NAME}_production.yml build
docker-compose -f {PROJECT_NAME}_production.yml up  -d --remove-orphans --force-recreate'''.format(**DOCKER)

  RUNSERVER_SCRIPT+='''
python manage.py collectstatic --noinput
python manage.py compress --force
gunicorn --bind=0.0.0.0:{WEB_PORT} --workers=3 {PROJECT_NAME}.wsgi
	'''.format(**DOCKER)

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

    proxy_cache_path {STATIC_ROOT} levels=1:2 keys_zone=my_cache:10m max_size=10g 
        inactive=60m use_temp_path=off;

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

        # Max_size
        client_max_body_size 20M;

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


            proxy_cache my_cache;
            proxy_cache_revalidate on;
            proxy_cache_min_uses 3;
            proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
            proxy_cache_background_update on;
            proxy_cache_lock on;

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

dockercompose = open('{PROJECT_NAME}_development.yml'.format(**DOCKER),'w')
dockercompose.write(DOCKERCOMPOSE_DEVELOPMENT)
dockercompose.close()

dockercompose = open('{PROJECT_NAME}_production.yml'.format(**DOCKER),'w')
dockercompose.write(DOCKERCOMPOSE_PRODUCTION)
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

