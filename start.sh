#!/bin/bash

# Wait for database to be ready
echo "Waiting for database to be ready..."
while ! mysqladmin ping -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent; do
    sleep 1
done

echo "Database is ready!"

# Create necessary directories
mkdir -p users_file_storage
mkdir -p flask_session

# Start gunicorn with configuration file
echo "Starting Gunicorn with configuration..."
exec gunicorn -c gunicorn.conf.py wsgi:application
