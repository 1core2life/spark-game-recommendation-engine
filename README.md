# Recommendation Engine With PySpark

This is recommendation opensource with python + spark. The source is only for studying. So it is a little immature code :>


### 1. Dataset

- User playtime data : it depend on how many user play the game 
. /data/game_user_data.csv  
. link : https://drive.google.com/drive/folders/1ESRLG9heVA5K4e0wYchkdi8KpqKOmh_b?usp=sharing  
. data source : https://github.com/raghavjajodia/steamGameRec  
. form : index , steamid(user) , appid(game) , playtime

- User playtime data filtered : filtered upper playtime data  
. /data/game_user_data_filtered.csv  
. form : steamid , appid , playtime  

- Game average playtime data : Average time of game
. /data/game_average_data.csv  
. form : appid , playtime

- User playtime data with rating : converting playtime to rating
. /data/game_average_data.csv  
. form : appid , playtime



### 2. Dataset preprocessing

- user's rating is defined by playtime

> ★☆☆☆☆(1) = 0 < playtime < average/4
> ★★☆☆☆(2) = average/4 <= playtime < average*3/4 
> ★★★☆☆(3) = average*3/4 <= playtime < average*5/4
> ★★★★☆(4) = average*5/4 <= playtime < average*7/4
> ★★★★★(5) = average*7/4 <= playtime



### 3. Execution

> python model.py : create model
> python predict.py : execute prediction with example user


### 4. Process

1. preprocessUserData() : game_user_data.csv -> game_user_data_filtered.csv
2. addGameAverageByUserData() : Add average playtime by appid with game_user_data_filtered.csv
3. getUserDataRating() : game_user_data_filtered.csv -> game_user_data_rating.csv
4. train() : Train Model with pyspark

