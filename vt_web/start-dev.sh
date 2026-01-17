#!/bin/bash
# export DEBUG=True
# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create a superuser if no users exist
echo "Creating superuser if no users exist..."
python manage.py createsuperuserifnone

python manage.py collectstatic --noinput

# Start the Django server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000