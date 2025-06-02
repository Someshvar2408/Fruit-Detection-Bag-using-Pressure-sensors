#include <SPI.h>
#include <WiFiNINA.h>

char ssid[] = "Jannat's S23";       // Replace with your WiFi SSID
char pass[] = "test1234";   // Replace with your WiFi password
int status = WL_IDLE_STATUS;

WiFiClient client;
char server[] = "192.168.255.86";   // Replace with your PC's IP address
int port = 12345;                // Port number to connect to Python server

const int sensorPin1 = A0;       // Weight sensor
const int numSensors = 6;
int sensorPins[numSensors] = {A1, A2, A3, A4, A5, A6};
int sensorValues[numSensors];
int threshold = 600;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("WiFi module not found!");
    while (true);
  }

  // Connect to WiFi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(5000);
  }

  Serial.println("Connected to WiFi.");
}

void loop() {
  // Read contact sensors
  int contactCount = 0;
  for (int i = 0; i < numSensors; i++) {
    long total = 0;
    for (int j = 0; j < 50; j++) {
      total += analogRead(sensorPins[i]);
      delay(1);
    }
    sensorValues[i] = total / 50;
    if (sensorValues[i] < threshold) contactCount++;
  }

  // Read weight sensor
  long total = 0;
  for (int i = 0; i < 50; i++) {
    total += analogRead(sensorPin1);
    delay(10);
  }
  float avgReading = total / 50.0;
  float weight = -2.3857 * avgReading + 1433.3969;

  // Prepare data as CSV line: contactCount,s1,s2,s3,s4,s5,s6,avgReading,weight
  String data = String(contactCount) + ",";
  for (int i = 0; i < numSensors; i++) {
    data += String(sensorValues[i]) + ",";
  }
  data += String(avgReading) + "," + String(weight);

  // Send data via TCP
  if (client.connect(server, port)) {
    client.println(data);
    client.stop();
  }

  delay(1000); // Sampling rate
}
