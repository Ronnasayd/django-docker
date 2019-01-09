#! /bin/bash

### VERSION: 2.2.2-beta ###

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
  	curl -H 'Cache-Control: no-cache' -s -L https://github.com/Ronnasayd/django-docker/blob/master/source_code.zip?raw=true --output tmp/source_code.zip
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