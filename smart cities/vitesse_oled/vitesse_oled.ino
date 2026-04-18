#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <TinyGPS++.h>
#include <HardwareSerial.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

#define SDA_PIN 21
#define SCL_PIN 22

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// GPS
TinyGPSPlus gps;
HardwareSerial GPSserial(1); // UART1

// Draw centered speed
void drawSpeed(int speed)
{
  display.clearDisplay();

  display.setTextSize(6);
  display.setTextColor(SSD1306_WHITE);

  String text = String(speed);

  int16_t x1, y1;
  uint16_t w, h;

  display.getTextBounds(text, 0, 0, &x1, &y1, &w, &h);
  int x = (128 - w) / 2;
  int y = 10;

  display.setCursor(x, y);
  display.print(text);

  // unit
  display.setTextSize(2);
  display.setCursor(40, 50);
  display.print("km/h");

  display.display();
}

void setup()
{
  Serial.begin(115200);

  // OLED init
  Wire.begin(SDA_PIN, SCL_PIN);
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("SSD1306 failed");
    while(true);
  }

  display.clearDisplay();

  // GPS init
  GPSserial.begin(9600, SERIAL_8N1, 16, 17);

  Serial.println("GPS + OLED Ready");
}

void loop()
{
  // Read GPS data
  while (GPSserial.available())
  {
    gps.encode(GPSserial.read());
  }

  // If speed is valid
  if (gps.speed.isValid())
  {
    int speed = gps.speed.kmph(); // speed in km/h
    drawSpeed(speed);

    Serial.print("Speed: ");
    Serial.println(speed);
  }
}