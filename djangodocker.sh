#! /bin/bash
if [ "$#" -lt 1 ] ; then
	echo "Number of arguments insufficient. Use <$0 --help> to see options"
	exit
fi
if [ "$1" = "--help" -o "$1" = "-h" ];then
	echo -e "Use: $0 <options> <complements>
Options:
	--help, -h : Show help
	--run,	-r : Mode of execution
	--make, -m : Enviroment creation mode
	--clear,-c : Delete generated files
	--clear-all,-ca : Delete all files
	--stop, -s : Stop a specific container
	--stop-all, -sa : Stop containers
	--stop-net, -sn : Stop all containers off a network
	--shell, -sl : Enter container shell
	--status, -st : Show the status of containers
	--command, -cm : Performs a command inside the container
	--net-status, -ns: Show all networks
	--create-su, -csu: Create a new admin user
	--migrate, -mi: Apply migrations in django 
	--clear-mig, -cmi: Clear all migrations and __pycache__ folders
	--show-db, -sdb: Show datbases create with django docker
	--clear-db, -cdb: Clear a specific database create with django docker
	--prune, -p: Prune the system
	--show-img, -si: Show the docker images
	--clear-img, -ci: Clear a specific docker image for image_id
	--attach, -att: Attach to a runing dev ambient

Examples:
	$0 --run
	$0 --make
	$0 --clear
	$0 --clear-all
	$0 --stop web
	$0 --stop-all
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
	"

elif [ "$1" = "--make" -o "$1" = "-m" ];then
	unameOut="$(uname -s)"
	case "${unameOut}" in
	    Linux*)     machine=Linux && python3 djangodocker.py;;
	    Darwin*)    machine=Mac && python3 djangodocker.py;;
	    CYGWIN*)    machine=Cygwin && python djangodocker.py;;
	    MINGW*)     machine=MinGw && python djangodocker.py;;
	    *)          machine="UNKNOWN:${unameOut}"
	esac
	echo "Ambiente: "${machine}" Arquivos criados"
elif [ "$1" = "--run" -o "$1" = "-r" ];then
	echo "Executing..."
	bash djd_data/make_ambient.sh
elif [ "$1" = "--stop-all" -o "$1" = "-sa" ];then
	docker stop $(docker ps -a -q)
	docker system prune --force
	echo "Containers stopped"
elif [ "$1" = "--stop" -o "$1" = "-s" ];then
	docker stop $2
	docker system prune --force
	echo "Container stopped"
elif [ "$1" = "--shell" -o "$1" = "-sl" ];then
	echo "Use exit to close"
	docker exec -ti $2 /bin/bash
elif [ "$1" = "--command" -o "$1" = "-c" ];then
	echo "Use exit to close"
	docker exec -ti $2 $3
elif [ "$1" = "--create-su" -o "$1" = "-csu" ];then
	docker exec -ti web python manage.py createsuperuser
elif [ "$1" = "--migrate" -o "$1" = "-mi" ];then
	docker exec -ti web python manage.py makemigrations $2
	docker exec -ti web python manage.py migrate $2
elif [ "$1" = "--status" -o "$1" = "-st" ];then
	docker ps
elif [ "$1" = "--show-db" -o "$1" = "-sdb" ];then
	docker volume ls | grep database | awk '{print $2}'
elif [ "$1" = "--clear-db" -o "$1" = "-cdb" ];then
	docker volume rm $2
elif [ "$1" = "--clear" -o "$1" = "-c" ];then
	rm -rf ./__pycache__ ./djd_data
	echo "Enviroment cleaned"
elif [ "$1" = "--clear-all" -o "$1" = "-ca" ];then
	rm -rf ./logs ./media ./__pycache__ ./static ./djd_data
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
elif [ "$1" = "--clear-img" -o "$1" = "-ci" ];then
	docker rmi $2
elif [ "$1" = "--attach" -o "$1" = "-att" ];then
	COMPOSE_HTTP_TIMEOUT=3600 docker-compose -f $(ls *development.yml) up
else 
	echo "Unrecognized argument in command list. Use <$0 --help> to see options"
fi


