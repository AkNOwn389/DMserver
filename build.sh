#/bin/bash

echo "BUILD START BOSS DARIUS"
python3.9 -m pipenv shell
python3.9 -m pip install -r requirements.txt
echo "BUILD END"
echo "Make Migrations"
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput
echo "Collect Static..."