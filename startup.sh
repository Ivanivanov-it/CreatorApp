#!/bin/bash
celery -A CreatorApp worker --loglevel=info &

gunicorn CreatorApp:app