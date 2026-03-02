# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ax INTEGER, ay INTEGER, az INTEGER,
            gx INTEGER, gy INTEGER, gz INTEGER,
            posture TEXT
        )
    ''')
    conn.commit()
    conn.close()

def detect_posture(ax, ay, az):
    if abs(ax) > 8000 or abs(ay) > 8000:
        return "Bad Posture"
    return "Good Posture"

# --- API Routes ---
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    ax, ay, az = data['ax'], data['ay'], data['az']
    gx, gy, gz = data['gx'], data['gy'], data['gz']
    posture = detect_posture(ax, ay, az)
    timestamp = datetime.datetime.now().isoformat()

    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO readings (timestamp, ax, ay, az, gx, gy, gz, posture)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, ax, ay, az, gx, gy, gz, posture))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok", "posture": posture}), 200

@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM readings ORDER BY id DESC LIMIT 50')
    rows = cursor.fetchall()
    conn.close()

    readings = []
    for row in rows:
        readings.append({
            "id": row[0], "timestamp": row[1],
            "ax": row[2], "ay": row[3], "az": row[4],
            "gx": row[5], "gy": row[6], "gz": row[7],
            "posture": row[8]
        })
    return jsonify(readings), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)