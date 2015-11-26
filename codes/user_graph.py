#!/usr/bin/env python3

import json
import sys
import glob
from tp_utils import *


max_users = 50000
friends_folder = 'friends/'
key = sys.argv[1]
q = queue()
visited = set()
frontier = set()
done = 0

userlist = open('users.txt', 'a+')
userlist.seek(0)

for line in userlist:
	uid = int(line)
	visited.add(uid)
	frontier.add(uid)

for user in glob.glob(friends_folder + '*.json'):
	uid = int(user[len(friends_folder):-5])
	done = done + 1
	if uid in frontier:
		frontier.remove(uid)
	else:
		visited.add(uid)

for uid in frontier:
	q.enqueue(uid)

frontier = None

if len(visited) is 0:
	q.enqueue(76561198013396073)
	visited.add(76561198013396073)
	userlist.write('{0}\n'.format(76561198013396073))

while not q.empty() and done < max_users:
	uid = q.dequeue()
	print('{0} ... '.format(uid), end = '')
	obj = fetch_json('http://api.steampowered.com/ISteamUser/GetFriendList/v1/?key={0}&steamid={1}&relationship=friend'.format(key, uid), None)
	if obj is not None:
		added = 0
		for user in obj['friendslist']['friends']:
			steamid = int(user['steamid'])
			if not steamid in visited:
				added = added + 1
				visited.add(steamid)
				q.enqueue(steamid)
				userlist.write('{0}\n'.format(steamid))
		userlist.flush()
		print('a = {0} / '.format(added), end = '')
	else:
		print('error / ', end = '')
		friends = '{}'
	ffile = open(friends_folder + '{0}.json'.format(uid), 'w')
	ffile.write(friends)
	ffile.close()
	done = done + 1
	print('v = {0} / q = {1} / d = {2}'.format(len(visited), len(q), done))

