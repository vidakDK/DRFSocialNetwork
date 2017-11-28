#!/usr/bin/env bash

rm -f tmp.db db.sqlite3
rm -r netapi/migrations
python manage.py makemigrations netapi
python manage.py migrate