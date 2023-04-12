#/bin/bash

echo "BUILD START BOSS DARIUS"
python3 -m pip install --upgrade setuptools
python3.11 manage.py collectstatic --noinput
python3.11 -m pip install configparser
python3.11 -m pip install -r requirements.txt
python3.11 -m pip install daphne
python3.11 -m pip install Django
python3.11 -m pip install djangorestframework-simplejwt
python3.11 -m pip install django-cors-headers
python3.11 -m pip install django-cloudinary-storage
python3.11 -m pip install cloudinary
python3.11 -m pip install django_extensions
python3.11 -m pip install django-imagekit
python3.11 -m pip install Pillow
python3.11 -m pip install djangorestframework
python3.11 -m pip install drf-yasg
python3.11 -m pip install PyJWT
python3.11 -m pip install shortuuid
python3.11 -m pip install channels
python3.11 -m pip install imageio
python3.11 -m pip install pilkit
python3.11 -m pip install psycopg2
python3.11 -m pip install psycopg2-binary
python3.11 -m pip install psycopg
python3.11 -m pip install dj-database-url
python3.11 -m pip install websocket-client
python3.11 manage.py collectstatic --noinput --clear
echo "BUILD END"
echo "Make Migrations"
python3.11 manage.py makemigrations --noinput
python3.11 manage.py migrate --noinput
echo "Collect Static..."