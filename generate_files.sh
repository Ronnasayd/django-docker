#! /bin/bash

# VERSION: 3.2.8-beta #

rm source_code.zip
rm -rf docs/
zip django_docker -r modules/ pydd.py ddo.sh config.py
wget -m -p -E -k http://localhost:8000/
mv ./localhost:8000 ./docs
sed -i -e 's/index.html//g' docs/index.html