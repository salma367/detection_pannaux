#include <SPI.h>


#include <MFRC522.h>

#define SS_RFID 5
#define RST_PIN 33
#define SS_SD   4   // change if needed

MFRC522 mfrc522(SS_RFID, RST_PIN);

void setup() {
  Serial.begin(115200);

  pinMode(SS_RFID, OUTPUT);
  pinMode(SS_SD, OUTPUT);

  // Disable all SPI devices
  digitalWrite(SS_RFID, HIGH);
  digitalWrite(SS_SD, HIGH);

  SPI.begin();

  // Activate RFID only
  digitalWrite(SS_RFID, LOW);

  mfrc522.PCD_Init();

  Serial.println("Scan RFID...");
}

void loop() {
  // Ensure only RFID is active
  digitalWrite(SS_SD, HIGH);
  digitalWrite(SS_RFID, LOW);

  if (!mfrc522.PICC_IsNewCardPresent()) return;
  if (!mfrc522.PICC_ReadCardSerial()) return;

  Serial.print("UID: ");
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    Serial.print(" ");
  }
  Serial.println();

  mfrc522.PICC_HaltA();
}