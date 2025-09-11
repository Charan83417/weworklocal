#!/bin/bash

# Simple start script for Railway deployment
echo "Starting WeWorkLocal application..."

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the application
echo "Starting Gunicorn server..."
exec gunicorn weworklocal.wsgi:application --bind 0.0.0.0:$PORT --workers 2
