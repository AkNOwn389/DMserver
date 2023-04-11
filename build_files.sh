echo "BUILD START BOSS DARIUS"
python3.9 -m pip install -r requirements.txt
python3.9 -m pip install django
python3.9 -m pip install daphne
python3.9 -m pip install djangorestframework-simplejwt
python3.9 -m pip install django-cors-headers
python3.9 manage.py collectstatic --noinput --clear

echo "BUILD END"