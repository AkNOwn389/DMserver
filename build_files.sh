echo "BUILD START BOSS DARIUS"
python3.9 -m pip install -r requirements.txt
python3.9 -m pip install django
python3.9 -m pip install daphne
python3.9 -m pip install djangorestframework-simplejwt
python3.9 -m pip install django-cors-headers
python3.9 -m pip install django-cloudinary-storage
python3.9 -m pip install cloudinary
python3.9 -m pip install django_extensions
python3.9 -m pip install django-imagekit
python3.9 -m pip install Pillow
python3.9 -m pip install djangorestframework
python3.9 -m pip install drf-yasg
python3.9 -m pip install PyJWT
python3.9 -m pip install shortuuid
python3.9 -m pip install channels
python3.9 -m pip install imageio
python3.9 -m pip install pilkit
python3.9 -m pip install websocket-client
python3.9 -m pip install urllib3
python3.9 -m pip install mysqlclient
python3.9 manage.py collectstatic --noinput --clear
yum install sqlite-devel
./configure
make && make altinstall

echo "BUILD END"