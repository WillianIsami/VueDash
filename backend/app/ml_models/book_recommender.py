import pandas as pd
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity

class BookRecommender:
    def __init__(self):
        self.books_df = None
        self.users_df = None
        self.ratings_df = None
        self.user_book_matrix = None
        self.book_similarity_matrix = None
        self.book_indices = None
        
    def load_data(self, books_path, users_path, ratings_path):
        """Load and prepare the datasets"""
        self.books_df = pd.read_csv(books_path)
        self.users_df = pd.read_csv(users_path)
        self.ratings_df = pd.read_csv(ratings_path, nrows=300_000)
        
        # Merge ratings with book information
        self.ratings_df = self.ratings_df.merge(
            self.books_df[['ISBN', 'Book-Title', 'Book-Author']], 
            on='ISBN'
        )
        
    def prepare_user_book_matrix(self, min_book_ratings=5, min_user_ratings=5):
        """Create user-book rating matrix with minimum rating thresholds"""
        # Filter based on minimum ratings
        book_stats = self.ratings_df['ISBN'].value_counts()
        user_stats = self.ratings_df['User-ID'].value_counts()
        
        popular_books = book_stats[book_stats >= min_book_ratings].index
        active_users = user_stats[user_stats >= min_user_ratings].index
        
        filtered_ratings = self.ratings_df[
            self.ratings_df['ISBN'].isin(popular_books) & 
            self.ratings_df['User-ID'].isin(active_users)
        ]
        
        # Create user-book matrix
        self.user_book_matrix = filtered_ratings.pivot(
            index='User-ID',
            columns='ISBN',
            values='Book-Rating'
        ).fillna(0)
        
        # Create book similarity matrix
        self.book_similarity_matrix = cosine_similarity(self.user_book_matrix.T)
        self.book_indices = {isbn: idx for idx, isbn in enumerate(self.user_book_matrix.columns)}
        
    def get_similar_books(self, isbn, limit=5, offset=0):
        """Get similar books based on user rating patterns"""
        if isbn not in self.book_indices:
            return []
            
        idx = self.book_indices[isbn]
        sim_scores = list(enumerate(self.book_similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:]

        sim_scores_paginated = sim_scores[offset:offset + limit]
        book_indices = [i[0] for i in sim_scores_paginated]
        recommended_isbns = self.user_book_matrix.columns[book_indices]
        
        recommendations = []
        for rec_isbn in recommended_isbns:
            book_info = self.books_df[self.books_df['ISBN'] == rec_isbn].iloc[0]
            recommendations.append({
                'ISBN': rec_isbn,
                'Title': book_info['Book-Title'],
                'Author': book_info['Book-Author'],
                'Year': book_info['Year-Of-Publication'],
                'Similarity Score': sim_scores[book_indices.index(self.book_indices[rec_isbn])][1],
                'Image-URL-S': book_info['Image-URL-S'],
                'Image-URL-M': book_info['Image-URL-M'],
                'Image-URL-L': book_info['Image-URL-L'],
            })
            
        return recommendations
    
    def get_user_recommendations(self, user_id, limit=5, offset=0):
        """Get personalized book recommendations for a user"""
        if user_id not in self.user_book_matrix.index:
            return []
            
        user_ratings = self.user_book_matrix.loc[user_id]
        rated_books = user_ratings[user_ratings > 0].index
        
        # Calculate weighted recommendations
        weighted_scores = np.zeros(len(self.user_book_matrix.columns))
        for book in rated_books:
            idx = self.book_indices[book]
            rating = user_ratings[book]
            weighted_scores += self.book_similarity_matrix[idx] * rating
            
        # Remove already rated books
        weighted_scores[np.array([self.book_indices[isbn] for isbn in rated_books])] = -1
        
        # Get top recommendations
        top_indices = weighted_scores.argsort()[::-1][offset:offset + limit]
        recommended_isbns = self.user_book_matrix.columns[top_indices]
        
        recommendations = []
        for rec_isbn in recommended_isbns:
            book_info = self.books_df[self.books_df['ISBN'] == rec_isbn].iloc[0]
            recommendations.append({
                'ISBN': rec_isbn,
                'Title': book_info['Book-Title'],
                'Author': book_info['Book-Author'],
                'Year': book_info['Year-Of-Publication'],
                'Predicted Rating': weighted_scores[self.book_indices[rec_isbn]],
                'Image-URL-S': book_info['Image-URL-S'],
                'Image-URL-M': book_info['Image-URL-M'],
                'Image-URL-L': book_info['Image-URL-L'],
            })
            
        return recommendations

    def recommend_for_new_user(self, limit=5, offset=0):
        """Recommend books for a new user who has not rated any books"""
        # Get popular books (e.g., books with most ratings)
        book_counts = self.ratings_df['ISBN'].value_counts()
        popular_books = book_counts.index[offset:offset + limit]
        
        recommendations = []
        for isbn in popular_books:
            book_info = self.books_df[self.books_df['ISBN'] == isbn].iloc[0]
            recommendations.append({
                'ISBN': isbn,
                'Title': book_info['Book-Title'],
                'Author': book_info['Book-Author'],
                'Year': book_info['Year-Of-Publication'],
                'Image-URL-S': book_info['Image-URL-S'],
                'Image-URL-M': book_info['Image-URL-M'],
                'Image-URL-L': book_info['Image-URL-L'],
            })
        
        return recommendations

    def save_model(self, filepath):
        """Save the recommender model and data to a file"""
        joblib.dump(self, filepath)

    @staticmethod
    def load_model(filepath):
        """Load the recommender model and data from a file"""
        return joblib.load(filepath)