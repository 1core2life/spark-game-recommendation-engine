from pyspark import SparkContext
from pyspark.mllib.recommendation import ALS, Rating
from getGameData import getGameTitle

GAME_USER_DATA_PATH = "./data/game_user_data_filtered.csv"


def parse_rating(line):
    # Parsing SteamID,AppID,Rating
    line = line.split(',')
    return Rating(int(line[0]), int(line[1]), float(line[2]))


# Train and evaluate an ALS recommender.
def train():
    # Set up environment
    sc = SparkContext("local[*]", "recommendationEngine")

    # Load and parse the data
    data = sc.textFile(GAME_USER_DATA_PATH)
    ratings = data.map(parse_rating)

    # Build the recommendation model using Alternating Least Squares
    rank = 8
    iterations = 10
    model = ALS.train(ratings, rank, iterations)

    # Evaluate the model on training data
    testdata = ratings.map(lambda p: (p[0], p[1]))
    predictions = model.predictAll(testdata).map(lambda r: ((r[0], r[1]), r[2]))
    rates_and_preds = ratings.map(lambda r: ((r[0], r[1]), r[2])).join(predictions)
    MSE = rates_and_preds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
    print("Mean Squared Error = " + str(MSE) + "\n")
    
    print("***** Top 10 Recommendations *****")
    userID = 1
    recommendations = model.recommendProducts(userID, 10)

    # row : steamid , userid , rating
    for row in recommendations:
        print(getGameTitle(row[2]))
    
    print("***** Train stopped *****")

if __name__ == "__main__":
    train()

