import requests
import os
from collections import defaultdict

GAME_AVERAGE_DATA_PATH = "./data/game_average_data.csv"
GAME_USER_DATA_PATH = "./data/game_user_data_filtered.csv"
GAME_AVERAGE_DATA_ADDED_PATH = "./data/game_average_data_added.csv"
GAME_APPID_ALL_PATH = "./data/game_appid_all.txt"


def getRating(playtime, averageTime):

    if playtime == 0:
        return 0
    elif 0 < playtime < averageTime/4 :
        return 1
    elif averageTime/4 <= playtime < averageTime*3/4 :
        return 2
    elif averageTime*3/4 <= playtime < averageTime*5/4 :
        return 3
    elif averageTime*5/4 <= playtime < averageTime*7/4 :
        return 4
    else:
        return 5


def getAvaerageFile():
    file = open('./data/game_average_data_added.csv', 'r')
    lines = file.readlines()

    averageFile = dict()
    for li in lines:
        filtered = li.split(',')
        averageFile[filtered[0]] = filtered[1]
    
    file.close()
    
    return averageFile


def getUserDataRating():
    averageData = getAvaerageFile()

    file = open('./data/game_user_data_filtered.csv', 'r')
    lines = file.readlines()
    
    filteredData = []
    
    for li in lines:
        filtered = li.split(',')

        steamid = filtered[0]
        appid = filtered[1]
        playtime = filtered[2]
        rating = getRating(playtime, averageData[appid])
        
        string = str(steamid) + ',' + str(appid) + ',' + str(rating)
        
        filteredData.append(string)

    file.close()

    print("***** Start writing rating data *****")

    file = open("./data/game_user_data_rating.csv", 'w')
    for i in filteredData:
        file.write(i)

    file.close()


def preprocessUserData():
    print("***** Start filtering raw data *****")

    file = open("./data/game_user_data.csv", 'r')
    lines = file.readlines()
    
    # Remove Columns name
    lines.pop(0)

    filteredData = []

    # steamid is too large, so re-indexing filtered[0] to 'idx' val
    idx = 0
    
    # value to check whether new row have new steamid or not
    global prevSteamId 
    prevSteamId = lines[0].split(',')[1]

    for li in lines:
        filtered = li.split(',')
        filtered.pop(0)
        
        if prevSteamId != filtered[0]:
            idx = idx + 1
            prevSteamId = filtered[0]
    
        first = str(idx)
        second = filtered[1]
        third = str( int(int(filtered[2], base=10) / 60) ) 

        string = first + ',' + second + ',' + third + '\n'

        filteredData.append(string)

    file.close()


    print("***** Start writing filtered data *****")

    file = open("./data/game_user_data_filtered.csv", 'w')
    for i in filteredData:
        file.write(i)

    file.close()


def getGameTitle(appid):
    appid = str(appid)
    URL = 'https://store.steampowered.com/api/appdetails/?appids='
    URL += appid
    response = requests.get(URL)
    obj = response.json()

    return obj[appid]['data']['name']


def getAllGames():
    obj = dict()

    file = open(GAME_APPID_ALL_PATH, "r")
    lines = file.readlines()
    
    for appid in lines:
        appid = appid.replace("\n","")
        obj[appid] = -1

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
        playtime = str(filtered[2]).replace("\n","")
        
        userData[appid].append(playtime)

    file.close()
    
    for key, vals in userData.items():
        if data[key] == 0:
            average = sum(vals, 0.0) / len(vals) 
            data[appid] = average

    print("***** Start Added average data ! *****")

    file = open(GAME_AVERAGE_DATA_ADDED_PATH, 'w')
    for key,val in data.items():
        file.write(str(key) + ',' + str(val) + '\n')

    file.close()

    print("***** All average playtime added ! *****")


def getPrevs(obj):
    file = open(GAME_AVERAGE_DATA_PATH, 'r')
    lines = file.readlines()
    file.close()
    
    for line in lines:
        appid, time = line.split(",")
        obj[appid] = int(time)    

    return obj


def getAverageTime(appid):
    URL = 'https://steamspy.com/api.php?request=appdetails&appid='
    URL += appid

    response = requests.get(URL)

    try:
        obj = response.json()
    except:
        print(response)

    return int(obj['average_forever'] / 60)


def makeGameAveragePlayTime():
    obj = getAllGames()
    obj = getPrevs(obj)

    loopIndex = 0
    
    for appid,time in obj.items():
        if time != -1:
            continue

        obj[appid] = getAverageTime(appid)
        print(appid,obj[appid])
        
        loopIndex += 1
        if (loopIndex%40000) == 0:
            print(loopIndex)
            break

    file = open(GAME_AVERAGE_DATA_PATH, 'w')
    for key,val in obj.items():
        file.write(str(key) + ',' + str(val) + "\n")

    file.close()


if __name__ == "__main__":
    makeGameAveragePlayTime()    

    

    

    