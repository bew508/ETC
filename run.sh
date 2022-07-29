# Enter env
source env/bin/activate

# Apply migrations
python3 ETC/manage.py makemigrations ETC
python3 ETC/manage.py migrate

# Run server
python3 ETC/manage.py runserver
