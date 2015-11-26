#!/usr/bin/env python3

import json
import sys
import glob
from tp_utils import *

min_summaries = 10

key = sys.argv[1]
owneddir = 'owned/'
achdir = 'achievements/'
summarydir = 'summaries/'
statsdir = 'stats/'
friendsdir = 'fixed_friends/'
users = set()

def write_summaries(summaries):
    print('summaries ---- download - {0}'.format(len(summaries)))
    ss = fetch_json('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={0}&steamids={1}'.format(key, ','.join(summaries)), onerror = {})
    summaries.clear()
    if 'response' in ss and 'players' in ss['response']:
        for player in ss['response']['players']:
            with open(summarydir + '{0}.json'.format(player['steamid']), 'w') as sfile:
                json.dump(player, sfile)
                sfile.close()

for user in glob.glob(achdir + '*.json'):
        uid = int(user[len(achdir):-5])
        users.add(uid)

for user in glob.glob(statsdir + '*.json'):
        uid = int(user[len(statsdir):-5])
        users.add(uid)

for user in glob.glob(summarydir + '*.json'):
        uid = int(user[len(summarydir):-5])
        users.add(uid)

summaries = []

for pos, uid in enumerate(users):

    print("{0} - {1}".format(pos, uid))

    uidjson = '{0}.json'.format(uid)

    summaryfile = summarydir + uidjson
    if not is_json(summaryfile):
        summaries.append(str(uid))
        print('summaries ---- {0} - {1}'.format(uid, len(summaries)))
        if len(summaries) >= min_summaries:
            write_summaries(summaries)


    ownedfile = owneddir + uidjson
    if not is_json(ownedfile):
        print('owned -------- {0}'.format(uid))
        download_file('http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={0}&include_played_free_games=1&steamid={1}'.format(key, uid), ownedfile)

    if is_json(ownedfile):

        with open(ownedfile, 'r') as ofile:
            games = json.load(ofile)['response']
            ofile.close()

        achfile = achdir + uidjson
        if is_json(achfile):
            with open(achfile, 'r') as afile:
                ach = json.load(afile)
                afile.close()
        else:
            ach = {}

        statsfile = statsdir + uidjson
        if is_json(statsfile):
            with open(statsfile, 'r') as sfile:
                stats = json.load(sfile)
                sfile.close()
        else:
            stats = {}

        if 'games' in games:
            for game in games['games']:
                gid = int(game['appid'])

                if not str(gid) in ach and has_achievements(gid):
                    print('achievements - {0} --- {1}'.format(uid, gid))
                    ach[gid] = fetch_json('http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?key={0}&appid={1}&steamid={2}'.format(key, gid, uid))

                if not str(gid) in stats and has_stats(gid):
                    print('stats -------- {0} --- {1}'.format(uid, gid))
                    stats[gid] = fetch_json('http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?key={0}&appid={1}&steamid={2}'.format(key, gid, uid))


        with open(achfile, 'w') as afile:
            json.dump(ach, afile)
            afile.close()

        with open(statsfile, 'w') as sfile:
            json.dump(stats, sfile)
            sfile.close()
