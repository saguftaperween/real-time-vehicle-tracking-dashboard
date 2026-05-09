from kafka import KafkaConsumer
import json
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["vehicle_db"]
collection = db["vehicle_data"]

consumer = KafkaConsumer(
    'vehicle_data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Consumer started... storing in MongoDB")

for message in consumer:
    data = message.value

    # insert into MongoDB
    collection.insert_one(data)

    print("Stored:", data)