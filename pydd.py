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

### VERSION: 2.3.2-beta ###

import os
from copy import deepcopy,copy
from config import *
from modules.dockerfile import Dockerfile
from modules.compose import Container,Service
from modules.controller import Controller
from modules.functional import *
from modules.constants import *



if __name__ == '__main__':


	
	CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
	CURRENT_DIRECTORY = CURRENT_DIRECTORY.replace('\\','/')
	



#############################################################################	
						## NODE DOCKERFILE OBJECT ##
#############################################################################
	node_dockerfile = Dockerfile()
	(node_dockerfile._from(container_base='node')
	.run(list_of_commands=[
	'apt-get update',
	'yarn global add gulp-cli',
	'yarn global add browser-sync'
	])
	.add(
		local_path=path_join([ROOT_DIRECTORY,PROJECT_NAME]),
		container_path=path_join([PROJECT_NAME])
	)
	.workdir(work_directory=path_join([PROJECT_NAME]))
	.user(container_user='node')
	.save(
		path_to_save=path_join([CURRENT_DIRECTORY,FOLDER_TO_SAVE]),
		filename='node'
	))
#############################################################################
						## WEB DOCKERFILE OBJECT ##
#############################################################################
	web_dockerfile = Dockerfile()
	(web_dockerfile._from(container_base='python:'+PYTHON_VERSION)
	.add(
		local_path=path_join([FOLDER_TO_SAVE,'requirements.txt']),
		container_path=path_join([ROOT_DIRECTORY,'requirements.txt'])
	)
	.run(list_of_commands=[
		'apt-get update',
		'pip install --upgrade pip',
		'pip install -r requirements.txt'
	]+WEB_COMMANDS_BUILD)
	.add(
		local_path=path_join([ROOT_DIRECTORY,PROJECT_NAME]),
		container_path=path_join([PROJECT_NAME])
	)
	.workdir(work_directory=path_join([PROJECT_NAME]))
	.cmd(last_command='chmod +x '+RUNSERVER_SCRIPT_NAME)
	.save(
		path_to_save=path_join([CURRENT_DIRECTORY,FOLDER_TO_SAVE]),
		filename='web'
	))
###########################################################################	
						## WEB CONTAINER OBJECT ##
###########################################################################
	web_compose = Container()
	(web_compose.name(container_name=WEB_CONTAINER_NAME)
	.build(
		context=CURRENT_DIRECTORY,
	 	dockerfile=path_join([FOLDER_TO_SAVE,web_dockerfile.filename])
	 )
	.restart(restart_option='always')
	.ports(list_ports=[
		(WEB_PORT,WEB_PORT),
	])\
	.expose(list_expose_ports=[WEB_PORT])
	.workdir(work_directory=path_join([PROJECT_NAME]))
	.command(command='./wait-for-it.sh '+(DATABASE_DEFAULT_ENVIROMENTS['DATABASE_HOST'] if DATABASE_EXTERNAL else DATABASE_CONTAINER_NAME)+':'+DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PORT']+' --timeout=15 --strict -- /bin/bash runserver.sh')
	.depends(list_depends=OTHERS_CONTAINER_NAME if DATABASE_EXTERNAL else [DATABASE_CONTAINER_NAME]+OTHERS_CONTAINER_NAME)
	.environ(list_enviroments=[
     ('DEBUG',str(DEBUG)),
     ('STATIC_ROOT',STATIC_ROOT),
     ('STATIC_URL','/static/'),
     ('MEDIA_ROOT',MEDIA_ROOT),
     ('MEDIA_URL','/media/'),
     ('DATABASE_USER',DATABASE_DEFAULT_ENVIROMENTS['DATABASE_USER']),
     ('DATABASE_NAME',DATABASE_DEFAULT_ENVIROMENTS['DATABASE_DB']),
     ('DATABASE_HOST',(DATABASE_DEFAULT_ENVIROMENTS['DATABASE_HOST'] if DATABASE_EXTERNAL else DATABASE_CONTAINER_NAME)),
     ('DATABASE_PORT',DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PORT']),
     ('DATABASE_PASSWORD',DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PASSWORD']),
	]+json2list(WEB_ENVIROMENT))
	.volumes(list_volumes=[
		(
			path_join([CURRENT_DIRECTORY,PROJECT_NAME]),
			path_join([PROJECT_NAME])
		), 
        (
        	MEDIA_VOLUME,
        	path_join([MEDIA_ROOT])
        )
    ] if DEBUG else [
    	(
    		MEDIA_VOLUME,
    		path_join([MEDIA_ROOT])
    	),
    	(
    		STATIC_VOLUME,
    		path_join([STATIC_ROOT])
    	)
    ]))
	# print(web_compose)
###########################################################################
					## DATABASE CONTAINER OBJECT ##
###########################################################################
	database_compose = Container()
	(database_compose.name(container_name=DATABASE_CONTAINER_NAME)
	.image(image_base=DATABASE_IMAGE)
	.restart(restart_option='always')
	.volumes(list_volumes=[
		(DATABASE_VOLUME,DATABASE_ROOT['DESTINATION'])
	])
	.environ([
		(DATABASE_DEFAULT_ENVIROMENTS['DATABASE_USER_NAME'],DATABASE_DEFAULT_ENVIROMENTS['DATABASE_USER']),
		(DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PASSWORD_NAME'],DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PASSWORD']),
		(DATABASE_DEFAULT_ENVIROMENTS['DATABASE_DB_NAME'],DATABASE_DEFAULT_ENVIROMENTS['DATABASE_DB']),
	]+json2list(DATABASE_OTHERS_ENVIROMENTS))
	)
	# print(database_compose)
###########################################################################
					## NODE CONTAINER OBJECT ##
###########################################################################
	node_compose = Container()
	(node_compose.name(container_name=NODE_CONTAINER_NAME)
	.build(
		context=CURRENT_DIRECTORY,
	 	dockerfile=path_join([FOLDER_TO_SAVE,node_dockerfile.filename])
	 )
	.restart(restart_option="always")
	.ports(list_ports=[
		('3000','3000'),
		('3001','3001'),
		('3002','3002')
	])
	.volumes(list_volumes=[
		(
			path_join([CURRENT_DIRECTORY,PROJECT_NAME]),
			path_join([PROJECT_NAME])
		)
	])
	.depends(list_depends=[WEB_CONTAINER_NAME])
	.workdir(work_directory=path_join([PROJECT_NAME]))
	.command(command="bash gulp.sh"))
	# print(node_compose)
############################################################################
					## NGINX CONTAINER OBJECT ##
############################################################################
nginx_compose = Container()
(nginx_compose.name(container_name=NGINX_CONTAINER_NAME)
.image(image_base='nginx')
.restart(restart_option='always')
.volumes(list_volumes=[
	(path_join([CURRENT_DIRECTORY,FOLDER_TO_SAVE,'nginx','nginx.conf']) , "/etc/nginx/nginx.conf"),
	(STATIC_VOLUME,STATIC_ROOT),
	(MEDIA_VOLUME,MEDIA_ROOT),
	(LOGS_VOLUME,LOGS_ROOT)
])
.depends(list_depends=[WEB_CONTAINER_NAME])
.ports(list_ports=[
	(NGINX_PORT,WEB_PORT)
]))
# print(node_compose)
##########################################################################
						## USER CONTAINERS OBJECTS##
###########################################################################
user_containers = []
for index,container_image in enumerate(CONTAINERS):
	temporary_container = Container()
	(temporary_container.name(OTHERS_CONTAINER_NAME[index])
	.image(container_image)
	.restart('always'))
	user_containers.append(temporary_container)
###########################################################################
						## FINAL COMPOSE FILES ##
###########################################################################

filename_development=PROJECT_NAME+'_development'
filename_production=PROJECT_NAME+'_production'

containers_production = [deepcopy(web_compose)]+deepcopy(user_containers) + [nginx_compose]
containers_development = [deepcopy(web_compose)]+deepcopy(user_containers)

if BROWSERSYNC_GULP_DEV_TOOLS:
	containers_development += [node_compose]
if not DATABASE_EXTERNAL:
	containers_development += [deepcopy(database_compose)]
	containers_production += [deepcopy(database_compose)]


service = Service()
(service.version(service_version=DOCKER_COMPOSE_VERSION)
.volumes(list_of_volumes=[DATABASE_VOLUME,MEDIA_VOLUME,STATIC_VOLUME,LOGS_VOLUME])
.networks(list_of_networks=[NETWORK_NAME]))


service_development = deepcopy(service)
service_production = deepcopy(service)


del service

(service_development.containers(list_of_containers=containers_development)
.build()
.save(
	path_to_save=path_join([CURRENT_DIRECTORY,FOLDER_TO_SAVE]),
	filename=filename_development
))
# print(service_development)

(service_production.containers(list_of_containers=containers_production)
.build()
.save(
	path_to_save=path_join([CURRENT_DIRECTORY,FOLDER_TO_SAVE]),
	filename=filename_production
))
# print(service_production)
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