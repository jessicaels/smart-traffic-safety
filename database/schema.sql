-- Membuat database jika belum ada
CREATE DATABASE IF NOT EXISTS traffic_db;
USE traffic_db;

-- Membuat tabel pelanggaran
CREATE TABLE IF NOT EXISTS violations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    location_id VARCHAR(50) NOT NULL,
    violation_type VARCHAR(50) DEFAULT 'NO_HELMET',
    confidence FLOAT,
    vehicle_plate VARCHAR(20),
    status VARCHAR(20) DEFAULT 'Unverified',
    evidence_path VARCHAR(255)
);

-- Contoh data dummy awal (Variasi Pelanggaran)
INSERT INTO violations (timestamp, location_id, violation_type, confidence, vehicle_plate, status)
VALUES 
(NOW(), 'GATE-03-VETERAN', 'NO_HELMET', 0.95, 'N 1234 AB', 'Verified'),
(NOW(), 'GATE-02-SUHAT', 'RED_LIGHT_RUNNER', 0.88, 'B 5678 CD', 'Unverified'),
(NOW(), 'GATE-01-UB', 'AGAINST_FLOW', 0.92, 'L 9988 XY', 'Unverified'),
(NOW(), 'GATE-03-VETERAN', 'NO_SEATBELT', 0.85, 'D 4455 GF', 'Verified');
