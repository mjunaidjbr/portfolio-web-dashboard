#!/bin/sh

# Wait for the database to be ready
while ! nc -z db 5432; do
  sleep 0.1
done

# Run makemigrations and migrate
python manage.py makemigrations
python manage.py migrate
# python manage.py collectstatic --noinput

# Start the Gunicorn server
exec gunicorn --bind 0.0.0.0:8000 portfolioLedger.wsgi:application
