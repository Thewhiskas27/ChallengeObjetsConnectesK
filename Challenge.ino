#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu.initialize();
  Serial.println(mpu.testConnection() ? "MPU6050 connected" : "Connection failed");
}

void loop() {
  int16_t ax, ay, az, gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  String data = String(ax) + "," + String(ay) + "," + String(az) + "," +
                String(gx) + "," + String(gy) + "," + String(gz);

  Serial.println(data);
  delay(500);
}