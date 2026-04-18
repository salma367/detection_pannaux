#define RED_PIN 25  // Pin for red color
#define GREEN_PIN 27 // Pin for green color
#define BLUE_PIN 26 
void setup() {
  // put your setup code here, to run once:
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  orange();
}
void setColor(int red, int green, int blue) {
  analogWrite(RED_PIN, red);
  analogWrite(GREEN_PIN, green);
  analogWrite(BLUE_PIN, blue);
}
void orange(){
  setColor(0, 255, 200);
}
