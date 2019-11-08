# Happy New Year Files

def getRating():
    
    return appid, playtime


def getUserDataRating():
    file = open('./data/game_user_data_filtered.csv', 'r')
    lines = file.readlines()

    filteredData = []
    
    for li in lines:
        filtered = li.split(',')

        steamid = filtered[0]
        appid = filtered[1]
        playtime = filtered[2]
        rating = getRating(appid, playtime)
        
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
    global prevSteamId = lines[0].split(',')[1]

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
