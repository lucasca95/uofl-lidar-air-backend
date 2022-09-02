#!/bin/bash

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

export FLASK_APP=app.py
flask run --reload --host=0.0.0.0 --port=5000