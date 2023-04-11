echo "BUILD START BOSS DARIUS"
python3 -m pip install --user --no-cache-dir google-cloud-bigquery
python3 -m pip install --upgrade setuptools
pip install -r requirements.txt
python3.9 manage.py collectstatic --noinput
apt-get install python-dev
sudo apt-get install mysql-server
sudo apt-get install libmysqlclient-dev
sudo apt-get install libmariadbclient-dev
sudo apt-get install libmysqlclient-dev
python3.9 pip install --upgrade-pip
python3.9 pip install mysql-python
python3.9 -m pip install -r requirements.txt
python3.9 -m pip install django
python3.9 -m pip install _sqlite3
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
python3.8 -m pip install --upgrade systemd-python
python3.9 -m pip install mysqlclient
python3.9 -m pip install mysql-python

python3.9 manage.py collectstatic --noinput --clear
yum install sqlite-devel
./configure
make && make altinstall


echo "BUILD END"