#!/usr/bin/env python
from sys import argv
import os
import json
import time
import requests
from deluge_client import DelugeRPCClient

path = 'data.csv' #Path to csv file
host = '127.0.0.1', #Deluge host
port = 0, #Deluge port
username = '' #Deluge username
password = '' #Deluge password
api_key = '' #Redacted API key

def load():
    if not os.path.exists(path):
        open(path, 'w').close()

    users = {}

    with open(path, 'r') as f:
        lines = f.read().splitlines()
        for line in lines:
            values = line.split(',')
            users[values[0]] = {
                'username': values[1],
                'ratios': values[2],
                'downloadeds': values[3],
                'uploadeds': values[4],
            }
    return users

def save(users):
    lines = []

    for user in users:
        line = user + ',' + users[user]['username'] + ',' + users[user]['ratios'] + ',' + users[user]['downloadeds'] + ',' + users[user]['uploadeds'] + '\n'
        lines.append(line)

    with open(path, 'w') as f:
        f.writelines(lines)

client = DelugeRPCClient(host, port, username, password)
client.connect()

if not client.connected:
    quit()

time.sleep(60)

torrent_id = argv[1]
status = client.call('core.get_torrent_status', torrent_id, ['tracker_host', 'ratio', 'total_done', 'total_uploaded'])

if status['tracker_host'] != 'flacsfor.me':
    quit()

headers = {
    'Authorization': api_key,
    'User-Agent': 'red_users/1.0 (Confruggy)'
}

response = requests.get('https://redacted.ch/ajax.php?action=torrent&hash=' + torrent_id.upper(), headers=headers)
torrent = json.loads(response.text)['response']['torrent']
user_id = str(torrent['userId'])
username = torrent['username']

users = load()

if users.has_key(user_id): 
    users[user_id]['username'] = username
    users[user_id]['ratios'] += str(status['ratio']) + ';'
    users[user_id]['downloadeds'] += str(status['total_done']) + ';'
    users[user_id]['uploadeds'] += str(status['total_uploaded']) + ';'
else:
    users[user_id] = {
        'username': username,
        'ratios': str(status['ratio']) + ';',
        'downloadeds': str(status['total_done']) + ';',
        'uploadeds': str(status['total_uploaded']) + ';'
    }

save(users)