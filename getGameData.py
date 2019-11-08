import requests
import os
from collections import defaultdict

GAME_AVERAGE_DATA_PATH = "./data/game_average_data.csv"
GAME_USER_DATA_PATH = "./data/game_user_data_filtered.csv"


def getGameTitle(appid):
    appid = str(appid)
    URL = 'https://store.steampowered.com/api/appdetails/?appids='
    URL += appid
    response = requests.get(URL)
    obj = response.json()

    return obj[appid]['data']['name']


def getAllGames():
    URL = 'http://api.steampowered.com/ISteamApps/GetAppList/v0002/'
    response = requests.get(URL)
    obj = response.json()

    return obj


def addGameAverageByUserData():
    # Load Game average playtime data
    file = open(GAME_AVERAGE_DATA_PATH, 'r')
    lines = file.readlines()

    data = dict()
    for li in lines:
        appid , average = li.split(',')
        data[appid] = average
    
    file.close()
    
    # Load User's playtime data by appid
    file = open(GAME_USER_DATA_PATH, 'r')
    lines = file.readlines()
    userData = defaultdict(list)

    for li in lines:
        filtered = li.split(',')

        appid = filtered[1]
        playtime = filtered[2]
        
        userData[appid].append(playtime)

    file.close()
    
    for key, vals in userData.items():
        if data[key] == 0:
            average = sum(vals, 0.0) / len(vals) 
            userData[appid] = average

    print("***** All average playtime added ! *****")


def getPrevId():
    if os.path.isfile(GAME_AVERAGE_DATA_PATH):
        file = open(GAME_AVERAGE_DATA_PATH, 'r')
        last = file.readlines()[-1]
        file.close()
        
        return last.split(',')[0]
    else:
        file = open(GAME_AVERAGE_DATA_PATH, 'w')
        file.write('')
        file.close()
        
        return None


def makeGameAveragePlayTime():
    obj = getAllGames()
    prev = getPrevId()

    data = dict()

    loopIndex = 0
    
    for ob in obj['applist']['apps']:
        appid = str(ob['appid'])

        # If prev data exists, start from the last
        if prev != None:
            if appid == prev :
                print("Starting from", appid)
                prev = None
            continue
        
        URL = 'https://steamspy.com/api.php?request=appdetails&appid='
        URL += appid

        response = requests.get(URL)
        obj = response.json()

        data[appid] =int(obj['average_forever'] / 60)
        
        loopIndex += 1
        if (loopIndex%1000) == 0:
            print(loopIndex)
            break

    file = open(GAME_AVERAGE_DATA_PATH, 'a')
    for key,val in data.items():
        file.write(str(key) + ',' + str(val) + '\n')

    file.close()


if __name__ == "__main__":
    makeGameAveragePlayTime()    

    

    

    