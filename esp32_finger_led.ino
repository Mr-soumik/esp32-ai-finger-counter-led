int leds[5] = {15, 2, 4, 5, 18};

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < 5; i++) pinMode(leds[i], OUTPUT);
}

void loop() {
  if (Serial.available()) {
    int n = Serial.parseInt();
    if (n >= 0 && n <= 5) {
      for (int i = 0; i < 5; i++) {
        digitalWrite(leds[i], i < n ? HIGH : LOW);
      }
    }
  }
}
