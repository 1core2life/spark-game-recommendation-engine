from pyspark import SparkContext
from pyspark.mllib.recommendation import ALS, Rating, MatrixFactorizationModel
from util import getGameTitle, parseRating


TRAINED_MODEL_PATH = "./data/"


def predict():
    sc = SparkContext("local[*]", "recommendationEngine")
    print("***** Load Trained Model *****")
    model = MatrixFactorizationModel.load(sc, TRAINED_MODEL_PATH)
    
    print("***** Top 10 Recommendations *****")
    userID = 1
    recommendations = model.recommendProducts(userID, 10)

    # row : steamid , userid , rating
    for row in recommendations:
        print(getGameTitle(row[1]),":",row[2])
    
    
if __name__ == "__main__":
    predict()

    
    