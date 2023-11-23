#!/bin/sh
until cd /stripeproject
do
    echo "Waiting for server volume..."
done

python manage.py collectstatic --noinput

gunicorn stripeproject.wsgi:application --bind 0.0.0.0:8000