from .table import Table
from .bplustree import BPTree


class DatabaseManager:

    def __init__(self):

        self.tables = {}
        self.indexes = {}


    def create_table(self, name, key):

        table = Table(name, key)

        self.tables[name] = table

        self.indexes[name] = BPTree(order=5)

        return table


    def build_index(self, table_name):

        table = self.tables[table_name]

        tree = self.indexes[table_name]

        for key, row in table.rows.items():

            tree.insert(key, row)


    def search(self, table_name, key):

        tree = self.indexes[table_name]

        return tree.search(key)


    def insert(self, table_name, row):

        table = self.tables[table_name]

        tree = self.indexes[table_name]

        key = row[table.key_column]

        table.insert(row)

        tree.insert(key, row)


    def delete(self, table_name, key):

        table = self.tables[table_name]

        tree = self.indexes[table_name]

        table.delete(key)

        tree.delete(key)


    def range_query(self, table_name, start, end):

        tree = self.indexes[table_name]

        return tree.range_query(start, end)