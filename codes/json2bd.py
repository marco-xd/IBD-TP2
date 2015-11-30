import json, MySQLdb, glob, sys, os
from _mysql import NULL

def getDirFilesNames(path):
	abspath = os.path.dirname(os.path.abspath(sys.argv[0]))
	files = []
	for name in glob.glob(os.path.abspath(abspath + '/' + path) + '/*.json'):
		files.append(os.path.basename(name))
	return files

def connectBd(ip, door, userName, password, dbName):
	#Necessario passar a porta caso nao seja a padrao...
	if door==NULL:
		db = MySQLdb.connect(ip, userName, password, dbName, charset='utf8')
		return db
	else:
		db = MySQLdb.connect(host=ip, port=door, user=userName, passwd=password, db=dbName, charset='utf8')
		return db

#[:len(name)-5]
def insertFriends(db):
	jzimFriends = getDirFilesNames('../data/friends')
	cursor = db.cursor()
	
	for jName in jzimFriends:
		fR = open('data/friends/'+jName, 'r')
		jzim = json.load(fR)
		fR.close()
		id1 = jName[:len(jName)-5]
		friends = jzim.keys()
		#print friends

		for fnd in friends:
			aux = jzim[fnd]
			id2 = aux['steamid']
			friends_since = aux['friend_since']
			#print 'id2: %s - friends since: %d' % (id2, friends_since)
			sql = "INSERT INTO friends(relationship, friend_since, steamid1, steamid2)\
			VALUES ('Friends', %s, %s, %s)" % (db.escape_string(u''.join(str(friends_since)).encode('utf8').strip()), db.escape_string(u''.join(str(id1)).encode('utf8').strip()), db.escape_string(u''.join(str(id2)).encode('utf8').strip()))
			cursor.execute(sql)
			db.commit()
				
def insertOwned(db):
	jzimOwned = getDirFilesNames('../data/owned')
	cursor = db.cursor()
	
	for jName in jzimOwned:
		fR = open('data/owned/'+jName, 'r')
		jzim = json.load(fR)
		fR.close()
		myId = jName[:len(jName)-5]
		gamesId = jzim.keys()
		#print len(gamesId)

		for gId in gamesId:
			aux = jzim[gId]
			playtime_forever = aux['playtime_forever']
			playtime_2weeks = aux['playtime_2weeks']
			#print 'playtime_2weeks: %s - playtime_forever: %d' % (playtime_2weeks, playtime_forever)
			sql = "INSERT INTO owned(steamid, appid, playtime_forever, playtime_2weeks)\
			VALUES ('%s', %d, %s, %s)" % (db.escape_string(u''.join(str(myId)).encode('utf8').strip()), int(gId), db.escape_string(u''.join(str(playtime_forever)).encode('utf8').strip()), db.escape_string(u''.join(str(playtime_2weeks)).encode('utf8').strip()))
			cursor.execute(sql)
			db.commit()

def insertPlayerAchievements(db):
	jzimAchievements = getDirFilesNames('../data/achievements')
	cursor = db.cursor()
	
	for jName in jzimAchievements:
		fR = open('data/achievements/'+jName, 'r')
		jzim = json.load(fR)
		fR.close()
		myId = jName[:len(jName)-5]
		gamesId = jzim.keys()
		if len(gamesId)==0:
			print 'Nao tinha nada: %s' % (myId)
			continue
		#print len(gamesId)
		for gId in gamesId:
			aux2 = jzim[gId]
			for aux in aux2:
				name = aux['name']
				#print 'playtime_2weeks: %s - playtime_forever: %d' % (playtime_2weeks, playtime_forever)
				sql = "INSERT INTO playerachievements(steamid, appid, achi_name, achieved)\
				VALUES ('%s', %d, '%s', 1)" % (db.escape_string(u''.join(str(myId)).encode('utf8').strip()), int(gId), db.escape_string(u''.join(str(name)).encode('utf8').strip()))
				cursor.execute(sql)
				db.commit()
			
def insertPlayerStats(db):
	jzimStats = getDirFilesNames('../data/stats')
	cursor = db.cursor()
	
	for jName in jzimStats:
		fR = open('data/stats/'+jName, 'r')
		jzim = json.load(fR)
		fR.close()
		myId = jName[:len(jName)-5]
		gamesId = jzim.keys()
		if len(gamesId)==0:
			print 'Nao tinha nada: %s' % (myId)
			continue
		#print len(gamesId)
		for gId in gamesId:
			aux2 = jzim[gId]
			for aux in aux2:
				name = aux['name']
				value = aux['value']
				#print 'playtime_2weeks: %s - playtime_forever: %d' % (playtime_2weeks, playtime_forever)
				sql = "INSERT INTO playerstats(steamid, appid, stats_name, value)\
				VALUES ('%s', %d, '%s', %s)" % (db.escape_string(u''.join(str(myId)).encode('utf8').strip()), int(gId), db.escape_string(u''.join(str(name)).encode('utf8').strip()), db.escape_string(u''.join(str(value)).encode('utf8').strip()))
				cursor.execute(sql)
				db.commit()


def insertSummaries(db):
	jzimSummaries = getDirFilesNames('../data/summaries')
	cursor = db.cursor()
	
	for jName in jzimSummaries:
		fR = open('data/summaries/'+jName, 'r')
		aux = json.load(fR)
		fR.close()
		myId = jName[:len(jName)-5]
		avatar = aux['avatar']
		communityvisibilitystate = aux['communityvisibilitystate']
		avatarmedium = aux['avatarmedium']
		personaname = aux['personaname']
		personastate = aux['personastate']
		profilestate = aux['profilestate']
		lastlogoff = aux['lastlogoff']
		avatarfull = aux['avatarfull']
		#commentpermission = aux['commentpermission']
		personastateflags = aux['personastateflags']
		profileurl = aux['profileurl']
		loccountrycode = aux['loccountrycode']
		
		sql = "INSERT INTO summaries(steamid, avatar, communityvisibilitystate, avatarmedium, personaname,\
		personastate, profilestate, lastlogoff, avatarfull, commentpermission, personastateflags,\
		profileurl, loccountrycode) VALUES ('%s', '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '0', %s, '%s',\
		 '%s')" % (db.escape_string(u''.join(str(myId)).encode('utf8').strip()), db.escape_string(u''.join(str(avatar)).encode('utf8').strip()), db.escape_string(u''.join(str(communityvisibilitystate)).encode('utf8').strip()),
				db.escape_string(u''.join(str(avatarmedium)).encode('utf8').strip()), db.escape_string(u''.join(str(personaname)).encode('utf8').strip()), db.escape_string(u''.join(str(personastate)).encode('utf8').strip()), 
				db.escape_string(u''.join(str(profilestate)).encode('utf8').strip()), db.escape_string(u''.join(str(lastlogoff)).encode('utf8').strip()), db.escape_string(u''.join(str(avatarfull)).encode('utf8').strip()),
				db.escape_string(u''.join(str(personastateflags)).encode('utf8').strip()), db.escape_string(u''.join(str(profileurl)).encode('utf8').strip()), db.escape_string(u''.join(str(loccountrycode)).encode('utf8').strip()))
		cursor.execute(sql)
		db.commit()

def insertAchievements(db):
	jzimAchievements = getDirFilesNames('../data/schema')
	cursor = db.cursor()
	
	for jName in jzimAchievements:
		fR = open('data/schema/'+jName, 'r')
		jzim = json.load(fR)
		fR.close()
		myId = jName[:len(jName)-5]
		achievements = jzim['achievements']
		
		for acv in achievements:
			achi_name = acv['name'].replace('\'', '\\\'')
			defaultvalue = acv['defaultvalue']
			displayname = acv['displayName'].replace('\'', '\\\'')
			hidden = acv['hidden']
			icon = acv['icon']
			icongray = acv['icongray']
			
			sql = "INSERT INTO achievements(appid, achi_name, defaultvalue, displayname, hidden, icon, icongray) \
			VALUES (%d, '%s', %s, '%s', %s, '%s', '%s')" % (int(myId), db.escape_string(u''.join(str(achi_name)).encode('utf8').strip()), db.escape_string(u''.join(str(defaultvalue)).encode('utf8').strip()),
				db.escape_string(u''.join(str(displayname)).encode('utf8').strip()), db.escape_string(u''.join(str(hidden)).encode('utf8').strip()), db.escape_string(u''.join(str(icon)).encode('utf8').strip()), db.escape_string(u''.join(str(icongray)).encode('utf8').strip()))
			
			cursor.execute(sql)
			db.commit()
	
def main():
	host = 'localhost'
	port = 2222
	user = 'root'
	passw = 'ibdsteamUFMG'
	dbName = 'steam'
	
	db = connectBd(host, port, user, passw, dbName)
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
			print "MySQL Error: %s" % u''.join(str(e)).encode('utf8').strip()
		raise
	db.close()

main()
exit