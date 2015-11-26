import json
from os.path import exists
from subprocess import call, check_output


def fix_owned (owned, games):
    if len(owned):
        if 'response' in owned and 'games' in owned['response']:
            final = {}
            for game in owned['response']['games']:
                if str(game['appid']) in games:
                    final[game['appid']] = {
                        'playtime_forever': game['playtime_forever'],
                        'playtime_2weeks': game['playtime_2weeks'] if 'playtime_2weeks' in game else 0
                    }
            return final
        return owned
    return {}

def fix_ach (ach, games):
    if len(ach):
        result = {}
        for gid in ach:
            if gid in games:
                if isinstance(ach[gid], list):
                    result[gid] = ach[gid]
                elif 'playerstats' in ach[gid] and 'achievements' in ach[gid]['playerstats']:
                    game = [ { 'achieved': 1, 'name': k['apiname'] } for k in ach[gid]['playerstats']['achievements'] if k['achieved'] is 1 ]
                    if len(game):
                        result[gid] = game
        return result
    return ach

def fix_stats (stats, games):
    if len(stats):
        result = {}
        for gid in stats:
            if gid in games:
                if isinstance(stats[gid], list):
                    result[gid] = stats[gid]
                elif 'playerstats' in stats[gid] and 'stats' in stats[gid]['playerstats'] and len(stats[gid]['playerstats']['stats']):
                    result[gid] = stats[gid]['playerstats']['stats']
        return result
    return stats

def fix_summary (summary):
    if len(summary) is 1:
        return summary['response']['players'][0]
    return summary

def is_json(fname):
    if exists(fname):
        try:
            with open(fname, 'r') as f:
                json.load(f)
                f.close()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            return False
        return True
    return False

ach_cache = {}
def has_achievements(gid):
    gid = int(gid)
    if not gid in ach_cache:
        try:
            with open('schema/{0}.json'.format(gid), 'r') as gfile:
                gschema = json.load(gfile)
                gfile.close()
                ach_cache[gid] = !!gschema['game']['availableGameStats']['achievements']
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            ach_cache[gid] = False
    return ach_cache[gid]

stats_cache = {}
def has_stats(gid):
    gid = int(gid)
    if not gid in stats_cache:
        try:
            with open('schema/{0}.json'.format(gid), 'r') as gfile:
                gschema = json.load(gfile)
                gfile.close()
                stats_cache[gid] = !!gschema['game']['availableGameStats']['stats']
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            stats_cache[gid] = False
    return stats_cache[gid]

def fetch_json(url, onerror = { 'success': False }):
    try:
        js = json.loads(check_output(['wget', '--content-on-error', '-qO-', url]).decode('utf-8'))
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        js = onerror
    return js

def download_file(url, destiny):
    call(['wget', '--content-on-error', '-qO', destiny, url])

class queue(object):

    def __init__(self):
        self.start = None
        self.end = None
        self.size = 0

    def enqueue(self, val):
        new = [val, None]
        if self.start is None:
            self.start = new
        else:
            self.end[1] = new
        self.size = self.size + 1
        self.end = new

    def dequeue(self):
        val = self.start
        if self.empty():
            return None
        else:
            self.size = self.size - 1
            self.start = val[1]
            if self.empty():
                self.end = None
            return val[0]

    def empty(self):
        return self.start is None

    def __len__(self):
        return self.size
