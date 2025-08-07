#!/bin/sh
pip3 install -r client-requirements.txt -t deps
cp tvrclient.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/tvrclient.plist
