#!/bin/bash
rm db.sqlite3
#python manage.py makemigrations django_celery_results
python manage.py migrate
python manage.py create_fake_users
