#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "SYSLAB";
const char* password = "KDasSharma@LABSYS";
const char* mqtt_server = "10.0.0.131";  // Pi IP

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");

  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    while (!client.connect("ESP32Publisher")) {
      delay(500);
    }
  }

  // Send commands to Pi LED
  client.publish("esp/led", "ON");
  delay(2000);
  client.publish("esp/led", "OFF");
  delay(2000);
  client.publish("esp/led", "BLINK 300"); // Blink with 300ms interval
  delay(5000);
}
