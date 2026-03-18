import time
import json
import random
import string
from datetime import datetime
from kafka import KafkaProducer

# --- 1. KONFIGURASI KAFKA ---
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'], 
    api_version=(0, 10, 1),
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

TOPIC_NAME = 'traffic_violations'

# --- 2. KONFIGURASI LOKASI & PELANGGARAN ---
LOCATIONS = ['GATE-01-UB', 'GATE-02-SUHAT', 'GATE-03-VETERAN']
# Bobot Lokasi: Veteran paling macet (70%)
LOCATION_WEIGHTS = [20, 10, 70] 

# DAFTAR PELANGGARAN BARU
VIOLATION_TYPES = [
    'NO_HELMET',        # Tidak pakai helm
    'RED_LIGHT_RUNNER', # Menerobos lampu merah
    'AGAINST_FLOW',     # Lawan arus
    'NO_SEATBELT',      # Tidak pakai sabuk (untuk mobil)
    'OVER_SPEED'        # Ngebut
]

# Bobot Pelanggaran: Helm paling sering (40%), sisanya bervariasi
VIOLATION_WEIGHTS = [40, 20, 15, 15, 10]

# --- 3. FUNGSI BIKIN PLAT NOMER INDONESIA ---
def generate_plat_indo():
    kode_wilayah = random.choice(['N', 'B', 'L', 'W', 'AG', 'DK', 'D', 'AB'])
    nomor = random.randint(1, 9999)
    jumlah_huruf = random.choice([2, 3])
    huruf_belakang = ''.join(random.choices(string.ascii_uppercase, k=jumlah_huruf))
    return f"{kode_wilayah} {nomor} {huruf_belakang}"

print(f"🎥 CCTV Simulator Started. Sending MULTI-VIOLATION data to topic '{TOPIC_NAME}'...")

# --- 4. LOOP UTAMA ---
try:
    while True:
        # Random sleep biar natural (1 - 3 detik)
        time.sleep(random.uniform(1, 3))

        # Pilih Lokasi berdasarkan bobot
        lokasi_terpilih = random.choices(LOCATIONS, weights=LOCATION_WEIGHTS, k=1)[0]
        
        # Pilih Jenis Pelanggaran berdasarkan bobot (REVISI DISINI)
        jenis_pelanggaran = random.choices(VIOLATION_TYPES, weights=VIOLATION_WEIGHTS, k=1)[0]

        # Generate Plat
        plat_nomor = generate_plat_indo() 

        # Buat Data JSON
        data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'location_id': lokasi_terpilih,
            'violation_type': jenis_pelanggaran,  # <--- Data dinamis sekarang
            'confidence': round(random.uniform(0.75, 0.99), 2),
            'vehicle_plate': plat_nomor
        }

        # Kirim ke Kafka
        producer.send(TOPIC_NAME, value=data)
        
        # Print log biar kelihatan bedanya
        print(f"⚠️ [{data['violation_type']}] di {data['location_id']} - {data['vehicle_plate']} (Conf: {data['confidence']})")

except KeyboardInterrupt:
    print("Stopped.")
