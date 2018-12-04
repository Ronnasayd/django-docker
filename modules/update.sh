if [ ! -d "tmp/" ]; then
  mkdir tmp/
fi
wget https://raw.githubusercontent.com/Ronnasayd/django-docker/master/modules/version -O tmp/version.txt

if ! diff -q tmp/version.txt modules/version.txt > /dev/null 2>&1;
then

  echo "Files are changed"

else

  echo "Files not changed"

fi

rm -rf tmp/