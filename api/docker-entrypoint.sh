#!/bin/sh

echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata auth
python manage.py collectstatic --noinput

exec "$@"
