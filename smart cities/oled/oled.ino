#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// SDA = 21 , SCL = 22
#define SDA_PIN 21
#define SCL_PIN 22

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void drawCenteredNumber(int value)
{
  display.clearDisplay();

  display.setTextSize(6);
  display.setTextColor(SSD1306_WHITE);

  String text = String(value);

  int16_t x1, y1;
  uint16_t w, h;

  display.getTextBounds(text, 0, 0, &x1, &y1, &w, &h);
  int x = (128 - w) / 2; 
  int y = 16;

  display.setCursor(x, y);
  display.print(text);

  display.display();
}

void setup()
{
  Wire.begin(SDA_PIN, SCL_PIN);

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.begin(115200);
    Serial.println("SSD1306 allocation failed");
    while(true);
  }

  display.clearDisplay();
}

void loop()
{
  drawCenteredNumber(60);
  delay(2000);

  drawCenteredNumber(120);
  delay(2000);

  drawCenteredNumber(40);
  delay(2000);
}