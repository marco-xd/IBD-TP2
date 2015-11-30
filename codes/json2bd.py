import json, MySQLdb, glob, sys, os
from _mysql import NULL

def normalizePath (path):
	abspath = os.path.dirname(os.path.abspath(sys.argv[0]))
	return os.path.abspath(abspath + '/' + path)


def getDirFilesNames (path):
	files = []
	for name in glob.glob(normalizePath(path) + '/*.json'):
		files.append(os.path.basename(name))
	return files

#[:len(name)-5]
def insertFriends (db):
	jzimFriends = getDirFilesNames('../data/friends')
	cursor = db.cursor()
	for jName in jzimFriends:
		with open(normalizePath('../data/friends/' + jName), 'r') as fR:
			jzim = json.load(fR)
			fR.close()
		for fnd, info in jzim.iteritems():
			if id1 > info['steamid']:
				cursor.execute("INSERT INTO friends(relationship, friend_since, steamid1, steamid2) VALUES ('friends', %s, %s, %s)",
					(info['friend_since'], id1, info['steamid']))
				
def insertOwned (db):
	jzimOwned = getDirFilesNames('../data/owned')
	cursor = db.cursor()
	
	for jName in jzimOwned:
		with open(normalizePath('../data/owned/' + jName), 'r') as fR:
			jzim = json.load(fR)
			fR.close()
		myId = jName[:-5]
		for gId, info in jzim.iteritems():
			cursor.execute("INSERT INTO owned(steamid, appid, playtime_forever, playtime_2weeks) VALUES ('%s', '%s', %d, %d)",
				(myId, gId, info['playtime_forever'], info['playtime_2weeks']))

def insertPlayerAchievements (db):
	jzimAchievements = getDirFilesNames('../data/achievements')
	cursor = db.cursor()
	
	for jName in jzimAchievements:
		with open(normalizePath('../data/achievements/' + jName), 'r') as fR:
			jzim = json.load(fR)
			fR.close()
		myId = jName[:-5]
		for gId, info in jzim.iteritems():
			for aux in info:
				cursor.execute("INSERT INTO playerachievements(steamid, appid, achi_name, achieved) VALUES ('%s', '%s', '%s', 1)",
					(myId, gId, aux['name']))
			
def insertPlayerStats (db):
	jzimStats = getDirFilesNames('../data/stats')
	cursor = db.cursor()
	
	for jName in jzimStats:
		with open(normalizePath('../data/stats/' + jName), 'r') as fR:
			jzim = json.load(fR)
			fR.close()
		myId = jName[:-5]
		for gId, info in jzim.iteritems():
			for aux in info:
				cursor.execute("INSERT INTO playerstats(steamid, appid, stats_name, value) VALUES ('%s', '%s', '%s', '%d')",
					(myId, gId, aux['name'], aux['value']))


def insertSummaries (db):
	jzimSummaries = getDirFilesNames('../data/summaries')
	cursor = db.cursor()
	
	for jName in jzimSummaries:
		with open(normalizePath('../data/summaries/' + jName), 'r') as fR:
			aux = json.load(fR)
			fR.close()
		myId = jName[:-5]
		cursor.execute("INSERT INTO summaries (steamid, avatar, communityvisibilitystate, avatarmedium, personaname, personastate, profilestate, lastlogoff, avatarfull, personastateflags, profileurl, loccountrycode, commentpermission)" +
		"VALUES ('%s', '%s', '%d', '%s', '%s', %d, '%s', %d, '%s', '%d', '%s', '%s', '%d')",
			(
				myId,
				aux['avatar'],
				aux['communityvisibilitystate'],
				aux['avatarmedium'],
				aux['personaname'],
				aux['personastate'],
				aux['profilestate'],
				aux['lastlogoff'],
				aux['avatarfull'],
				aux['personastateflags'],
				aux['profileurl'],
				aux['loccountrycode'],
				aux['commentpermission'] if 'commentpermission' in aux else 0
			)
		)

def insertAchievements (db):
	jzimAchievements = getDirFilesNames('../data/schema')
	cursor = db.cursor()
	
	for jName in jzimAchievements:
		with open(normalizePath('../data/schema/' + jName), 'r') as fR:
			jzim = json.load(fR)
			fR.close()
		myId = jName[:-5]
		for acv in jzim['achievements']:
			print(acv)
			cursor.execute("INSERT INTO achievements(appid, achi_name, defaultvalue, displayname, hidden, icon, icongray) VALUES ('%s', '%s', '%d', '%s', '%d', '%s', '%s')",
				(myId, acv['name'], int(acv['defaultvalue']), acv['displayName'], int(acv['hidden']), acv['icon'], acv['icongray']))
	
def main ():
	host = 'localhost'
	user = 'root'
	pw = 'ibdsteamUFMG'
	dbName = 'steam'
	
	db = MySQLdb.connect(host, user, pw, dbName, charset='utf8')
	try:
		#insertFriends(db)
		#insertOwned(db)
		#insertPlayerAchievements(db)
		#insertPlayerStats(db)
		#insertSummaries(db)
		insertAchievements(db)
		db.commit()
	except MySQLdb.Error, e:
		db.rollback()
		try:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		except IndexError:
			print "MySQL Error: %s" % e
		raise
	db.close()

main()
exit