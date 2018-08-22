#! /bin/bash
if [ "$1" = "--help" -o "$1" = "-h" ];then
	echo "Modo Execução: $0 --run"
	echo "Modo Criação de Ambiente: $0 --make"
fi


if [ "$1" = "--make" ];then
 	echo "Criando Ambiente"
 	python3 djangodocker.py
fi

if [ "$1" = "--run" ];then
	echo "Executando"
	bash make_ambient.sh
fi
