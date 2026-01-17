#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create a superuser if no users exist
echo "Creating superuser if no users exist..."
python manage.py createsuperuserifnone

python manage.py collectstatic --noinput

# Start the Django server
echo "Starting Django server..."
gunicorn --bind 0.0.0.0:8000 --workers 2 --threads 2 vt_conf.wsgi:application
