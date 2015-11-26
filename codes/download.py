#!/usr/bin/env python3

import json
import sys
from time import sleep
from tp_utils import *


key = sys.argv[1]
newsdir = 'news/'
schemadir = 'schema/'
detailsdir = 'details/'

with open('games.json') as games_file:    
    games = json.load(games_file)
    games_file.close()

print('Processing {0} games...'.format(len(games['applist']['apps'])))

for game in games['applist']['apps']:

    gid = game['appid']
    gidjson = '{0}.json'.format(gid)

    newsfile = newsdir + gidjson
    while not is_json(newsfile):
        print('news ---- {0}'.format(gid))
        download_file('http://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?count=100000&appid={0}'.format(gid), newsfile)

    schemafile = schemadir + gidjson
    while not is_json(schemafile):
        print('schema -- {0}'.format(gid))
        download_file('http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={0}&appid={1}'.format(key, gid), schemafile)

    tried = False
    sleeps = 0
    detailsfile = detailsdir + gidjson
    while not is_json(detailsfile):
        if tried is True:
            sleeps = sleeps + 1
            stime = 10 * sleeps
            print('sleeping for {0}s'.format(stime))
            sleep(stime)
        print('details - {0}'.format(gid))
        download_file('http://store.steampowered.com/api/appdetails?appids={0}'.format(gid), detailsfile)
        tried = True
