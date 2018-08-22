#! /bin/bash
if [ "$1" = "--help" -o "$1" = "-h" ];then
	echo "Modo Execução: $0 --run"
	echo "Modo Criação de Ambiente: $0 --make"
	echo "Limpar arquivos: $0 --clear"
fi


if [ "$1" = "--make" ];then
	if  echo $(uname -a | grep "Linux") > /dev/null ; then
 		python3 djangodocker.py
 	else
 		python djangodocker.py
 	fi
 	echo "Ambiente criado"
fi

if [ "$1" = "--run" ];then
	echo "Executando"
	bash make_ambient.sh
fi

if [ "$1" = "--clear" ];then
	sudo rm -r ./databases ./logs ./media ./nginx ./__pycache__ ./static ./*.Dockerfile ./*.yml ./make_ambient.sh ./runserver.sh ./requirements.txt
	echo "Ambiente limpo"
fi

