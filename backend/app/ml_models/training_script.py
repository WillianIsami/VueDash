from app.core.config import settings
from app.ml_models.book_recommender import BookRecommender

recommender = BookRecommender()
recommender.load_data('app/data/filtered/FilteredBooks.csv', 'app/data/filtered/FilteredUsers.csv', 'app/data/filtered/FilteredRatings.csv')
recommender.prepare_user_book_matrix()
recommender.save_model(settings.MODEL_PATH)