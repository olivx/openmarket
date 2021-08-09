#!/usr/bin/env bash

echo "Waiting 15 seconds to be sure database is setup"

sleep 15

/usr/local/bin/python3 manage.py migrate

/usr/local/bin/gunicorn -c gunicorn.py openmarket.wsgi:application
