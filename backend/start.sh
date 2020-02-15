#!/bin/bash
source venv/bin/activate
export FLASK_APP=app.py
export FLASK_DEBUG=1
# export FLASK_RUN_HOST=0.0.0.0
# export FLASK_RUN_PORT=80
flask run
