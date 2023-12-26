#!/bin/sh
heroku config:get REDIS_TLS_URL -s > .env
heroku config:get SEC_KEY -s >> .env
python3 rclient.py
