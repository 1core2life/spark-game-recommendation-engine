import requests
import os

GAME_AVERAGE_DATA_PATH = "./data/game_average_data.csv"



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
    file = open(GAME_AVERAGE_DATA_PATH, 'r')
    lines = file.readlines()

    averageFile = dict()
    for li in lines:
        filtered = li.split(',')
        averageFile[filtered[0]] = int(filtered[1])
    
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

