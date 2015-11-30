import json, MySQLdb, glob, sys, os, codecs
from _mysql import NULL

def normalizePath (path):
	abspath = os.path.dirname(os.path.abspath(sys.argv[0]))
	return os.path.abspath(abspath + '/' + path)


def getDirFilesNames (path):
	files = []
	for name in glob.glob(normalizePath(path) + '/*.json'):
		files.append(os.path.basename(name))
	return files

def insertCountries (db):
	inserted = {}
	countries = getDirFilesNames('../data/countries')
	cursor = db.cursor()
	for f in countries:
		with codecs.open(normalizePath('../data/countries/' + f), 'r', 'utf-8') as fo:
			country = json.load(fo)
			fo.close()
		if not country['loccountrycode'] in inserted:
			inserted[country['loccountrycode']] = True
			cursor.execute("INSERT INTO countries(countryname, countrycurrency, loccountrycode, countrytype, countrysubtype, countryformalname, countrysovereignty) VALUES (%s, %s, %s, %s, %s, %s, %s)",
				(country['countryname'], country['countrycurrency'], country['loccountrycode'], country['countrytype'], country['countrysubtype'], country['countryformalname'], country['countrysovereignty']))

def insertSummaries (db):
	jzimSummaries = getDirFilesNames('../data/summaries')
	cursor = db.cursor()
	
	for jName in jzimSummaries:
		with codecs.open(normalizePath('../data/summaries/' + jName), 'r', 'utf-8') as fR:
			aux = json.load(fR)
			fR.close()
		myId = jName[:-5]
		print "\r" + myId, 
		cursor.execute("INSERT INTO summaries (steamid, avatar, communityvisibilitystate, avatarmedium, personaname, personastate, profilestate, lastlogoff, avatarfull, personastateflags, profileurl, loccountrycode, commentpermission)" +
		"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
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

def insertFriends (db):
	jzimFriends = getDirFilesNames('../data/friends')
	cursor = db.cursor()
	for jName in jzimFriends:
		with codecs.open(normalizePath('../data/friends/' + jName), 'r', 'utf-8') as fR:
			jzim = json.load(fR)
			fR.close()
		id1 = jName[:-5]
		# print(id1)
		for fnd, info in jzim.iteritems():
			if id1 > info['steamid']:
				cursor.execute("INSERT INTO friends(relationship, friend_since, steamid1, steamid2) VALUES ('friend', %s, %s, %s)",
					(info['friend_since'], id1, info['steamid']))

def insertDetails (db):
	files = getDirFilesNames('../data/details')
	cursor = db.cursor()
	for f in files:
		with codecs.open(normalizePath('../data/details/' + f), 'r', 'utf-8') as fo:
			game = json.load(fo)
			fo.close()
		appid = f[:-5]
		print "\r" + appid, 
		cursor.execute('INSERT INTO `details` (`appid`, `about_the_game`, `background`, `coming_soon`, `detailed_description`, `dlc_from`,' +
			' `header_image`, `is_free`, `linux_requirements`, `linux_support`, `mac_requirements`, `mac_support`, `pc_requirements`, `price`,' +
			' `release_date`, `required_age`, `support_email`, `support_url`, `supported_languages`, `type`, `website`, `windows_support`)' +
			' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
			(appid, game['about_the_game'], game['background'], game['coming_soon'], game['detailed_description'], game['dlc_from'],
				game['header_image'], game['is_free'], game['linux_requirements'], game['linux_support'], game['mac_requirements'], game['mac_support'], game['pc_requirements'], game['price'],
				game['release_date'], game['required_age'], game['support_email'], game['support_url'], game['supported_languages'], game['type'], game['website'], game['windows_support']))

def insertAchievementsAndStats (db):
	jzimAchievements = getDirFilesNames('../data/schema')
	cursor = db.cursor()
	
	for jName in jzimAchievements:
		with codecs.open(normalizePath('../data/schema/' + jName), 'r', 'utf-8') as fR:
			jzim = json.load(fR)
			fR.close()
		myId = jName[:-5]
		print "\r" + myId, 
		for acv in jzim['achievements']:
			cursor.execute("INSERT INTO achievements(appid, achi_name, defaultvalue, displayname, hidden, icon, icongray) VALUES (%s, %s, %s, %s, %s, %s, %s)",
				(myId, acv['name'], acv['defaultvalue'], acv['displayName'], acv['hidden'], acv['icon'], acv['icongray']))
		for stat in jzim['stats']:
			cursor.execute("INSERT INTO stats(appid, stat_name, defaultvalue, displayname) VALUES (%s, %s, %s, %s)",
				(myId, stat['name'], stat['defaultvalue'], stat['displayName']))

def insertPlayerAchievements (db):
	jzimAchievements = getDirFilesNames('../data/achievements')
	cursor = db.cursor()
	
	for jName in jzimAchievements:
		with codecs.open(normalizePath('../data/achievements/' + jName), 'r', 'utf-8') as fR:
			jzim = json.load(fR)
			fR.close()
		myId = jName[:-5]
		print "\r" + myId, 
		for gId, info in jzim.iteritems():
			for aux in info:
				cursor.execute("INSERT INTO playerachievements(steamid, appid, achi_name, achieved) VALUES (%s, %s, %s, 1)",
					(myId, gId, aux['name']))
			
def insertPlayerStats (db):
	jzimStats = getDirFilesNames('../data/stats')
	cursor = db.cursor()
	for jName in jzimStats:
		with codecs.open(normalizePath('../data/stats/' + jName), 'r', 'utf-8') as fR:
			jzim = json.load(fR)
			fR.close()
		myId = jName[:-5]
		for gId, info in jzim.iteritems():
			for aux in info:
				print "\r" + (' ' * 80) + "\r" + myId + ' ' + aux['name'] + ' ' + str(aux['value']),
				cursor.execute("INSERT INTO playerstats(steamid, appid, stat_name, value) VALUES (%s, %s, %s, %s)",
					(myId, gId, aux['name'], aux['value']))
				
def insertOwned (db):
	jzimOwned = getDirFilesNames('../data/owned')
	cursor = db.cursor()
	
	for jName in jzimOwned:
		with codecs.open(normalizePath('../data/owned/' + jName), 'r', 'utf-8') as fR:
			jzim = json.load(fR)
			fR.close()
		myId = jName[:-5]
		print "\r" + myId, 
		for gId, info in jzim.iteritems():
			cursor.execute("INSERT INTO owned(steamid, appid, playtime_forever, playtime_2weeks) VALUES (%s, %s, %s, %s)",
				(myId, gId, info['playtime_forever'], info['playtime_2weeks']))

def insertNews (db):
	files = getDirFilesNames('../data/news')
	cursor = db.cursor()
	for f in files:
		with codecs.open(normalizePath('../data/news/' + f), 'r', 'utf-8') as fo:
			news = json.load(fo)
			fo.close()
		appid = f[:-5]
		print "\r" + appid, 
		for info in news['newsitems']:
			cursor.execute('INSERT INTO `news` (`appid`, `gid`, `title`, `url`, `is_external_url`, `author`,' +
				' `contents`, `feedlabel`, `date`, `feedname`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
				(appid, info['gid'], info['title'], info['url'], info['is_external_url'], info['author'],
					info['contents'], info['feedlabel'], info['date'], info['feedname']))

def insertDevelopers (db):
	files = getDirFilesNames('../data/developers')
	cursor = db.cursor()
	for f in files:
		with codecs.open(normalizePath('../data/developers/' + f), 'r', 'utf-8') as fo:
			dev = json.load(fo)
			fo.close()
		for name, games in dev.iteritems():
			for game in games:
				cursor.execute('INSERT INTO `developers` (`dev_name`, `appid`) VALUES (%s, %s)', (name, game))

def insertPublishers (db):
	files = getDirFilesNames('../data/publishers')
	cursor = db.cursor()
	for f in files:
		with codecs.open(normalizePath('../data/publishers/' + f), 'r', 'utf-8') as fo:
			pub = json.load(fo)
			fo.close()
		for name, games in pub.iteritems():
			for game in games:
				cursor.execute('INSERT INTO `publishers` (`pub_name`, `appid`) VALUES (%s, %s)', (name, game))

host = 'localhost'
user = 'root'
pw = 'ibdsteamUFMG'
dbName = 'steam'

db = MySQLdb.connect(host, user, pw, dbName, charset='utf8', use_unicode=True)

cursor = db.cursor()

cursor.execute('SET NAMES utf8mb4')
cursor.execute("SET CHARACTER SET utf8mb4")
cursor.execute("SET character_set_connection=utf8mb4")

try:
	# print('Inserting countries...')
	# insertCountries(db)
	# print('Inserting summaries...')
	# insertSummaries(db)
	# print('Inserting friends...')
	# insertFriends(db)
	# print('Inserting details...')
	# insertDetails(db)
	# print('Inserting achievements and stats...')
	# insertAchievementsAndStats(db)
	# # print('Inserting player achievements...')
	# # insertPlayerAchievements(db)
	print('Inserting player stats...')
	insertPlayerStats(db)
	print('Inserting owned...')
	insertOwned(db)
	print('Inserting news...')
	insertNews(db)
	print('Inserting developers...')
	insertDevelopers(db)
	print('Inserting publishers...')
	insertPublishers(db)
	db.commit()
except MySQLdb.Error, e:
	db.rollback()
	try:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	except IndexError:
		print "MySQL Error: %s" % e
	raise
except:
	raise

db.close()
