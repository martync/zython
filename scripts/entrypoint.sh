#!/bin/bash -e

python manage.py migrate
python manage.py collectstatic --clear --no-input

exec "$@"
