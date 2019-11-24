# Recommendation Engine With PySpark (Not Yet Complete)

This is recommendation opensource with python + spark. The source is only for studying. So it is clumsy code :>


### 1. Dataset

- User playtime data : it depend on how many user play the game 
. /data/game_user_data.csv  
. link : https://drive.google.com/drive/folders/1ESRLG9heVA5K4e0wYchkdi8KpqKOmh_b?usp=sharing  
. source : https://github.com/raghavjajodia/steamGameRec  
. form : index , steamid , appid , playtime

- User playtime data filtered : filtered upper playtime data  
. /data/game_user_data_filtered.csv  
. form : steamID , appID , playtime  

- Game average playtime data  
. From steamspy api
. /data/game_average_data.csv  
. form : steamID , playtime



### 2. Dataset preprocessing

- if user's game playtime is more than average playtime, user recommend the game. 
- if no more than average, not recommend


- ★☆☆☆☆(1) = 0 < playtime < average/4
- ★★☆☆☆(2) = average/4 <= playtime < average*3/4 
- ★★★☆☆(3) = average*3/4 <= playtime < average*5/4
- ★★★★☆(4) = average*5/4 <= playtime < average*7/4
- ★★★★★(5) = average*7/4 <= playtime



### 3. Execution

> python model.py


### 4. Process

1. preprocessUserData() : game_user_data.csv -> game_user_data_filtered.csv
2. makeGameAveragePlayTime() : crawl 'game_average_data.csv'  
3. addGameAverageByUserData() : add average to calculated by user data into 'game_average_data.csv' 


3. getUserDataRating() : game_user_data_filtered.csv -> game_user_data_rating.csv
4. train() : Train Model with pyspark

