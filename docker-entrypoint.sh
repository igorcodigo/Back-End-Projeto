#!/bin/bash
set -e

# Create the database directory if it doesn't exist
mkdir -p /app/db

# Copy the existing database file if it exists in the base directory but not in the /app/db directory
if [ -f /app/db.sqlite3 ] && [ ! -f /app/db/db.sqlite3 ]; then
  echo "Copying existing database to the Docker volume..."
  cp /app/db.sqlite3 /app/db/db.sqlite3
fi

# Run migrations
python manage.py migrate

# Start the Django development server
exec python manage.py runserver 0.0.0.0:8000 