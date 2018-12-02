#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from copy import deepcopy
from config import *
from modules.dockerfile import Dockerfile
from modules.compose import Container,Service
from modules.controller import Controller
from modules.functional import *

if __name__ == '__main__':

	
	CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
	CURRENT_DIRECTORY = CURRENT_DIRECTORY.replace('\\','/')
	ROOT_DIRECTORY="."
	PARENT_DIRECTORY=".."


#############################################################################	
						## NODE DOCKERFILE OBJECT ##
#############################################################################
	node_dockerfile = Dockerfile()
	node_dockerfile._from(container_base='node')\
	.run(list_of_commands=[
	'apt-get update',
	'yarn global add gulp-cli',
	'yarn global add browser-sync'
	])\
	.add(
		local_path=path_join([ROOT_DIRECTORY,PROJECT_NAME]),
		container_path=path_join([PROJECT_NAME])
	)\
	.workdir(work_directory=path_join([PROJECT_NAME]))\
	.user(container_user='node')\
	.save(
		path_to_save=path_join([CURRENT_DIRECTORY,FOLDER_TO_SAVE]),
		filename='node'
	)
#############################################################################
						## WEB DOCKERFILE OBJECT ##
#############################################################################
	web_dockerfile = Dockerfile()
	web_dockerfile._from(container_base='python:3.6')\
	.add(
		local_path=path_join([FOLDER_TO_SAVE,'requirements.txt']),
		container_path=path_join([ROOT_DIRECTORY,'requirements.txt'])
	)\
	.run(list_of_commands=[
		'apt-get update',
		'pip install -r requirements.txt'
	])\
	.add(
		local_path=path_join([ROOT_DIRECTORY,PROJECT_NAME]),
		container_path=path_join([PROJECT_NAME])
	)\
	.workdir(work_directory=path_join([PROJECT_NAME]))\
	.cmd(last_command='chmod +x '+RUNSERVER_SCRIPT_NAME)\
	.save(
		path_to_save=path_join([CURRENT_DIRECTORY,FOLDER_TO_SAVE]),
		filename='web'
	)
###########################################################################	
						## WEB CONTAINER OBJECT ##
###########################################################################
	web_compose = Container()
	web_compose.name(container_name='web')\
	.build(
		context=CURRENT_DIRECTORY,
	 	dockerfile=path_join([FOLDER_TO_SAVE,web_dockerfile.filename])
	 )\
	.restart(restart_option='always')\
	.ports(list_ports=[
		(WEB_PORT,WEB_PORT),
	])\
	.expose(list_expose_ports=[WEB_PORT])\
	.workdir(work_directory=path_join([PROJECT_NAME]))\
	.command(command='./wait-for-it.sh '+DATABASE_DEFAULT_ENVIROMENTS['DATABASE_HOST']+':'+DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PORT']+' --timeout=15 --strict -- /bin/bash runserver.sh')\
	.depends(list_depends=CONTAINERS if DATABASE_EXTERNAL else [DATABASE_IMAGE]+CONTAINERS)\
	.environ(list_enviroments=[
     ('DEBUG',str(DEBUG)),
     ('STATIC_ROOT',STATIC_ROOT),
     ('STATIC_URL','/static/'),
     ('MEDIA_ROOT',MEDIA_ROOT),
     ('MEDIA_URL','/media/'),
     ('DATABASE_USER',DATABASE_DEFAULT_ENVIROMENTS['DATABASE_USER']),
     ('DATABASE_NAME',DATABASE_DEFAULT_ENVIROMENTS['DATABASE_DB']),
     ('DATABASE_HOST',DATABASE_DEFAULT_ENVIROMENTS['DATABASE_HOST']),
     ('DATABASE_PORT',DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PORT']),
     ('DATABASE_PASSWORD',DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PASSWORD']),
	]+json2list(WEB_ENVIROMENT))\
	.volumes(list_volumes=[
		(
			path_join([CURRENT_DIRECTORY,PROJECT_NAME]),
			path_join([PROJECT_NAME])
		), 
        (
        	path_join([CURRENT_DIRECTORY,'media']),
        	path_join([MEDIA_ROOT])
        )
    ] if DEBUG else [
    	(
    		path_join([CURRENT_DIRECTORY,'media']),
    		path_join([MEDIA_ROOT])
    	),
    	(
    		path_join([CURRENT_DIRECTORY,'static']),
    		path_join([STATIC_ROOT])
    	)
    ])
	# print(web_compose)
###########################################################################
					## DATABASE CONTAINER OBJECT ##
###########################################################################
	database_compose = Container()
	database_compose.name(container_name=DATABASE_IMAGE)\
	.image(image_base=DATABASE_IMAGE)\
	.restart(restart_option='always')\
	.volumes(list_volumes=[
		('database',DATABASE_ROOT['DESTINATION'])
	])\
	.environ([
		(DATABASE_DEFAULT_ENVIROMENTS['DATABASE_USER_NAME'],DATABASE_DEFAULT_ENVIROMENTS['DATABASE_USER']),
		(DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PASSWORD_NAME'],DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PASSWORD']),
		(DATABASE_DEFAULT_ENVIROMENTS['DATABASE_DB_NAME'],DATABASE_DEFAULT_ENVIROMENTS['DATABASE_DB']),
	]+json2list(DATABASE_OTHERS_ENVIROMENTS))
	# print(database_compose)
###########################################################################
					## NODE CONTAINER OBJECT ##
###########################################################################
	node_compose = Container()
	node_compose.name(container_name="node")\
	.build(
		context=CURRENT_DIRECTORY,
	 	dockerfile=path_join([FOLDER_TO_SAVE,node_dockerfile.filename])
	 )\
	.restart(restart_option="always")\
	.ports(list_ports=[
		('3000','3000'),
		('3001','3001'),
		('3002','3002')
	])\
	.volumes(list_volumes=[
		(
			path_join([CURRENT_DIRECTORY,PROJECT_NAME]),
			path_join([PROJECT_NAME])
		)
	])\
	.depends(list_depends=[web_compose.container_name])\
	.workdir(work_directory=path_join([PROJECT_NAME]))\
	.command(command="bash gulp.sh")
	# print(node_compose)
############################################################################
					## NGINX CONTAINER OBJECT ##
############################################################################
nginx_compose = Container()
nginx_compose.name(container_name='nginx')\
.image(image_base='nginx')\
.restart(restart_option='always')\
.volumes(list_volumes=[
	(path_join([CURRENT_DIRECTORY,FOLDER_TO_SAVE,'nginx','nginx.conf']) , "/etc/nginx/nginx.conf"),
	(path_join([CURRENT_DIRECTORY,'static']),STATIC_ROOT),
	(path_join([CURRENT_DIRECTORY,'media']),MEDIA_ROOT),
	(path_join([CURRENT_DIRECTORY,'logs']),LOGS_ROOT)
])\
.depends(list_depends=[web_compose.container_name])\
.ports(list_ports=[
	('80',WEB_PORT)
])
# print(node_compose)
##########################################################################
						## USER CONTAINERS OBJECTS##
###########################################################################
user_containers = []
for container_image in CONTAINERS:
	temporary_container = Container()\
	.name(container_image)\
	.image(container_image)\
	.restart('always')
	user_containers.append(temporary_container)
###########################################################################
						## FINAL COMPOSE FILES ##
###########################################################################
containers_base = [web_compose]+user_containers
filename_development=PROJECT_NAME+'_development'
filename_production=PROJECT_NAME+'_production'

containers_production = containers_base + [nginx_compose]
containers_development = containers_base

if BROWSERSYNC_GULP_DEV_TOOLS:
	containers_development += [node_compose]
if not DATABASE_EXTERNAL:
	containers_development += [database_compose]
	containers_production += [database_compose]


service = Service()\
.version(service_version=DOCKER_COMPOSE_VERSION)\
.volumes(list_of_volumes=['database'])\
.networks(list_of_networks=[NETWORK_NAME])

service_development = deepcopy(service)
service_development.containers(list_of_containers=containers_development)\
.build()\
.save(
	path_to_save=path_join([CURRENT_DIRECTORY,FOLDER_TO_SAVE]),
	filename=filename_development
)

service_production = deepcopy(service)
service_production.containers(list_of_containers=containers_production)\
.build()\
.save(
	path_to_save=path_join([CURRENT_DIRECTORY,FOLDER_TO_SAVE]),
	filename=filename_production
)
########################################################################
					## MVC GENERATED FILES ##
########################################################################

controller = Controller()
nginx_content = controller.build_nginx()
gulpfile_content = controller.build_gulpfile()
make_ambient_content = controller.build_make_ambiente(debug_mode=DEBUG)
runserver_content = controller.build_runserver(debug_mode=DEBUG)
requirements_content = controller.build_requirements()
gulp_script_content = controller.build_gulp_script()


save(path_join([CURRENT_DIRECTORY,FOLDER_TO_SAVE,'nginx']),'nginx.conf',nginx_content)
save(path_join([CURRENT_DIRECTORY,FOLDER_TO_SAVE]),'gulpfile.js',gulpfile_content)
save(path_join([CURRENT_DIRECTORY,FOLDER_TO_SAVE]),'make_ambient.sh',make_ambient_content)
save(path_join([CURRENT_DIRECTORY,FOLDER_TO_SAVE]),RUNSERVER_SCRIPT_NAME,runserver_content)
save(path_join([CURRENT_DIRECTORY,FOLDER_TO_SAVE]),'requirements.txt',requirements_content)
save(path_join([CURRENT_DIRECTORY,FOLDER_TO_SAVE]),'gulp.sh',gulp_script_content)
########################################################################