#! /bin/bash

# VERSION: 3.2.7-beta #

rm source_code.zip
rm -rf docs/
zip source_code -r modules/ pydd.py ddo.sh config.py
wget -m -p -E -k http://localhost:8000/
mv ./localhost:8000 ./docs
sed -i -e 's/index.html//g' docs/index.html