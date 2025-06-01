#include <SPI.h>
#include <WiFiNINA.h>

// WiFi credentials
const char* ssid = "Somesh’s iPhone 16 Pro Max";
const char* password = "test1234";

// TCP Server setup
WiFiServer server(5000);
WiFiClient client;

// Sensor configuration
int sensorPin1 = A0;  // Weight sensor
const int numSensors = 6;
int sensorPins[numSensors] = {A1, A2, A3, A4, A5, A6};
int sensorValues[numSensors];
int threshold = 600;

void setup() {
  Serial.begin(9600);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected to WiFi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Start TCP server
  server.begin();
}

void loop() {
  // Wait for or maintain a connected client
  if (!client || !client.connected()) {
    client = server.available();
    if (client) {
      Serial.println("Client connected");
    } else {
      Serial.println("No client");
      delay(1000);
      return;
    }
  }

  // Read contact sensor values
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

  // Send structured data
  client.print("Contacts:");
  client.print(contactCount);
  client.print(",Sensors:");
  for (int i = 0; i < numSensors; i++) {
    client.print(sensorValues[i]);
    if (i < numSensors - 1) client.print(",");
  }
  client.print(",WeightSensor:");
  client.print(avgReading);
  client.print(",Weight:");
  client.println(weight);

  // Debug output
  Serial.println("Data sent to client:");
  Serial.print("Contacts: ");
  Serial.print(contactCount);
  Serial.print(", Weight: ");
  Serial.println(weight);

  delay(1000); // Sampling interval
}
