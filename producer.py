from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    data = {
        "car_id": random.randint(100, 999),
        "speed": random.randint(40, 120),

        # ✅ REQUIRED FOR MAP
        "lat": random.uniform(12.90, 13.15),
        "lon": random.uniform(80.15, 80.30),

        # ✅ REQUIRED FOR SORTING
        "timestamp": time.time()
    }

    producer.send('vehicle_data', data)
    print("Sent:", data)

    time.sleep(1)