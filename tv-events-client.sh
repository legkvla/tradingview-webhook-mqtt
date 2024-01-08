#!/bin/sh
/opt/homebrew/bin/heroku config:get REDIS_TLS_URL -s > .env
/opt/homebrew/bin/heroku config:get SEC_KEY -s >> .env
/usr/bin/python3 -u rclient.py
