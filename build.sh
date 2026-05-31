#!/bin/bash

# Install dependencies
python -m pip install --break-system-packages -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput
