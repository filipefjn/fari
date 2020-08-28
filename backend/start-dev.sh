#!/bin/bash
. venv/bin/activate
python3 db.py
# use '--log-level debug' for more detailed logging
./venv/bin/gunicorn \
    --timeout 600 \
    --log-level info \
    --access-logfile access.log \
    --reload \
    --workers 4 \
    --bind 0.0.0.0:5000 wsgi:app
