# gateway.py
import requests
import random
import time

API_URL = "http://127.0.0.1:5000/data"

def simulate_sensor_data():
    """
    Simulates MPU-6050 data like it would come from Arduino via Bluetooth.
    In production, this would read from a real Serial/BLE connection.
    """
    bad_posture = random.random() < 0.3  # 30% chance of bad posture

    if bad_posture:
        ax = random.randint(9000, 12000) * random.choice([-1, 1])
        ay = random.randint(9000, 12000) * random.choice([-1, 1])
    else:
        ax = random.randint(-3000, 3000)
        ay = random.randint(-3000, 3000)

    az = random.randint(14000, 18000)  # Z axis ~16384 at rest (1g)
    gx = random.randint(-500, 500)
    gy = random.randint(-500, 500)
    gz = random.randint(-500, 500)

    return {"ax": ax, "ay": ay, "az": az, "gx": gx, "gy": gy, "gz": gz}

def send_data(data):
    try:
        response = requests.post(API_URL, json=data)
        result = response.json()
        print(f"Sent: ax={data['ax']}, ay={data['ay']}, az={data['az']} → Posture: {result['posture']}")
    except Exception as e:
        print(f"Error sending data: {e}")

if __name__ == '__main__':
    print("Gateway started — simulating Bluetooth data stream...")
    print("Press Ctrl+C to stop\n")
    while True:
        data = simulate_sensor_data()
        send_data(data)
        time.sleep(1)  # Send every second