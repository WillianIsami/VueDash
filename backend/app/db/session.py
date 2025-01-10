import psycopg2
from app.core.config import settings

class DatabaseManager:
    def __init__(self):
        self.conn = None
    
    def create_connection(self):
        self.conn = psycopg2.connect(
                            dbname=settings.POSTGRES_NAME,
                            user=settings.POSTGRES_USER,
                            password=settings.POSTGRES_PASSWORD,
                            host=settings.POSTGRES_HOST,
                            port=settings.POSTGRES_PORT
                        )
        return self.conn

    def create_table(self, queries):
        cursor = self.conn.cursor()
        for query in queries:
            cursor.execute(query)
        self.conn.commit()
        print("Tables created")
    
    def insert_values_into_table(self, table_name, column_mappings, df, batch_size=2000):
        """
        Insert values into a specified table in the database using batch processing.

        :param table_name: The name of the table to insert data into.
        :param column_mappings: A dictionary mapping DataFrame columns to table columns.
        :param df: The DataFrame containing the data to insert.
        :param batch_size: Number of rows to insert in each batch (default: 2000).
        """
        columns = ', '.join(column_mappings.values())
        placeholders = ', '.join(['%s'] * len(column_mappings))
        sql = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders});
        """

        values = df[list(column_mappings.keys())].values.tolist()
        total_rows = len(values)
        
        with self.conn.cursor() as cur:
            try:
                # Turn off autocommit for better performance
                self.conn.autocommit = False
                
                # Process in batches
                for i in range(0, total_rows, batch_size):
                    batch = values[i:i + batch_size]
                    cur.executemany(sql, batch)
                    
                    # Print progress
                    rows_inserted = min(i + batch_size, total_rows)
                    print(f"Progress: {rows_inserted}/{total_rows} rows inserted", end='\r')
                
                # Final commit
                self.conn.commit()
                print(f"\nSuccessfully inserted {total_rows} rows into {table_name}")
                
            except Exception as e:
                self.conn.rollback()
                print(f"Error occurred: {str(e)}")
                raise
            finally:
                # Reset autocommit to default
                self.conn.autocommit = True

    def close_connection(self):
        """Close database connection"""
        if self.conn is not None:
            self.conn.close()
