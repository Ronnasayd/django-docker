#! /bin/bash

# VERSION: 3.2.11-beta #

rm -rf snyk
mkdir snyk
cp ./dd_auxfiles/requirements.txt ./snyk
cp ./django_docker_example/package.json ./snyk
rm django_docker.zip
rm -rf docs/
zip django_docker -r modules/ pydd.py ddo.sh config.py
wget -m -p -E -k http://localhost:8000/
mv ./localhost:8000 ./docs
sed -i -e 's/index.html//g' docs/index.html