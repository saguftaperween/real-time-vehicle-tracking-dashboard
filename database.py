import sqlite3

def create_table():
    conn = sqlite3.connect("vehicle_data.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicle_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_id INTEGER,
        speed INTEGER,
        location TEXT,
        timestamp REAL
    )
    """)

    conn.commit()
    conn.close()


def insert_data(car_id, speed, location, timestamp):
    conn = sqlite3.connect("vehicle_data.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO vehicle_data (car_id, speed, location, timestamp)
    VALUES (?, ?, ?, ?)
    """, (car_id, speed, location, timestamp))

    conn.commit()
    conn.close()