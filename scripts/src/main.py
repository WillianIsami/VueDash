from data_cleaning import DataCleaner
from db_operations import DatabaseManager

def main():
    book_file_path, book_filtered_file_path = './data/raw/Books.csv', './data/filtered/FilteredBooks.csv'
    user_file_path, user_filtered_file_path = './data/raw/Users.csv', './data/filtered/FilteredUsers.csv'
    rating_file_path, rating_filtered_file_path = './data/raw/Ratings.csv', './data/filtered/FilteredRatings.csv'
    
    book_cleaning_rules = {
        "drop_duplicates": ["ISBN"],
        "convert": {
            "Year-Of-Publication": "int"
        }
    }
    book_data_cleaner = DataCleaner(book_file_path, book_filtered_file_path)
    book_data_cleaner.read_csv()
    df_books = book_data_cleaner.get_clean_data(book_cleaning_rules)

    user_cleaning_rules = {
        "dropna": ["User-ID"],
        "drop_duplicates": ["User-ID"],
        "remove_zeros": ["Age"]
    }
    user_data_cleaner = DataCleaner(user_file_path, user_filtered_file_path)
    user_data_cleaner.read_csv()
    df_users = user_data_cleaner.get_clean_data(user_cleaning_rules)

    rating_cleaning_rules = {
        "dropna": ["User-ID", "ISBN", "Book-Rating"],
        "remove_zeros": ["Book-Rating"]
    }
    ratings_data_cleaner = DataCleaner(rating_file_path, rating_filtered_file_path)
    ratings_data_cleaner.read_csv()
    df_ratings = ratings_data_cleaner.get_clean_data(rating_cleaning_rules)

    table_books = "books"
    table_book_img_url = "book_img_url"
    table_users = "users"
    table_ratings = "ratings"

    # Create table queries
    book_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_books} (
        isbn VARCHAR(20) PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year_published INTEGER NOT NULL,
        publisher TEXT NOT NULL
    );
    """

    auxiliar_book_img_url_query = f"""
    CREATE TABLE IF NOT EXISTS {table_book_img_url} (
        isbn VARCHAR(20) PRIMARY KEY REFERENCES books(isbn) ON DELETE CASCADE,
        small VARCHAR(255),
        medium VARCHAR(255),
        large VARCHAR(255)
    );
    """

    user_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_users} (
        user_id VARCHAR(50) PRIMARY KEY,
        location TEXT,
        age VARCHAR(20)
    );
    """

    ratings_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_ratings} (
        user_id VARCHAR(50) REFERENCES users(user_id) ON DELETE CASCADE,
        isbn VARCHAR(20) REFERENCES books(isbn) ON DELETE CASCADE,
        book_rating INT,
        PRIMARY KEY (user_id, isbn)
    );
    """

    # Column mappings
    books_column_mappings = {
        'ISBN': 'isbn',
        'Book-Title': 'title',
        'Book-Author': 'author',
        'Year-Of-Publication': 'year_published',
        'Publisher': 'publisher'
    }
    
    book_img_url_column_mappings = {
        'ISBN': 'isbn',
        'Image-URL-S': 'small',
        'Image-URL-M': 'medium',
        'Image-URL-L': 'large'
    }

    users_column_mappings = {
        'User-ID': 'user_id',
        'Location': 'location',
        'Age': 'age'
    }

    ratings_column_mappings = {
        'User-ID': 'user_id',
        'ISBN': 'isbn',
        'Book-Rating': 'book_rating'
    }

    database_manager = DatabaseManager()
    database_manager.create_connection()

    # Create tables
    database_manager.create_table([book_table_query, auxiliar_book_img_url_query, user_table_query, ratings_table_query])

    # Inserting values from CSV to postgres DB
    database_manager.insert_values_into_table(table_books, books_column_mappings, df_books)
    database_manager.insert_values_into_table(table_book_img_url, book_img_url_column_mappings, df_books)
    database_manager.insert_values_into_table(table_users, users_column_mappings, df_users)

    existing_user_ids = df_users['User-ID'].unique()
    existing_book_isbns = df_books['ISBN'].unique()

    # Filters the classification data to include only records with existing keys
    df_ratings_filtered = df_ratings[
        df_ratings['User-ID'].isin(existing_user_ids) & df_ratings['ISBN'].isin(existing_book_isbns)
    ]
    database_manager.insert_values_into_table(table_ratings, ratings_column_mappings, df_ratings_filtered)
    df_ratings_filtered.to_csv(rating_filtered_file_path, index=False)

    database_manager.close_connection()

if __name__ == "__main__":
    main()