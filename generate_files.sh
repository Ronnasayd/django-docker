#! /bin/bash

# VERSION: 3.2.4-beta #

zip source_code -r modules/ pydd.py ddo.sh config.py
wget -m -p -E -k http://localhost:8000/
mv ./localhost:8000 ./docs
sed -i -e 's/index.html//g' docs/index.html