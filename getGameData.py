import requests
import os
from collections import defaultdict
from time import sleep
from util import *


GAME_USER_DATA_PATH = "./data/game_user_data.csv"
GAME_USER_DATA_FILTERED_PATH = "./data/game_user_data_filtered.csv"
GAME_AVERAGE_DATA_PATH = "./data/game_average_data.csv"
GAME_USER_DATA_RATING_PATH = "./data/game_user_data_rating.csv"


def getUserDataRating():
    averageData = getAvaerageFile()

    file = open(GAME_USER_DATA_FILTERED_PATH, 'r')
    lines = file.readlines()
    
    filteredData = []
    
    for li in lines:
        filtered = li.split(',')

        steamid = filtered[0]
        appid = filtered[1]
        playtime = int(filtered[2])
        rating = getRating(playtime, averageData[appid])
        
        string = str(steamid) + ',' + str(appid) + ',' + str(rating)
        
        filteredData.append(string)

    file.close()

    print("***** Start writing rating data *****")

    file = open(GAME_USER_DATA_RATING_PATH, 'w+')
    for i in filteredData:
        file.write(i + '\n')

    file.close()


def addGameAverageByUserData():      
    # Load User's playtime data by appid
    file = open(GAME_USER_DATA_FILTERED_PATH, 'r')
    lines = file.readlines()
    userData = defaultdict(list)

    for li in lines:
        filtered = li.split(',')

        appid = filtered[1]
        playtime = int(str(filtered[2]).replace("\n",""))
        
        userData[appid].append(playtime)

    file.close()

    print("***** All User Playtime Loaded *****")

    data = dict()

    index = 0
    for key, vals in userData.items():
        average = sum(vals) / len(vals) 
        data[key] = int(average)

        index += 1

    print("All Data Length :",str(index))
    print("***** Start Added average data ! *****")

    file = open(GAME_AVERAGE_DATA_PATH, 'w+')
    for key,val in data.items():
        file.write(str(key) + ',' + str(val) + '\n')

    file.close()

    print("***** All average playtime added ! *****")

    
def preprocessUserData():
    print("***** Start filtering raw data *****")

    file = open(GAME_USER_DATA_PATH, 'r')
    lines = file.readlines()
    
    # Remove Columns name
    lines.pop(0)

    filteredData = []

    # steamid is too large, so re-indexing filtered[0] to 'idx' val
    idx = 0
    
    # value to check whether new row have new steamid or not
    prevSteamId = lines[0].split(',')[1]

    for li in lines:
        filtered = li.split(',')
        filtered.pop(0)
        
        if prevSteamId != filtered[0]:
            idx = idx + 1
            prevSteamId = filtered[0]
    
        first = str(idx)
        second = filtered[1]
        third = str( (int(filtered[2], base=10) / 60 ) )

        string = first + ',' + second + ',' + third + '\n'

        filteredData.append(string)

    file.close()


    print("***** Start writing filtered data *****")

    file = open(GAME_USER_DATA_FILTERED_PATH, 'w')
    for i in filteredData:
        file.write(i)

    file.close()

    

    