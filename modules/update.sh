#! /bin/bash

# MIT License

# Copyright (c) 2019 Ronnasayd de Sousa Machado

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# VERSION: 3.2.9-beta #

if [ ! -d "tmp/" ]; then
  mkdir tmp/
fi
# wget -q --no-cache https://raw.githubusercontent.com/Ronnasayd/django-docker/master/modules/version -O tmp/version
curl -H 'Cache-Control: no-cache' -s https://raw.githubusercontent.com/Ronnasayd/django-docker/master/modules/version --output tmp/version
if ! diff -q tmp/version modules/version > /dev/null 2>&1;
then

  echo -e "you have a update"
  echo -e "do you want update ? (y/n):"
  read -s answer

  if [ "$answer" = "y" ];then
  	echo "updating..."
  	# wget -q --no-cache https://github.com/Ronnasayd/django-docker/blob/master/source_code.zip?raw=true -O tmp/source_code.zip
  	curl -H 'Cache-Control: no-cache' -s -L https://github.com/Ronnasayd/django-docker/blob/master/django_docker.zip?raw=true --output tmp/source_code.zip
    unzip -q tmp/source_code.zip -d tmp/
  	rm tmp/source_code.zip
  	cp tmp/pydd.py pydd.py
  	cp tmp/ddo.sh  ddo.sh
  	cp -r tmp/modules "$(pwd)"
    cp tmp/config.py config$(cat tmp/version | awk '{print $3}').py
  fi


else

  echo "You already update !"

fi

rm -rf tmp/