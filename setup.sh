#!/usr/bin/env bash
touch credentials.json
apt install python3 -y && pip3 install requests
echo python3 ~/college-login-portal/login-script.py >> ~/.bashrc