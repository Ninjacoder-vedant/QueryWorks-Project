import pandas as pd


class Table:

    def __init__(self, name, key_column):

        self.name = name
        self.key_column = key_column

        self.rows = {}


    def load_csv(self, path):

        df = pd.read_csv(path)

        for _, row in df.iterrows():

            key = row[self.key_column]

            self.rows[key] = row.to_dict()


    def insert(self, row):

        key = row[self.key_column]

        self.rows[key] = row


    def delete(self, key):

        if key in self.rows:
            del self.rows[key]


    def get(self, key):

        return self.rows.get(key)