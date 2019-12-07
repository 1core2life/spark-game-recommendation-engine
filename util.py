import requests
import os

GAME_AVERAGE_DATA_PATH = "./data/game_average_data.csv"
GAME_USER_DATA_PATH = "./data/game_user_data_filtered.csv"
GAME_AVERAGE_DATA_ADDED_PATH = "./data/game_average_data_added.csv"
GAME_APPID_ALL_PATH = "./data/game_appid_all.txt"

CRAWLING_ERROR_CODE = -2
DEFAULT_CODE = -1


def parseRating(line):
    # Parsing SteamID,AppID,Rating
    line = line.split(',')
    return Rating(int(line[0]), int(line[1]), float(line[2]))


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
    file = open(GAME_AVERAGE_DATA_ADDED_PATH, 'r')
    lines = file.readlines()

    averageFile = dict()
    for li in lines:
        filtered = li.split(',')
        averageFile[filtered[0]] = filtered[1]
    
    file.close()
    
    return averageFile


def getGameTitle(appid):
    appid = str(appid)
    URL = 'https://store.steampowered.com/api/appdetails/?appids='
    URL += appid

    response = requests.get(URL)
    obj = response.json()

    if 'data' in obj[appid]:
        return obj[appid]['data']['name']
    else:
        return appid


def getAllGames():
    obj = dict()

    file = open(GAME_APPID_ALL_PATH, "r")
    lines = file.readlines()
    
    for appid in lines:
        appid = appid.replace("\n","")
        obj[appid] = DEFAULT_CODE

    return obj


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
        print(appid)
        return int(obj['average_forever'] / 60)
    except:
        print("Error: ", appid)
        return CRAWLING_ERROR_CODE


