#! /bin/bash

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

### VERSION: 3.1.1-beta ###

PROJECT_RENAME=$(cat config.py | grep PROJECT_NAME | awk '{split($0,a,"="); print a[2]}'| sed -e 's/"//g' | sed -e "s/'//g" | sed -e "s/_/./g")
FOLDER_TO_SAVE=$(cat config.py | grep FOLDER_TO_SAVE | awk '{split($0,a,"="); print a[2]}'| sed -e 's/"//g' | sed -e "s/'//g")
PROJECT_NAME=$(cat config.py | grep PROJECT_NAME | awk '{split($0,a,"="); print a[2]}'| sed -e 's/"//g' | sed -e "s/'//g")


if [ "$#" -lt 1 ] ; then
  echo "Number of arguments insufficient. Use <$0 --help> to see options"
  exit
fi
if [ "$1" = "--help" -o "$1" = "-h" ];then
  echo -e "Use: $0 <options> <complements>

Options:
  --help                      or    -h       : Show help
  --run                       or    -r       : Mode of execution
  --make                      or    -m       : Enviroment creation mode
  --clear                     or    -c       : Delete generated files
  --clear-all                 or    -ca      : Delete all files
  --stop                      or    -s       : Stop a specific container
  --stop-app                  or    -sap     : Stop containers in app network
  --stop-net                  or    -sn      : Stop all containers off a network
  --stop-all                  or    -sal     : Stop all containers running on docker
  --shell                     or    -sl      : Enter container shell
  --status                    or    -st      : Show the status of containers
  --command                   or    -cm      : Performs a command inside the container
  --net-status                or    -ns      : Show all networks
  --create-su                 or    -csu     : Create a new admin user
  --migrate                   or    -mi      : Apply migrations in django 
  --clear-mig                 or    -cmi     : Clear all migrations and __pycache__ folders
  --show-db                   or    -sdb     : Show datbases create with django docker
  --clear-db                  or    -cdb     : Clear a specific database create with django docker
  --prune                     or    -p       : Prune the system
  --show-img                  or    -si      : Show the docker images
  --clear-img                 or    -ci      : Clear a specific docker image for image_id
  --attach                    or    -att     : Attach to a runing dev ambient
  --restart                   or    -res     : Restart a container
  --minify-img                or    -mimg    : Minify images in selected folder
  --update                    or    -up      : Update django docker
  --show-vol                  or    -sv      : Show all volumes
  --clear-vol                 or    -cv      : Clear a volume
  --django-create-project     or    -dcp     : Create a django project 
  --django-create-app         or    -dca     : Create a django app in a django project
  --dbeaver                   or    -dbv      : Run a container with Dbeaver database manager (Just in LINUX)


Examples:
  $0 --run
  $0 --make
  $0 --clear
  $0 --clear-all
  $0 --stop web
  $0 --stop-app
  $0 --stop-net network_example
  $0 --shell web
  $0 --status
  $0 --net-status
  $0 --command web 'python manage.py migrate'
  $0 --create-su
  $0 --migrate # migrate in all models
  $0 --migrate django_docker_app # migrate specific model
  $0 --clear-mig
  $0 --show-db
  $0 --clear-db djangodocker_database
  $0 --prune
  $0 --show-img
  $0 --clear-img 627c27fc5060
  $0 --attach
  $0 --restart web
  $0 --minify-img
  $0 --update
  $0 --show-vol
  $0 --stop-all
  $0 --django-create-project django_docker_example
  $0 --django-create-app django_docker_example api
  $0 --dbeaver 

  "

elif [ "$1" = "--make" -o "$1" = "-m" ];then
  unameOut="$(uname -s)"
  case "${unameOut}" in
      Linux*)     machine=Linux && python3 ./pydd.py;;
      Darwin*)    machine=Mac && python3 ./pydd.py;;
      CYGWIN*)    machine=Cygwin && python ./pydd.py;;
      MINGW*)     machine=MinGw && python ./pydd.py;;
      *)          machine="UNKNOWN:${unameOut}"
  esac
  echo "Ambiente: "${machine}" Arquivos criados"
elif [ "$1" = "--run" -o "$1" = "-r" ];then
  echo "Executing..."
  bash $FOLDER_TO_SAVE/make_ambient.sh
elif [ "$1" = "--stop-app" -o "$1" = "-sap" ];then
  docker-compose -f $(ls $FOLDER_TO_SAVE/*development.yml) stop
  docker-compose -f $(ls $FOLDER_TO_SAVE/*production.yml) stop
  docker system prune --force
  echo "Containers stopped"
elif [ "$1" = "--stop" -o "$1" = "-s" ];then
  docker stop $2
  docker system prune --force
  echo "Container stopped"
elif [ "$1" = "--stop-all" -o "$1" = "-sal" ];then
  docker stop $(docker ps -aq)
  docker system prune --force
  echo "Containers stopped"
elif [ "$1" = "--shell" -o "$1" = "-sl" ];then
  echo "Use exit to close"
  docker exec -ti $2 /bin/bash
elif [ "$1" = "--command" -o "$1" = "-c" ];then
  echo "Use exit to close"
  docker exec -ti $2 $3
elif [ "$1" = "--create-su" -o "$1" = "-csu" ];then
  docker exec -ti web.$PROJECT_RENAME python manage.py createsuperuser
elif [ "$1" = "--minify-img" -o "$1" = "-mimg" ];then
  docker exec -ti node.$PROJECT_RENAME gulp imagemin
elif [ "$1" = "--migrate" -o "$1" = "-mi" ];then
  docker exec -ti web.$PROJECT_RENAME python manage.py makemigrations $2
  docker exec -ti web.$PROJECT_RENAME python manage.py migrate $2
elif [ "$1" = "--status" -o "$1" = "-st" ];then
  docker ps
elif [ "$1" = "--show-db" -o "$1" = "-sdb" ];then
  docker volume ls | grep database_$PROJECT_NAME | awk '{print $2}'
elif [ "$1" = "--show-vol" -o "$1" = "-sv" ];then
  docker volume ls | grep _$PROJECT_NAME | awk '{print $2}'
elif [ "$1" = "--clear-db" -o "$1" = "-cdb" ];then
  docker volume rm $(docker volume ls | grep database_$PROJECT_NAME | awk '{print $2}')
elif [ "$1" = "--clear-vol" -o "$1" = "-cv" ];then
  docker volume rm $2
elif [ "$1" = "--clear" -o "$1" = "-c" ];then
  rm -rf ./logs ./media ./__pycache__ ./static ./$FOLDER_TO_SAVE
  echo "Enviroment cleaned"
elif [ "$1" = "--clear-all" -o "$1" = "-ca" ];then
  rm -rf ./logs ./media ./__pycache__ ./static ./$FOLDER_TO_SAVE
  rm -rf $(find . -name '__pycache__')
  rm -rf $(find . -name 'migrations')
  rm -rf $(find . -name 'node_modules')
  rm -rf $(find . -name 'runserver.sh')
  rm -rf $(find . -name 'gulp.sh')
  rm -rf $(find . -name 'gulpfile.js')
  rm -rf $(find . -name 'package.json')
  rm -rf $(find . -name 'yarn.lock')
  rm -rf $(find . -name 'yarn-error.log')
  rm -rf $(find . -name 'wait-for-it.sh')
  docker volume rm $(docker volume ls | grep static_$PROJECT_NAME | awk '{print $2}')
  docker volume rm $(docker volume ls | grep media_$PROJECT_NAME | awk '{print $2}')
  docker volume rm $(docker volume ls | grep logs_$PROJECT_NAME | awk '{print $2}')
  echo "Enviroment cleaned"
elif [ "$1" = "--clear-mig" -o "$1" = "-cmi" ];then
  rm -rf $(find . -name '__pycache__')
  rm -rf $(find . -name 'migrations')
  echo "Migrations cleaned"
elif [ "$1" = "--stop-net" -o "$1" = "-sn" ];then
  docker stop $(docker network inspect $2 | grep Name | grep -v network | awk '{sub("\",","",$2);sub("\"","",$2);print $2}')
  echo "Network containers stoped"
elif [ "$1" = "--net-status" -o "$1" = "-ns" ];then
  docker network ls
elif [ "$1" = "--prune" -o "$1" = "-p" ];then
  docker system prune --force
elif [ "$1" = "--show-img" -o "$1" = "-si" ];then
  docker images
elif [ "$1" = "--update" -o "$1" = "-up" ];then
  bash modules/update.sh
elif [ "$1" = "--clear-img" -o "$1" = "-ci" ];then
  docker rmi -f $2
elif [ "$1" = "--restart" -o "$1" = "-res" ];then
  docker container restart $2
elif [ "$1" = "--django-create-project" -o "$1" = "-dcp" ];then
  django-admin startproject $2
elif [ "$1" = "--django-create-app" -o "$1" = "-dca" ];then
  cd ./$2
  unameOut="$(uname -s)"
  case "${unameOut}" in
      Linux*)     machine=Linux && python3 manage.py startapp $3;;
      Darwin*)    machine=Mac && python3 manage.py startapp $3;;
      CYGWIN*)    machine=Cygwin && python manage.py startapp $3;;
      MINGW*)     machine=MinGw && python manage.py startapp $3;;
      *)          machine="UNKNOWN:${unameOut}"
  esac
  cd ..
elif [ "$1" = "--attach" -o "$1" = "-att" ];then
  COMPOSE_HTTP_TIMEOUT=3600 docker-compose -f $(ls $FOLDER_TO_SAVE/*development.yml) up
elif [ "$1" = "--dbeaver" -o "$1" = "-dbv" ];then
  bash modules/dbeaver/dbeaver.sh
else 
  echo "Unrecognized argument in command list. Use <$0 --help> to see options"
fi


