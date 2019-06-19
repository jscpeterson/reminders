#!/bin/bash
rm db.sqlite3
rm -rf remind/migrations/*
rm -rf users/migrations/*
python manage.py makemigrations remind
python manage.py makemigrations users
#python manage.py makemigrations django_celery_results
python manage.py migrate
python manage.py create_fake_users