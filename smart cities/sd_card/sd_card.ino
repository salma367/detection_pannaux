#include <SPI.h>
#include <SD.h>

#define SD_CS 4

void setup() {

  Serial.begin(115200);

  if (!SD.begin(SD_CS)) {
    Serial.println("SD Card Failed!");
    return;
  }

  Serial.println("SD Card Ready!");

  // Write to file
  File file = SD.open("/test.txt", FILE_WRITE);

  if (file) {
    file.println("sumooo");
    file.close();
    Serial.println("File written");
  } else {
    Serial.println("Error opening file for writing");
  }

  // Read the file
  file = SD.open("/test.txt");

  if (file) {
    Serial.println("Reading file:");

    while (file.available()) {
      Serial.write(file.read());
    }

    file.close();
  } 
  else {
    Serial.println("Error opening file for reading");
  }
}

void loop() {
}