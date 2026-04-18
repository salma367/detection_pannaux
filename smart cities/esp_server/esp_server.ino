#include <WiFi.h>
#include <WebServer.h>
#include <DNSServer.h>

const char* ssid = "ESP32_SENSORS";
const char* password = "12345678";

DNSServer dnsServer;
WebServer server(80);

void portalPage() {

  float temperature = 25.3;
  float humidity = 60.2;

  String page = "<html><body>";
  page += "<h1>ESP32 Sensor Data</h1>";
  page += "Temperature: " + String(temperature) + " C<br>";
  page += "Humidity: " + String(humidity) + " %";
  page += "</body></html>";

  server.send(200, "text/html", page);
}

void setup() {

  Serial.begin(115200);

  WiFi.softAP(ssid, password);

  dnsServer.start(53, "*", WiFi.softAPIP());

  server.on("/", portalPage);

  // Android connectivity check
  server.on("/generate_204", portalPage);

  // Apple captive portal check
  server.on("/hotspot-detect.html", portalPage);

  // Windows check
  server.on("/connecttest.txt", portalPage);

  server.onNotFound(portalPage);

  server.begin();
}

void loop() {

  dnsServer.processNextRequest();
  server.handleClient();
}