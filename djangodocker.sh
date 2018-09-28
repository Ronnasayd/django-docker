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

Examples:
	$0 --run
	$0 --make
	$0 --clear
	$0 --stop web
	$0 --stop-all
	$0 --stop-net network_example
	$0 --shell web
	$0 --status
	$0 --net-status
	$0 --command web 'python manage.py migrate'"

elif [ "$1" = "--make" -o "$1" = "-m" ];then
	unameOut="$(uname -s)"
	case "${unameOut}" in
	    Linux*)     machine=Linux && python3 djangodocker.py;;
	    Darwin*)    machine=Mac && python3 djangodocker.py;;
	    CYGWIN*)    machine=Cygwin && python djangodocker.py;;
	    MINGW*)     machine=MinGw && python djangodocker.py;;
	    *)          machine="UNKNOWN:${unameOut}"
	esac
	echo "Ambiente: "${machine}
elif [ "$1" = "--run" -o "$1" = "-r" ];then
	echo "Executing..."
	bash make_ambient.sh
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
elif [ "$1" = "--status" -o "$1" = "-st" ];then
	docker ps
elif [ "$1" = "--clear" -o "$1" = "-c" ];then
	sudo rm -r ./__pycache__ ./*.Dockerfile ./*.yml ./make_ambient.sh ./runserver.sh ./requirements.txt
	echo "Enviroment cleaned"
elif [ "$1" = "--clear-all" -o "$1" = "-ca" ];then
	sudo rm -r ./databases ./logs ./media ./nginx ./__pycache__ ./static ./*.Dockerfile ./*.yml ./make_ambient.sh ./runserver.sh ./requirements.txt
	echo "Enviroment cleaned"
elif [ "$1" = "--stop-net" -o "$1" = "-sn" ];then
	docker stop $(docker network inspect $2 | grep Name | grep -v network | awk '{sub("\",","",$2);sub("\"","",$2);print $2}')
	echo "Network containers stoped"
elif [ "$1" = "--net-status" -o "$1" = "-ns" ];then
	docker network ls
else 
	echo "Unrecognized argument in command list. Use <$0 --help> to see options"
fi

