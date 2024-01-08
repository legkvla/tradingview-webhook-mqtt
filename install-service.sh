#!/bin/sh
pip3 install -r requirements.txt -t deps
cp tvrclient.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/tvrclient.plist
