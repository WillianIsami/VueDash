import pandas as pd

class DataCleaner:
    def __init__(self, file_path, result_path):
        self.file_path = file_path
        self.result_path = result_path
        self.df = None

    def read_csv(self):
        """Reads the CSV file and loads it into a DataFrame."""
        self.df = pd.read_csv(self.file_path)

    def get_clean_data(self, cleaning_rules):
        """
        Cleans the DataFrame based on the provided rules.

        Return the cleaned data loaded into a DataFrame.
        
        :param cleaning_rules: A dictionary with the cleaning rules for different columns.
                                Example:
                                {
                                    "dropna": ["Book-Title", "Book-Author"], 
                                    "drop_duplicates": ["ISBN"],
                                    "remove_zeros": ["Age"]  # New rule to remove zeros from 'Age'
                                    "convert": {
                                        "Year-Of-Publication": "int"
                                    }
                                }
        """
        if self.df is None:
            raise ValueError("DataFrame is not initialized. Call read_csv() first.")
        
        print("Initial Data Shape:", self.df.shape)
        
        # Drop NaN values in specified columns
        if "dropna" in cleaning_rules:
            for col in cleaning_rules["dropna"]:
                self.df = self.df.dropna(subset=[col])
        print("DEBUGGING DROPNA:", self.df.shape)

        # Drop duplicates in specified columns
        if "drop_duplicates" in cleaning_rules:
            for col in cleaning_rules["drop_duplicates"]:
                self.df = self.df.drop_duplicates(subset=[col])
        print("DEBUGGING DROP DUPLICATES:", self.df.shape)
    
        if "remove_zeros" in cleaning_rules:
            for col in cleaning_rules["remove_zeros"]:
                self.df = self.df[self.df[col] != 0]
        print("DEBUGGING DROP ZEROS:", self.df.shape)    
        
        # Convert columns to specified types
        if "convert" in cleaning_rules:
            for col, dtype in cleaning_rules["convert"].items():
                if dtype == "int":
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                    self.df = self.df.dropna(subset=[col])  # Remove rows with NaN after conversion
                    self.df[col] = self.df[col].astype(int)
                elif dtype == "float":
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                    self.df = self.df.dropna(subset=[col])  # Remove rows with NaN after conversion
                    self.df[col] = self.df[col].astype(float)
                elif dtype == "str":
                    self.df[col] = self.df[col].astype(str)
        print("DEBUGGING DROP CONVERT:", self.df.shape)

        print("Data after cleaning:", self.df.shape)

        self.df.to_csv(self.result_path, index=False)
        print(f"Cleaned data saved to {self.result_path}")
        return pd.read_csv(self.result_path)