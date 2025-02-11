#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# to reset the database
python manage.py flush --no-input
python manage.py makemigrations chatbot
python manage.py migrate

# this executes the command passed from docker-compose.yml
exec "$@"