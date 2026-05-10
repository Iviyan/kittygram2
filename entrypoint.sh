#!/bin/sh
mkdir -p /app/data
touch /app/data/db.sqlite3
python manage.py migrate --noinput
exec gunicorn kittygram2.wsgi:application --bind 0.0.0.0:8000
