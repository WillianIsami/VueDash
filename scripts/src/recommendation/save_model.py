from model import BookRecommender

recommender = BookRecommender()
recommender.load_data('data/filtered/FilteredBooks.csv', 'data/filtered/FilteredUsers.csv', 'data/filtered/FilteredRatings.csv')
recommender.prepare_user_book_matrix()
recommender.save_model('book_recommender_model.pkl')