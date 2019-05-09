#! /bin/bash

# VERSION: 4.1.0-beta #


rm -rf snyk
mkdir snyk
cp ./django_docker_example/package.json ./snyk
cp ./django_docker_example/requiriments.txt ./snyk
rm django_docker.zip
rm -rf docs/
zip django_docker -r modules/ pydd.py ddo.sh config.py
wget -m -p -E -k http://localhost/
mv ./localhost ./docs
sed -i -e 's/index.html//g' docs/index.html
python ddotests.py