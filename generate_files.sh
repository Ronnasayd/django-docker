#! /bin/bash

# VERSION: 4.1.4-beta #


rm -rf snyk
mkdir snyk
cp ./django_docker_example/package.json ./snyk
cp ./django_docker_example/requirements.txt ./snyk
rm django_docker.zip
rm -rf docs/
zip django_docker -r modules/ pydd.py ddo.sh config.py
wget -m -p -E -k http://localhost/
mv ./localhost ./docs
sed -i -e 's/index.html//g' docs/index.html
coverage run pydd.py
coverage xml
export CODACY_PROJECT_TOKEN=493db568a4594312846b4f614f054705
python-codacy-coverage -r coverage.xml
python ddotests.py