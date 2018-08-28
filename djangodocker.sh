#! /bin/bash
if [ "$1" = "--help" -o "$1" = "-h" ];then
	echo "Modo Execução: $0 --run"
	echo "Modo Criação de Ambiente: $0 --make"
	echo "Limpar arquivos: $0 --clear"
	echo "Limpar containers: $0 --stop"
fi


if [ "$1" = "--make" ];then
	unameOut="$(uname -s)"
	case "${unameOut}" in
	    Linux*)     machine=Linux && python3 djangodocker.py;;
	    Darwin*)    machine=Mac && python3 djangodocker.py;;
	    CYGWIN*)    machine=Cygwin && python djangodocker.py;;
	    MINGW*)     machine=MinGw && python djangodocker.py;;
	    *)          machine="UNKNOWN:${unameOut}"
	esac
	echo "Ambiente: "${machine}
fi

if [ "$1" = "--run" ];then
	echo "Executando"
	bash make_ambient.sh
fi

if [ "$1" = "--stop" ];then
	docker stop $(docker ps -a -q)
	docker system prune -f
	echo "Containers limpos"
fi

if [ "$1" = "--clear" ];then
	sudo rm -r ./databases ./logs ./media ./nginx ./__pycache__ ./static ./*.Dockerfile ./*.yml ./make_ambient.sh ./runserver.sh ./requirements.txt
	echo "Ambiente limpo"
fi

