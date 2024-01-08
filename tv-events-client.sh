#!/bin/sh
/opt/homebrew/bin/heroku config:get REDIS_TLS_URL -s > .env
/opt/homebrew/bin/heroku config:get SEC_KEY -s >> .env
python3 rclient.py
