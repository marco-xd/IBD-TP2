#!/usr/bin/env python3

import glob
import json
import sys
from tp_utils import *


friends_folder = 'friends/'
fixed_folder = 'fixed_friends/'
achdir = 'achievements/'
summarydir = 'summaries/'
statsdir = 'stats/'
users = set()
visited = set()
friends = {}

for user in glob.glob(achdir + '*.json'):
    users.add(int(user[len(achdir):-5]))

for user in glob.glob(statsdir + '*.json'):
    users.add(int(user[len(statsdir):-5]))

for user in glob.glob(summarydir + '*.json'):
    users.add(int(user[len(summarydir):-5]))

for uid in users:
	with open(friends_folder + '/{0}.json'.format(uid), 'r') as ufile:
		ujson = json.load(ufile)
		ufile.close()
	visited.add(uid)
	friends[uid] = {}
	if len(ujson) is not 0:
		for friend in ujson['friendslist']['friends']:
			friends[uid][int(friend['steamid'])] = int(friend['friend_since'])

for uid in friends:
	friends[uid] = { k: friends[uid][k] for k in friends[uid] if k in visited }

for uid in friends:
	for fid in friends[uid]:
		friends[fid][uid] = friends[uid][fid]

for uid in friends:
	with open(fixed_folder + '/{0}.json'.format(uid), 'w') as ffile:
		ffile.write(json.dumps({ 'friendslist': { 'friends': [ { 'steamid': k, 'relationship': 'friend', 'friend_since': friends[uid][k] } for k in friends[uid] ] } }))
		ffile.close()
