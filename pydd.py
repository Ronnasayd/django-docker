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

# VERSION: 3.2.9-beta #

import os
import config 
from copy import deepcopy
from modules import dockerfile
from modules import compose
from modules import controller
from modules import functional
from modules import constants

if __name__ == '__main__':
	CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
	CURRENT_DIRECTORY = CURRENT_DIRECTORY.replace('\\', '/')

#############################################################################	
						## NODE DOCKERFILE OBJECT ##
#############################################################################
	node_dockerfile = dockerfile.Dockerfile()
	(node_dockerfile._from(container_base='node')
	.run(list_of_commands=[
	'apt-get update',
	'yarn global add --no-bin-links gulp-cli',
	'yarn global add --no-bin-links browser-sync',
	'mkdir ' + config.PROJECT_NAME,
	])
	.workdir(work_directory=functional.path_join([config.PROJECT_NAME]))
	.user(container_user='node')
	.save(
		path_to_save=functional.path_join([CURRENT_DIRECTORY, config.FOLDER_TO_SAVE]),
		filename='node'
	))
#############################################################################
						## WEB DOCKERFILE OBJECT ##
#############################################################################
	web_dockerfile = dockerfile.Dockerfile()
	(web_dockerfile._from(container_base='python:'+config.PYTHON_VERSION)
	.add(
		local_path=functional.path_join([config.FOLDER_TO_SAVE, 'requirements.txt']),
		container_path=functional.path_join([constants.ROOT_DIRECTORY, 'requirements.txt'])
	)
	.run(list_of_commands=[
		'apt-get update',
		'pip install --upgrade pip',
		'pip install -r requirements.txt',
	]+config.WEB_COMMANDS_BUILD)
	.add(
		local_path=functional.path_join([constants.ROOT_DIRECTORY, config.PROJECT_NAME]),
		container_path=functional.path_join([config.PROJECT_NAME])
	)
	.workdir(work_directory=functional.path_join([config.PROJECT_NAME]))
	.save(
		path_to_save=functional.path_join([CURRENT_DIRECTORY, config.FOLDER_TO_SAVE]),
		filename='web'
	))
###########################################################################	
						## WEB CONTAINER OBJECT ##
###########################################################################
	web_compose = compose.Container()
	(web_compose.name(container_name=constants.WEB_CONTAINER_NAME)
	.build(
		context=CURRENT_DIRECTORY,
	 	dockerfile=functional.path_join([config.FOLDER_TO_SAVE, web_dockerfile.filename])
	 )
	.restart(restart_option='always')
	.ports(list_ports=[
		(config.WEB_PORT, config.WEB_PORT),
	])\
	.expose(list_expose_ports=[config.WEB_PORT])
	.workdir(work_directory=functional.path_join([config.PROJECT_NAME]))
	.command(command='./wait-for-it.sh '+(config.DATABASE_DEFAULT_ENVIROMENTS['DATABASE_HOST'] if config.DATABASE_EXTERNAL else constants.DATABASE_CONTAINER_NAME)+':'+config.DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PORT']+' --timeout=15 --strict -- /bin/bash runserver.sh')
	.depends(list_depends=constants.OTHERS_CONTAINER_NAME if config.DATABASE_EXTERNAL else [constants.DATABASE_CONTAINER_NAME]+constants.OTHERS_CONTAINER_NAME)
	.environ(list_enviroments=[
     ('DEBUG',str(config.DEBUG)),
     ('STATIC_ROOT',constants.STATIC_ROOT),
     ('STATIC_URL','/static/'),
     ('MEDIA_ROOT',constants.MEDIA_ROOT),
     ('MEDIA_URL','/media/'),
     ('DATABASE_ENGINE',config.DATABASE_ENGINE),
     ('DATABASE_USER',config.DATABASE_DEFAULT_ENVIROMENTS['DATABASE_USER']),
     ('DATABASE_NAME',config.DATABASE_DEFAULT_ENVIROMENTS['DATABASE_DB']),
     ('DATABASE_HOST',(config.DATABASE_DEFAULT_ENVIROMENTS['DATABASE_HOST'] if config.DATABASE_EXTERNAL else constants.DATABASE_CONTAINER_NAME)),
     ('DATABASE_PORT',config.DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PORT']),
     ('DATABASE_PASSWORD',config.DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PASSWORD']),
	]+functional.json2list(config.WEB_ENVIROMENT))
	.volumes(list_volumes=[
		(
			functional.path_join([CURRENT_DIRECTORY,config.PROJECT_NAME]),
			functional.path_join([config.PROJECT_NAME])
		), 
        (
        	constants.MEDIA_VOLUME,
        	functional.path_join([constants.MEDIA_ROOT])
        )
    ] if config.DEBUG else [
    	(
    		constants.MEDIA_VOLUME,
    		functional.path_join([constants.MEDIA_ROOT])
    	),
    	(
    		constants.STATIC_VOLUME,
    		functional.path_join([constants.STATIC_ROOT])
    	)
    ]))
	# print(web_compose)
###########################################################################
					## DATABASE CONTAINER OBJECT ##
###########################################################################
	database_compose = compose.Container()
	(database_compose.name(container_name=constants.DATABASE_CONTAINER_NAME)
	.image(image_base=config.DATABASE_IMAGE)
	.restart(restart_option='always')
	.volumes(list_volumes=[
		(constants.DATABASE_VOLUME,config.DATABASE_ROOT['DESTINATION'])
	])
	.environ([
		(config.DATABASE_DEFAULT_ENVIROMENTS['DATABASE_USER_NAME'],config.DATABASE_DEFAULT_ENVIROMENTS['DATABASE_USER']),
		(config.DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PASSWORD_NAME'],config.DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PASSWORD']),
		(config.DATABASE_DEFAULT_ENVIROMENTS['DATABASE_DB_NAME'],config.DATABASE_DEFAULT_ENVIROMENTS['DATABASE_DB']),
	]+functional.json2list(config.DATABASE_OTHERS_ENVIROMENTS))
	)
	if config.DEBUG:
		database_compose.ports(list_ports=[(config.DATABASE_EXTERNAL_PORT,config.DATABASE_DEFAULT_ENVIROMENTS['DATABASE_PORT'])])
	# print(database_compose)
###########################################################################
					## NODE CONTAINER OBJECT ##
###########################################################################
	node_compose = compose.Container()
	(node_compose.name(container_name=constants.NODE_CONTAINER_NAME)
	.build(
		context=CURRENT_DIRECTORY,
	 	dockerfile=functional.path_join([config.FOLDER_TO_SAVE,node_dockerfile.filename])
	 )
	.restart(restart_option="always")
	.ports(list_ports=[
		('3000','3000'),
		('3001','3001'),
		('3002','3002')
	])
	.volumes(list_volumes=[
		(
			functional.path_join([CURRENT_DIRECTORY,config.PROJECT_NAME]),
			functional.path_join([config.PROJECT_NAME])
		)
	])
	.depends(list_depends=[constants.WEB_CONTAINER_NAME])
	.workdir(work_directory=functional.path_join([config.PROJECT_NAME]))
	.command(command="bash gulp.sh"))
	# print(node_compose)
############################################################################
					## NGINX CONTAINER OBJECT ##
############################################################################
	nginx_compose = compose.Container()
	(nginx_compose.name(container_name=constants.NGINX_CONTAINER_NAME)
	.image(image_base='nginx')
	.restart(restart_option='always')
	.volumes(list_volumes=[
		(functional.path_join([CURRENT_DIRECTORY,config.FOLDER_TO_SAVE,'nginx','nginx.conf']) , "/etc/nginx/nginx.conf"),
		(constants.STATIC_VOLUME,constants.STATIC_ROOT),
		(constants.MEDIA_VOLUME,constants.MEDIA_ROOT),
		(constants.LOGS_VOLUME,constants.LOGS_ROOT)
	])
	.depends(list_depends=[constants.WEB_CONTAINER_NAME])
	.ports(list_ports=[
		(config.NGINX_PORT,config.WEB_PORT)
	]))
# print(node_compose)
##########################################################################
						## USER CONTAINERS OBJECTS##
###########################################################################
	user_containers = []
	for index,container_image in enumerate(config.CONTAINERS):
		temporary_container = compose.Container()
		(temporary_container.name(constants.OTHERS_CONTAINER_NAME[index])
		.image(container_image)
		.restart('always'))
		user_containers.append(temporary_container)
###########################################################################
						## FINAL COMPOSE FILES ##
###########################################################################

	filename_development=config.PROJECT_NAME+'_development'
	filename_production=config.PROJECT_NAME+'_production'

	containers_production = [deepcopy(web_compose)]+deepcopy(user_containers) + [nginx_compose]
	containers_development = [deepcopy(web_compose)]+deepcopy(user_containers)

	if config.FRONT_DEV_TOOLS:
		containers_development += [node_compose]
	if not config.DATABASE_EXTERNAL:
		containers_development += [deepcopy(database_compose)]
		containers_production += [deepcopy(database_compose)]


	service = compose.Service()
	(service.version(service_version=config.DOCKER_COMPOSE_VERSION)
	.volumes(list_of_volumes=[constants.DATABASE_VOLUME,constants.MEDIA_VOLUME,constants.STATIC_VOLUME,constants.LOGS_VOLUME])
	.networks(list_of_networks=[config.NETWORK_NAME]))


	service_development = deepcopy(service)
	service_production = deepcopy(service)


	del service

	(service_development.containers(list_of_containers=containers_development)
	.build()
	.save(
		path_to_save=functional.path_join([CURRENT_DIRECTORY,config.FOLDER_TO_SAVE]),
		filename=filename_development
	))
	# print(service_development)

	(service_production.containers(list_of_containers=containers_production)
	.build()
	.save(
		path_to_save=functional.path_join([CURRENT_DIRECTORY,config.FOLDER_TO_SAVE]),
		filename=filename_production
	))
	# print(service_production)
	########################################################################
						## MVC GENERATED FILES ##
	########################################################################

	pycontroller = controller.Controller()

	nginx_content = pycontroller.build_nginx()
	gulpfile_content = pycontroller.build_gulpfile()
	make_ambient_content = pycontroller.build_make_ambiente(debug_mode=config.DEBUG)
	runserver_content = pycontroller.build_runserver(debug_mode=config.DEBUG)
	requirements_content = pycontroller.build_requirements()
	gulp_script_content = pycontroller.build_gulp_script()
	wait_for_it_content = pycontroller.build_wait_for_it()
	settings = pycontroller.build_settings()
	manage = pycontroller.build_manage()



	functional.save(functional.path_join([CURRENT_DIRECTORY,config.FOLDER_TO_SAVE,'nginx']),'nginx.conf',nginx_content)
	functional.save(functional.path_join([CURRENT_DIRECTORY,config.FOLDER_TO_SAVE]),'gulpfile.js',gulpfile_content)
	functional.save(functional.path_join([CURRENT_DIRECTORY,config.FOLDER_TO_SAVE]),'make_ambient.sh',make_ambient_content)
	functional.save(functional.path_join([CURRENT_DIRECTORY,config.FOLDER_TO_SAVE]),constants.RUNSERVER_SCRIPT_NAME,runserver_content)
	functional.save(functional.path_join([CURRENT_DIRECTORY,config.FOLDER_TO_SAVE]),'requirements.txt',requirements_content)
	functional.save(functional.path_join([CURRENT_DIRECTORY,config.FOLDER_TO_SAVE]),'gulp.sh',gulp_script_content)
	functional.save(functional.path_join([CURRENT_DIRECTORY,config.FOLDER_TO_SAVE]),'wait-for-it.sh',wait_for_it_content)
	functional.save(functional.path_join([CURRENT_DIRECTORY,config.FOLDER_TO_SAVE]),constants.SETTINGS_FILE_NAME+'.py',settings)
	functional.save(functional.path_join([CURRENT_DIRECTORY,config.FOLDER_TO_SAVE]),'manage.py',manage)
