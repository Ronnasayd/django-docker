﻿<p  align="center"><img  src="django-docker.png"  alt="django-docker"  width="200"/></p>

# Django-Docker CLI
[https://ronnasayd.github.io/django-docker/](https://ronnasayd.github.io/django-docker/)

[![code quality](https://img.shields.io/codacy/grade/ff5a4f4521cd4d9a8c8e85214a29f5b1.svg)](https://app.codacy.com/project/Ronnasayd/django-docker/dashboard)	[![build](https://travis-ci.org/Ronnasayd/django-docker.svg?branch=master)](https://travis-ci.org/Ronnasayd/django-docker)	[![Known Vulnerabilities](https://snyk.io/test/github/Ronnasayd/django-docker/badge.svg?targetFile=snyk%2Frequirements.txt)](https://snyk.io/test/github/Ronnasayd/django-docker?targetFile=snyk%2Frequirements.txt)	[![coverage](https://api.codacy.com/project/badge/Coverage/ff5a4f4521cd4d9a8c8e85214a29f5b1)](https://www.codacy.com/app/Ronnasayd/django-docker?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Ronnasayd/django-docker&amp;utm_campaign=Badge_Coverage)	[![license](https://img.shields.io/github/license/ronnasayd/django-docker.svg)](LICENSE.md)	![code s](https://img.shields.io/github/languages/code-size/ronnasayd/django-docker.svg)	[![releases](https://img.shields.io/github/release-pre/ronnasayd/django-docker.svg)](https://github.com/Ronnasayd/django-docker/releases)	[![releases date](https://img.shields.io/github/release-date-pre/ronnasayd/django-docker.svg)](https://github.com/Ronnasayd/django-docker/releases)	[![issues closed](https://img.shields.io/github/issues-closed-raw/ronnasayd/django-docker.svg)](https://github.com/Ronnasayd/django-docker/issues?q=is%3Aissue+is%3Aclosed)	[![last-commit](https://img.shields.io/github/last-commit/ronnasayd/django-docker.svg)](https://github.com/Ronnasayd/django-docker/commits/master)	![python](https://img.shields.io/badge/language-python-blue.svg)	[![social](https://img.shields.io/github/stars/ronnasayd/django-docker.svg?style=social)](https://github.com/Ronnasayd/django-docker/stargazers)

System to automatically create development and production environments in django with docker and facilitate the development of applications.

## Required Programs
- [Python](https://www.python.org/) version 3 or higher
- [Docker](https://www.docker.com/)
- [Docker compose](https://docs.docker.com/compose/)

## Installation
**Linux:**

    sudo apt-get install python3.6
    sudo apt-get install docker.io
    sudo apt-get install docker-compose
    sudo groupadd docker
    sudo usermod -aG docker $USER
    
> Log out and log back in so that your group membership is re-evaluated.

**Windows:**

> Download and install the binaries of [python](https://www.python.org/downloads/) and [docker toolbox](https://docs.docker.com/toolbox/toolbox_install_windows/)

## How to use

The files *config.py*, *pydd.py*, *ddo.sh*  and the folder *modules* should be in the same directory of your django project.

Modify the *config.py* settings as you wish, and then run the *ddo.sh* script with a desirable argument. 

**Variables in config.py:**

*DEBUG (boolean):*	
> when False determines the mode of development and when True mode of production
> 
 *FRONT_DEV_TOOLS (boolean):*   
> when True enables front-end helper tools like gulp and browsersync

 *REQUIREMENTS (List[str]):*
>   list with the python modules to be installed

*PROJECT_NAME (str):*
> the name of your django project

*PYTHON_VERSION (str):*
> python version in the container that will run django

*DJANGO_VERSION (str):*
  > version of Django
  
*WEB_COMMANDS_BUILD (List[str]):*
>  list of shell commands to be added to the container in build

 **Make enviroment:**

    bash ddo.sh --make

 **Run enviroment:**

    bash ddo.sh --run

## List of commands
| Argument |Abbreviation  |Explanation|
|--|--|--|
 --help                     |      -h       | Show help
  --run                      |      -r       | Run the application in selected mode
  --make                     |      -m       | Enviroment creation mode
  --clear                    |      -c       | Delete generated files
  --clear-all                |      -ca      | Delete all files
  --stop                     |      -s       | Stop a specific container
  --stop-app                 |      -sap     | Stop containers in app network
  --stop-net                 |      -sn      | Stop all containers off a network
  --stop-all                 |      -sal     | Stop all containers running on docker
  --shell                    |      -sl      | Enter container shell
  --status                   |      -st      | Show the status of containers
  --command                  |      -cm      | Performs a command inside the container
  --net-status               |      -ns      | Show all networks
  --create-su                |      -csu     | Create a new admin user
  --migrate                  |      -mi      | Apply migrations in django 
  --clear-mig                |      -cmi     | Clear all migrations and __pycache__ folders
  --show-db                  |      -sdb     | Show datbases create with django docker
  --clear-db                 |      -cdb     | Clear a specific database create with django docker
  --prune                    |      -p       | Prune the system
  --show-img                 |      -si      | Show the docker images
  --clear-img                |      -ci      | Clear a specific docker image for image_id
  --attach                   |      -att     | Attach to a running ambient
  --restart                  |      -res     | Restart a container
  --update                   |      -up      | Update django docker
  --show-vol                 |      -sv      | Show all volumes
  --clear-vol                |      -cv      | Clear a volume
  --django-create-project    |      -dcp     | Create a django project 
  --django-create-app        |      -dca     | Create a django app in a django project
  --dbeaver                  |      -dbv     | Run a container with Dbeaver database manager (Just in LINUX yet)
  --portainer                |      -ptn     | Run a container with portainer gui manager for docker 


  
## Contributing
1. Fork it ([https://github.com/Ronnasayd/django-docker/fork](https://github.com/Ronnasayd/django-docker))
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details