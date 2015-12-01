import random, json, os, sys, glob

def normalizePath (path):
    abspath = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.abspath(abspath + '/' + path) + ('/' if path[-1] == '/' else '')

def getDirFilesNames (path):
    files = []
    for name in glob.glob(normalizePath(path) + '/*.json'):
        files.append(os.path.basename(name)[:-5])
    return files

def randomIds(size):
    rtn = set()
    while len(rtn) < size:
        newUser = '999' + str(random.randint(11111111111111, 99999999999999))
        rtn.add(newUser)
    return list(rtn)

def randomUserNames(randomIds):
    fname = open('12mil.txt', 'r')
    rtn = {}
    i = 0
    mx = len(randomIds)
    for name in fname:
        rtn[randomIds[i]] = name[:-1]
        #print rtn
        i = i + 1
        if i == mx:
            break
    fname.close()
    return rtn

#Funcao para Amigos


def friendList(myId, all_Users):
    print('friends for ' + str(myId))
    nUsers = len(all_Users)
    nFriends = random.randint(2, 50)
    jzim = {}
    used = [myId]
    while nFriends>0:
        rnd = random.randint(0, nUsers-1)
        friendId = all_Users[rnd]
        if friendId not in used:
            aux = {"steamid": friendId, "friend_since": random.randint(998307200, 1246422390)}
            jzim[friendId] = aux
            nFriends = nFriends - 1
    fOut = open(normalizePath('../data/new_friends/') + str(myId) + '.json', 'w')
    json.dump(jzim, fOut)
    fOut.close()

def friendsGenerator(all_Ids):
    friends = dict.fromkeys(all_Ids, {})
    for i, uid in enumerate(all_Ids):
        print('[' + str(i) + '] friends for ' + str(uid))
        ids = set([ k for k in all_Ids if k not in friends[uid] and k != uid ])
        for _ in range(random.randint(0, len(ids))):
            friend = random.sample(ids, 1)
            friends[uid][friend] = { 'steamid': friend, 'friend_since': random.randint(998307200, 1246422390) }
            ids.remove(friend)
    for uid in all_Ids:
        with open(normalizePath('../data/new_friends/') + str(uid) + '.json', 'w') as fo:
            json.dump(friends[uid], fo)
            fo.close()

def userGames(all_Ids, allGames):
    ownedGames = len(allGames)
    for myId in all_Ids:
        print('games for ' + str(myId))
        nGames = random.randint(2, 5)
        jzim = {}
        used = []
        while nGames>0:
            rnd = random.randint(0, ownedGames-1)
            gameId = random.choice(allGames)
            if gameId not in used:
                used.append(gameId)
                playedTime = random.randint(123, 5000)
                aux = {"playtime_2weeks": random.randint(0, 100) if random.random() > 0.7 else 0, "playtime_forever": playedTime}
                jzim[gameId] = aux
                nGames = nGames - 1
                fOut = open(normalizePath('../data/new_owned/') + str(myId) + '.json', 'w')
                json.dump(jzim, fOut)
                fOut.close()
        #aproveitar o used
        fOut = open(normalizePath('../data/new_achievements/') + str(myId) + '.json', 'w')
        fOut2 = open(normalizePath('../data/new_stats/') + str(myId) + '.json', 'w')
        acv = {}
        sts = {}
        for game in used:
            aTemp, sTemp = getAchievements(game)
            if len(aTemp)>0:
                acv[game] = aTemp
                sts[game] = sTemp
        json.dump(acv, fOut)
        fOut.close()
        json.dump(sts, fOut2)
        fOut2.close()
#

def getAchievements(game):#retorna lista de achievements e lista de stats
    #gerar para um usuario
    fR = open(normalizePath('../data/schema/') + game + '.json', 'r')
    jzim = json.loads(fR.read())
    fR.close()
    allAchievements = jzim['achievements']
    nAchv = len(allAchievements)
    achievements = []
    stats = []
    if nAchv>0:
        i = random.randint(0, nAchv-1)
        used = []
        while i>0:
            nRand = random.randint(0, nAchv-1)
            if nRand not in used:
                used.append(nRand)
                achievements.append({"achieved": 1, "name": allAchievements[nRand]['name']})
                stats.append({"value": random.uniform(0, 256), "name": allAchievements[nRand]['name']})
                i = i - 1    
    #else:
        #print 'Nao tenho achievements...'#'Name of Game: ', allAchievements[0]['name']
        #Neste caso, e retornado um dicionario vazio...
        #achievements.append({"achieved": 1, "name": allAchievements[i]['name']})
        #stats.append({"value": 2222, "name": allAchievements[i]['name']})
    return achievements, stats

def getCountriesCode():
    countriesList = getDirFilesNames('../data/countries')
    codesList = []
    #nContryCodes = len(countriesList)
    for country in countriesList:
        fR = open(normalizePath('../data/countries/') + country + '.json', 'r')
        jzim = json.loads(fR.read())
        fR.close()
        codesList.append(jzim["loccountrycode"])
    return codesList

def summaryCreator(myId, myName):
    print('summary for ' + str(myId))
    #print 'SCreator Recebi: ', myId
    #print 'Nome: ', myName
    timecreated = random.randint(978307200, 1446422399)
    summUser = {}
    summUser['loccountrycode'] = random.choice(getCountriesCode())
    summUser['lastlogoff'] = random.randint(timecreated, 1448927999)
    summUser['personastateflags'] = 0
    summUser['profileurl'] = 'http://steamcommunity.com/profiles/' + str(myId) + '/'
    summUser['profilestate'] = 1
    summUser['avatar'] = 'http://homepages.dcc.ufmg.br/~marcoantonio/random_image.php?s=small&sid=' + str(myId)
    summUser['avatarfull'] = 'http://homepages.dcc.ufmg.br/~marcoantonio/random_image.php?s=large&sid=' + str(myId)
    summUser['personaname'] = myName
    summUser['communityvisibilitystate'] = 3
    summUser['steamid'] = myId
    summUser['timecreated'] = timecreated
    summUser['personastate'] = 3
    summUser['avatarmedium'] = 'http://homepages.dcc.ufmg.br/~marcoantonio/random_image.php?s=medium&sid=' + str(myId)
    fW = open(normalizePath('../data/new_summaries/') + str(myId) + '.json', 'w')
    json.dump(summUser, fW)
    fW.close()

def main(nUsers):    
    allUsersId = randomIds(nUsers)#total de nomes diferentes que tenho no arquivo: 12mil.txt
    friendsGenerator(allUsersId)
    usersIdName = randomUserNames(allUsersId)
    allGamesList = getDirFilesNames('../data/details')
    userGames(allUsersId, allGamesList)
    
    for myId in allUsersId:
        #print 'nomes: '+myId+', Nome: '+str(usersIdName[myId])
        summaryCreator(myId, usersIdName[myId])
    print 'FIM!'

main(int(sys.argv[1]) if len(sys.argv) > 1 else 12000)

exit