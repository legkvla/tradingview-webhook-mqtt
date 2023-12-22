#!/bin/sh
heroku config:get REDIS_TLS_URL -s > .env
python3 rclient.py
