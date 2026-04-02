#!/bin/bash

celery -A CreatorApp worker --loglevel=info &


gunicorn CreatorApp.wsgi --bind=0.0.0.0:8000