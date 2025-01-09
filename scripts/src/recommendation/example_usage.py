import time 
from model import BookRecommender

recommender = BookRecommender.load_model('notebooks/book_recommender_model.pkl')

user_id = 114
recommendations = recommender.get_user_recommendations(user_id)
print(recommendations)
while True:
    time.sleep(1)
    user_id = int(input("Insert the userID: "))
    recommendations = recommender.get_user_recommendations(user_id)
    print("\nRecommendations:\n", recommendations)
    if user_id == 0:
        print("turning off")
        break
