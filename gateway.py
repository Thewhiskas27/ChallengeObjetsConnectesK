# gateway.py
import requests
import random
import time

API_URL = "http://127.0.0.1:5000/data"

def simulate_sensor_data():
    """
    Une simulation de données MPU-6050 comme si elle venait d'un Arduino via Bluetooth.
    Dans un scénario de prod, ceci lirait les données comme une connection Serial/BLE réelle.
    """
    bad_posture = random.random() < 0.3 

    if bad_posture:
        ax = random.randint(9000, 12000) * random.choice([-1, 1])
        ay = random.randint(9000, 12000) * random.choice([-1, 1])
    else:
        ax = random.randint(-3000, 3000)
        ay = random.randint(-3000, 3000)

    az = random.randint(14000, 18000) 
    gx = random.randint(-500, 500)
    gy = random.randint(-500, 500)
    gz = random.randint(-500, 500)

    return {"ax": ax, "ay": ay, "az": az, "gx": gx, "gy": gy, "gz": gz}

def send_data(data):
    try:
        response = requests.post(API_URL, json=data)
        result = response.json()
        print(f"Envoyé: ax={data['ax']}, ay={data['ay']}, az={data['az']} → Posture: {result['posture']}")
    except Exception as e:
        print(f"Erreur à l'envoi des données: {e}")

if __name__ == '__main__':
    print("Démarrage du Gateway — Simulation des données Bluetooth en cours...")
    print("Ctrl+C - Arreter l'application\n")
    while True:
        data = simulate_sensor_data()
        send_data(data)
        time.sleep(1)