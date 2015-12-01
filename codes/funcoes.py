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
    rtn = []
    for _ in range(size):
        newUser = '999' + str(random.randint(11111111111111, 99999999999999))
        if newUser not in rtn:
            rtn.append(newUser)
    return rtn

def randomUserNames(randomIds):
    fname = open('12mil.txt', 'r')
    rtn = {}
    i = 0
    mx = len(randomIds)
    for name in fname:
        rtn[randomIds[i]] = name[:(len(name)-1)]
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

def friendsGenerator(amount, all_Ids):
    used = []
    size = len(all_Ids)
    if size > 12000:
        print 'So gera 12 mil! Necessario um arquivo com nomes de pessoas maior que 12 mil...'
        size = 12000
    
    while amount>0:
        rnd = random.randint(0, size-1)
        myId = all_Ids[rnd]
        if myId not in used:
            used.append(myId)
            friendList(myId, all_Ids)
            amount = amount - 1
    return used

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
    summUser = {'timecreated': random.randint(978307200, 1446422399)}

    summUser['loccountrycode'] = random.choice(getCountriesCode())
    summUser['lastlogoff'] = random.randint(summUser['timecreated'], 1448927999)
    summUser['personastateflags'] = 0
    summUser['profileurl'] = 'http://steamcommunity.com/profiles/'+str(myId)+'/'
    summUser['profilestate'] = 1
    summUser['avatar'] = 'http://homepages.dcc.ufmg.br/~marcoantonio/random_image.php?s=small&sid='+str(myId)
    summUser['avatarfull'] = 'http://homepages.dcc.ufmg.br/~marcoantonio/random_image.php?s=large&sid='+str(myId)
    summUser['personaname'] = myName
    summUser['communityvisibilitystate'] = 3
    summUser['steamid'] = myId
    # timecreated
    summUser['personastate'] = 3
    summUser['avatarmedium'] = 'http://homepages.dcc.ufmg.br/~marcoantonio/random_image.php?s=medium&sid='+str(myId)
    fW = open(normalizePath('../data/new_summaries/') + str(myId) + '.json', 'w')
    json.dump(summUser, fW)
    fW.close()

def main(nUsers):    
    allUsersId = randomIds(nUsers)#total de nomes diferentes que tenho no arquivo: 12mil.txt
    usersId = friendsGenerator(nUsers, allUsersId)
    usersIdName = randomUserNames(usersId)
    allGamesList = getDirFilesNames('../data/details')
    userGames(usersId, allGamesList)
    #print 'UsersId: ', usersId
    #print 'Um id que foi usado: ', usersId[0]
    #print 'Nome desse ID: ', usersIdName[usersId[0]]
    
    #print len(usersId)
    #print 'UltimoElemento: ', usersId[len(usersId)-1]
    #print 'NomeDoUltimo: ', usersIdName[usersId[len(usersId)-1]]
    
    for myId in usersId:
        #print 'nomes: '+myId+', Nome: '+str(usersIdName[myId])
        summaryCreator(myId, usersIdName[myId])
    print 'FIM!'

main(int(sys.argv[1]) if len(sys.argv) > 1 else 12000)

exit