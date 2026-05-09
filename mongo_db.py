from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["vehicle_db"]
collection = db["vehicle_data"]

def insert_data(data):
    collection.insert_one(data)