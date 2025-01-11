from pathlib import Path
from app.data_processing.utils.data_cleaning import DataCleaner
from app.db.session import DatabaseManager
from app.core.config import settings

def main():
    # File paths
    data_dir = Path(settings.RAW_DATA_PATH)
    filtered_dir = Path(settings.FILTERED_DATA_PATH)
    
    book_paths = {
        'raw': data_dir / 'Books.csv',
        'filtered': filtered_dir / 'FilteredBooks.csv'
    }
    user_paths = {
        'raw': data_dir / 'Users.csv',
        'filtered': filtered_dir / 'FilteredUsers.csv'
    }
    rating_paths = {
        'raw': data_dir / 'Ratings.csv',
        'filtered': filtered_dir / 'FilteredRatings.csv'
    }

    # Cleaning rules
    cleaning_rules = {
        'books': {
            "drop_duplicates": ["ISBN"],
            "convert": {"Year-Of-Publication": "int"}
        },
        'users': {
            "dropna": ["User-ID"],
            "drop_duplicates": ["User-ID"],
            "remove_zeros": ["Age"]
        },
        'ratings': {
            "dropna": ["User-ID", "ISBN", "Book-Rating"],
            "remove_zeros": ["Book-Rating"]
        }
    }

    # Database table creation queries
    table_queries = {
        'books': """
            CREATE TABLE IF NOT EXISTS books (
                isbn VARCHAR(20) PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year_published INTEGER NOT NULL,
                publisher TEXT NOT NULL,
                img_small VARCHAR(255),
                img_medium VARCHAR(255),
                img_large VARCHAR(255)
            );
        """,
        'user_table_query': """
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(50) PRIMARY KEY,
                location TEXT,
                age VARCHAR(20)
            );
        """,
        'ratings_table_query': """
            CREATE TABLE IF NOT EXISTS ratings (
                user_id VARCHAR(50) REFERENCES users(user_id) ON DELETE CASCADE,
                isbn VARCHAR(20) REFERENCES books(isbn) ON DELETE CASCADE,
                book_rating INT,
                PRIMARY KEY (user_id, isbn)
            );
        """
    }

    column_mapping_queries = {
        'books_column_mappings': {
            'ISBN': 'isbn',
            'Book-Title': 'title',
            'Book-Author': 'author',
            'Year-Of-Publication': 'year_published',
            'Publisher': 'publisher',
            'Image-URL-S': 'img_small',
            'Image-URL-M': 'img_medium',
            'Image-URL-L': 'img_large'
        },
        'users_column_mappings': {
            'User-ID': 'user_id',
            'Location': 'location',
            'Age': 'age'
        },
        'ratings_column_mappings': {
            'User-ID': 'user_id',
            'ISBN': 'isbn',
            'Book-Rating': 'book_rating'
        }
    }

    # Process data
    db_manager = DatabaseManager()
    db_manager.create_connection()

    try:
        # Create tables
        db_manager.create_table(table_queries.values())

        # Process books
        book_cleaner = DataCleaner(book_paths['raw'], book_paths['filtered'])
        book_cleaner.read_csv()
        df_books = book_cleaner.get_clean_data(cleaning_rules['books'])
        db_manager.insert_values_into_table('books', column_mapping_queries['books_column_mappings'], df_books)

        # Process users
        user_cleaner = DataCleaner(user_paths['raw'], user_paths['filtered'])
        user_cleaner.read_csv()
        df_users = user_cleaner.get_clean_data(cleaning_rules['users'])
        db_manager.insert_values_into_table('users', column_mapping_queries['users_column_mappings'], df_users)

        # Process ratings
        rating_cleaner = DataCleaner(rating_paths['raw'], rating_paths['filtered'])
        rating_cleaner.read_csv()
        df_ratings = rating_cleaner.get_clean_data(cleaning_rules['ratings'])

        existing_book_isbns = df_books['ISBN'].unique()
        existing_user_ids = df_users['User-ID'].unique()

        # Filters the classification data to include only records with existing keys
        df_ratings_filtered = df_ratings[
            df_ratings['User-ID'].isin(existing_user_ids) & df_ratings['ISBN'].isin(existing_book_isbns)
        ]
        db_manager.insert_values_into_table('ratings', column_mapping_queries['ratings_column_mappings'], df_ratings_filtered)
        
        # Save data
        df_books.to_csv(book_paths['filtered'], index=False)
        df_users.to_csv(user_paths['filtered'], index=False)
        df_ratings_filtered.to_csv(rating_paths['filtered'], index=False)
        
    finally:
        db_manager.close_connection()

if __name__ == "__main__":
    main()