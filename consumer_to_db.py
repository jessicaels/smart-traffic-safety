import json
from kafka import KafkaConsumer
import mysql.connector

# Konek ke MySQL
db = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="admin123",
    database="traffic_db"
)
cursor = db.cursor()

# Konek ke Kafka
consumer = KafkaConsumer(
    'traffic_violations',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("📥 Consumer Started. Waiting for data...")

for message in consumer:
    data = message.value
    
    # Masukkan ke MySQL
    sql = "INSERT INTO violations (timestamp, location_id, violation_type, confidence, vehicle_plate) VALUES (%s, %s, %s, %s, %s)"
    val = (data['timestamp'], data['location_id'], data['violation_type'], data['confidence'], data['vehicle_plate'])
    
    try:
        cursor.execute(sql, val)
        db.commit()
        print(f"✅ Data Saved to MySQL: {data['vehicle_plate']} at {data['location_id']}")
    except Exception as e:
        print(f"❌ Error saving data: {e}")
