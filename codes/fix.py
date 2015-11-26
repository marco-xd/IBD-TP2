#!/usr/bin/env python3
import json
import glob
import os
import random
from tp_utils import *
import sys


def fix_owned (owned, games):
	final = {}
	if 'response' in owned and 'games' in owned['response']:
		for game in owned['response']['games']:
			if str(game['appid']) in games:
				final[game['appid']] = {
					'playtime_forever': game['playtime_forever'],
					'playtime_2weeks': game['playtime_2weeks'] if 'playtime_2weeks' in game else 0
				}
	return final

with open('games.json', 'r') as fo:
	games = set(json.load(fo).keys())
	fo.close()

with open('users.json', 'r') as fo:
	users = set(json.load(fo).keys())
	fo.close()

for f in list(glob.glob('new_owned/*.json')):
	users.add(f[len('new_owned/'):-5])

for f in glob.glob('news/*.json'):
	if not f[len('news/'):-5] in games:
		os.remove(f)

for f in glob.glob('schema/*.json'):
	if not f[len('schema/'):-5] in games:
		os.remove(f)

key = sys.argv[1]
ignored = set()

with open('users.txt', 'r') as ufile:
	for f in list(glob.glob('owned/*.json')):
		if not f[len('owned/'):-5] in users:
			os.remove(f)
			continue
		uid = f[len('owned/'):-5]
		print('testing {0} ... '.format(uid), end = '')
		with open(f, 'r') as fo:
			try:	
				owned = fix_owned(json.load(fo), games)
			except:
				owned = {}
			fo.close()
		os.remove(f)
		if not len(owned) and random.random() >= 0.3:
			print('0 games')
			ignored.add(uid)
			while True:
				user = ufile.readline().strip()
				if len(user) is 0:
					sys.exit(1)
				if not user in users and not user in ignored:
					print('downloading {0} ... '.format(user), end = '')
					owned = fix_owned(fetch_json('http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={0}&include_played_free_games=1&steamid={1}'.format(key, user)), games)
					if len(owned):
						print('ok')
						ach = {}
						stats = {}
						friends = fetch_json('http://api.steampowered.com/ISteamUser/GetFriendList/v1/?key={0}&steamid={1}&relationship=friend'.format(key, user))
						summary = fetch_json('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={0}&steamids={1}'.format(key, user))
						for game in owned:
							gid = int(game)
							if has_stats(gid) or has_achievements(gid):
								print('stats -------- {0} --- {1}'.format(user, gid))
								info = fetch_json('http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?key={0}&appid={1}&steamid={2}'.format(key, gid, user))
								if 'playerstats' in info:
									if 'stats' in info['playerstats']:
										stats[gid] = info['playerstats']['stats']
									if 'achievements' in info['playerstats']:
										ach[gid] = info['playerstats']['achievements']
						with open('stats/{0}.json'.format(user), 'w') as fo:
							print('stats -------- {0}'.format(user))
							json.dump(stats, fo)
							fo.close()
						with open('achievements/{0}.json'.format(user), 'w') as fo:
							print('achievements - {0}'.format(user))
							json.dump(ach, fo)
							fo.close()
						with open('friends/{0}.json'.format(user), 'w') as fo:
							print('friends ------ {0}'.format(user))
							json.dump(friends, fo)
							fo.close()
						with open('summaries/{0}.json'.format(user), 'w') as fo:
							print('summary ------ {0}'.format(user))
							json.dump(summary, fo)
							fo.close()
						with open('new_owned/{0}.json'.format(user), 'w') as fo:
							print('owned -------- {0}'.format(user))
							json.dump(owned, fo)
							fo.close()
						users.add(user)
						break
					else:
						print('0 games')
						ignored.add(user)
			if os.path.exists('stats/{0}.json'.format(uid)):
				os.rename('stats/{0}.json'.format(uid), 'recycle/stats/{0}.json'.format(uid))
			if os.path.exists('friends/{0}.json'.format(uid)):
				os.rename('friends/{0}.json'.format(uid), 'recycle/friends/{0}.json'.format(uid))
			if os.path.exists('summaries/{0}.json'.format(uid)):
				os.rename('summaries/{0}.json'.format(uid), 'recycle/summaries/{0}.json'.format(uid))
			if os.path.exists('achievements/{0}.json'.format(uid)):
				os.rename('achievements/{0}.json'.format(uid), 'recycle/achievements/{0}.json'.format(uid))
			if os.path.exists('owned/{0}.json'.format(uid)):
				os.rename('owned/{0}.json'.format(uid), 'recycle/owned/{0}.json'.format(uid))
		else:
			print('ok')
			print('friends ------ {0}'.format(uid))
			download_file('http://api.steampowered.com/ISteamUser/GetFriendList/v1/?key={0}&steamid={1}&relationship=friend'.format(key, uid), 'friends/{0}.json'.format(uid))
			with open('new_owned/{0}.json'.format(uid), 'w') as fo:
				print('owned -------- {0}'.format(uid))
				json.dump(owned, fo)
				fo.close()
			if os.path.exists('owned/{0}.json'.format(uid)):
				os.rename('owned/{0}.json'.format(uid), 'recycle/owned/{0}.json'.format(uid))

	ufile.close()
