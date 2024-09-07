import pandas as pd
import re

class DataCleaner:
    def __init__(self, file_path, result_path):
        self.file_path = file_path
        self.result_path = result_path
        self.df = None
        self.df_cleaned = None

    def read_csv(self):
        self.df = pd.read_csv(self.file_path)

    def is_valid_data(self, name):
        return isinstance(name, str) and len(name.strip()) > 0

    def is_valid_url(self, url):
        url_pattern = re.compile("^http:\/\/images\.amazon\.com\/images.*")
        return isinstance(url, str) and bool(url_pattern.match(url))

    def clean_data(self):
        if self.df is None:
            raise ValueError("DataFrame is not initialized. Call read_csv() first.")
        self.df['ISBN'] = pd.to_numeric(self.df['ISBN'], errors='coerce')
        self.df = self.df.dropna(subset=['ISBN'])
        self.df['ISBN'] = self.df['ISBN'].astype(int)
        self.df = self.df.dropna(subset=['Book-Title', 'Book-Author'])

        self.df['Year-Of-Publication'] = pd.to_numeric(self.df['Year-Of-Publication'], errors='coerce')
        self.df = self.df.dropna(subset=['Year-Of-Publication'])
        self.df['Year-Of-Publication'] = self.df['Year-Of-Publication'].astype(int)

        self.df = self.df.drop_duplicates(subset=['ISBN'])

        self.df = self.df[self.df['Book-Title'].apply(self.is_valid_data)]
        self.df = self.df[self.df['Book-Author'].apply(self.is_valid_data)]

        Image_URL_S = self.df['Image-URL-S'].apply(self.is_valid_url)
        Image_URL_M = self.df['Image-URL-M'].apply(self.is_valid_url)
        Image_URL_L = self.df['Image-URL-L'].apply(self.is_valid_url)

        self.df = self.df.loc[Image_URL_S]
        self.df = self.df.loc[Image_URL_M]
        self.df = self.df.loc[Image_URL_L]

        self.df = self.df.sort_values(by='ISBN')
        self.df.to_csv(self.result_path, index=False)

    def get_cleaned_data(self):
        self.df_cleaned = pd.read_csv(self.result_path)
        if self.df_cleaned is None:
            raise ValueError("DataFrame is not initialized. Call clean_data() first.")
        return self.df_cleaned