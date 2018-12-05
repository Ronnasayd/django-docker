#! /bin/bash

### VERSION: 2.1.3-beta ###

if [ ! -d "tmp/" ]; then
  mkdir tmp/
fi
wget -q --no-cache https://raw.githubusercontent.com/Ronnasayd/django-docker/master/modules/version -O tmp/version

if ! diff -q tmp/version modules/version > /dev/null 2>&1;
then

  echo -e "you have a update"
  echo -e "do you want update ? (y/n):"
  read -s answer

  if [ "$answer" = "y" ];then
  	echo "updating..."
  	wget -q --no-cache https://github.com/Ronnasayd/django-docker/blob/master/source_code.zip?raw=true -O tmp/source_code.zip
  	unzip -q tmp/source_code.zip -d tmp/
  	rm tmp/source_code.zip
  	cp tmp/pydd.py pydd$(cat tmp/version | awk '{print $3}').py
  	cp tmp/ddo.sh  ddo$(cat tmp/version | awk '{print $3}').sh
  	cp -r tmp/modules modules$(cat tmp/version | awk '{print $3}')
    cp tmp/config.py config$(cat tmp/version | awk '{print $3}').py
  fi


else

  echo "You already update !"

fi

rm -rf tmp/