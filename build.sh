#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py makemigrations
python manage.py migrate

python test_db_connection.py

python create_superuser.py

