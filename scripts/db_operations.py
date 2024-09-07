import psycopg2
from config import DATABASE

class DatabaseManager:
    def __init__(self):
        self.conn = None
    
    def create_connection(self):
        self.conn = psycopg2.connect(dbname=DATABASE.get('dbname'),
                            user=DATABASE.get('user'),
                            password=DATABASE.get('password'),
                            host=DATABASE.get('host'),
                            port=DATABASE.get('port'))
        return self.conn

    def create_table(self, queries):
        cursor = self.conn.cursor()
        for query in queries:
            cursor.execute(query)
        self.conn.commit()
        print("Tables created")

    def insert_values_into_table(self, table_name, column_mappings, df):
        """
        Insert values into a specified table in the database.

        :param conn: The database connection object.
        :param table_name: The name of the table to insert data into.
        :param column_mappings: A dictionary mapping DataFrame columns to table columns.
        :param df: The DataFrame containing the data to insert.
        """
        columns = ', '.join(column_mappings.values())
        placeholders = ', '.join(['%s'] * len(column_mappings))
        sql = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders});
        """
        data = []
        for _, row in df.iterrows():
            row_data = [row[df_col] for df_col in column_mappings.keys()]
            data.append(tuple(row_data))
        with self.conn.cursor() as cur:
            cur.executemany(sql, data)
            self.conn.commit()
            print(f"Inserted {cur.rowcount} rows into the {table_name} table")

    def close_connection(self):
        """Close database connection"""
        if self.conn is not None:
            self.conn.close()
