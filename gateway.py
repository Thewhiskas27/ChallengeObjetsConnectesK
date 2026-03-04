import serial
import requests

API_URL = "http://127.0.0.1:5000/data"

def parse_line(line):
    try:
        parts = line.strip().split(',')
        if len(parts) != 6:
            return None
        ax, ay, az, gx, gy, gz = map(int, parts)
        return {"ax": ax, "ay": ay, "az": az, "gx": gx, "gy": gy, "gz": gz}
    except:
        return None

def send_data(data):
    try:
        response = requests.post(API_URL, json=data)
        result = response.json()
        print(f"Wokwi → API: ax={data['ax']:>7}, ay={data['ay']:>7}, az={data['az']:>7} → {result['posture']}")
    except Exception as e:
        print(f"Erreur API: {e}")

if __name__ == '__main__':
    print("Connexion au Serial Wokwi avec RFC2217 (TCP port 4000)...")
    try:
        ser = serial.serial_for_url('rfc2217://localhost:4000', baudrate=115200, timeout=2)
        print("Succès!\n")
        while True:
            try:
                raw = ser.readline().decode('utf-8', errors='ignore')
                if not raw.strip():
                    continue
                if ',' not in raw:
                    print(f"[Info] {raw.strip()}")
                    continue
                data = parse_line(raw)
                if data:
                    send_data(data)
            except KeyboardInterrupt:
                print("\nStopped.")
                break
    except Exception as e:
        print(f"Échec: {e}")
        print("Veuillez voir si la simulation Wokwi tourne sur VSCode avant de continuer!")