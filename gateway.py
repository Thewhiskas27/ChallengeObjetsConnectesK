import requests
import random
import time

API_URL = "http://127.0.0.1:5000/data"

def simulate_sensor_data():
    state = random.choices(
        ["DEBOUT", "ASSIS", "COUCHE"],
        weights=[50, 30, 20]  # 50% debout, 30% assis, 20% couché
    )[0]

    if state == "DEBOUT":
        # Tronc vertical — pitch et roll proches de 0°
        # ax proche de 0, az proche de 16384 (1g vers le bas)
        ax = random.randint(-2000, 2000)
        ay = random.randint(-2000, 2000)
        az = random.randint(14000, 16384)

    elif state == "ASSIS":
        # Tronc incliné ~90° vers l'avant — pitch entre 50° et 130°
        # ax très négatif (penché en avant), az faible
        ax = random.randint(-14000, -8000)
        ay = random.randint(-2000, 2000)
        az = random.randint(2000, 6000)

    elif state == "COUCHE":
        # Corps horizontal — az très faible (< 0.3g = ~4915 LSB)
        ax = random.randint(-2000, 2000)
        ay = random.randint(-2000, 2000)
        az = random.randint(-3000, 3000)  # proche de 0g sur Z

    # Gyroscope — légère variation dans tous les cas
    gx = random.randint(-200, 200)
    gy = random.randint(-200, 200)
    gz = random.randint(-200, 200)

    return {"ax": ax, "ay": ay, "az": az, "gx": gx, "gy": gy, "gz": gz}

def send_data(data):
    try:
        response = requests.post(API_URL, json=data)
        result = response.json()
        print(f"Sent: ax={data['ax']:>7}, ay={data['ay']:>7}, az={data['az']:>7} → {result['posture']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    print("Gateway démarré — Simulation d'états de posture...\n")
    while True:
        data = simulate_sensor_data()
        send_data(data)
        time.sleep(1)