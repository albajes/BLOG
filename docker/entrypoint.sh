#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

pwd
cd blog
ls -d */
pwd
source ../venv/bin/activate
python manage.py flush --no-input
python manage.py migrate

exec "$@"