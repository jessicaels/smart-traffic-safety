import mysql.connector

try:
    # 1. Konek ke Database
    db = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin123",
        database="traffic_db"
    )
    cursor = db.cursor()

    # 2. Perintah SQL Pembuatan Tabel
    print("Sedang membuat tabel violations...")
    query = """
    CREATE TABLE IF NOT EXISTS violations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        location_id VARCHAR(50),
        violation_type VARCHAR(50),
        confidence FLOAT,
        vehicle_plate VARCHAR(20),
        status VARCHAR(20) DEFAULT 'UNVERIFIED'
    );
    """
    
    # 3. Eksekusi
    cursor.execute(query)
    print("✅ SUKSES! Tabel 'violations' berhasil dibuat.")
    
    cursor.close()
    db.close()

except Exception as e:
    print(f"❌ Gagal: {e}")
    
