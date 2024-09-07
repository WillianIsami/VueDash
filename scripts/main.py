from data_cleaning import DataCleaner
from db_operations import DatabaseManager

def main():
    file_path = "./scripts/data/Books.csv"
    result_path = './scripts/ResultBooks.csv'

    data_cleaner = DataCleaner(file_path, result_path)
    data_cleaner.read_csv()
    data_cleaner.clean_data()
    df = data_cleaner.get_cleaned_data()

    table_books = "books"
    table_book_img_url = "book_img_url"
    book_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_books} (
        isbn BIGINT PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year_published INTEGER NOT NULL,
        publisher TEXT NOT NULL
    );
    """
    auxiliar_book_img_url_query = f"""
    CREATE TABLE IF NOT EXISTS {table_book_img_url} (
        isbn BIGINT PRIMARY KEY REFERENCES books(isbn) ON DELETE CASCADE,
        small VARCHAR(255),
        medium VARCHAR(255),
        large VARCHAR(255)
    );
    """
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
    database_manager = DatabaseManager()
    database_manager.create_connection()
    database_manager.create_table([book_table_query, auxiliar_book_img_url_query])
    database_manager.insert_values_into_table(table_books, books_column_mappings, df)
    database_manager.insert_values_into_table(table_book_img_url, book_img_url_column_mappings, df)
    database_manager.close_connection()

if __name__ == "__main__":
    main()