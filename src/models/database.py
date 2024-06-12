from pymongo import MongoClient
from bson import ObjectId


class BookDatabase:
    def __init__(self, host='localhost', port=27017, db_name='book_catalog', collection_name='books'):
        self.client = MongoClient(f'mongodb://{host}:{port}/')
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_all_books(self):
        return list(self.collection.find())

    def get_book_by_id(self, book_id):
        return self.collection.find_one({'_id': ObjectId(book_id)})

    def add_book(self, book_data):
        return self.collection.insert_one(book_data)

    def update_book(self, book_id, updated_data):
        return self.collection.update_one({'_id': ObjectId(book_id)}, {'$set': updated_data})

