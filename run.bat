:: Enter env
env\Scripts\activate.bat

:: Apply migrations
python ETC\manage.py makemigrations ETC
python ETC\manage.py migrate

:: Run server
python ETC\manage.py runserver
