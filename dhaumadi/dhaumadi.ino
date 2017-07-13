int pins[] = {
  A2, A3, A4, A5, A1, A0, 13
};

void setup() {
  Serial.begin(115200);
  for (auto pin : pins)
    pinMode(pin, INPUT);
}

int getValue() {
  int value = 0;
  int v = 1;
  for (auto pin : pins) {
    if (digitalRead(pin))
      value |= v;
    v <<= 1;
  }
  return value;
}

void loop() {
  const int dly = 5;
  int idx_a_zero = 0;
  for (auto pin_a_zero : pins) {
    pinMode(pin_a_zero, OUTPUT);
    digitalWrite(pin_a_zero, 0);
    
    int value = getValue();
    
    pinMode(pin_a_zero, INPUT);
    
    Serial.print(idx_a_zero);
    Serial.print(' ');
    Serial.println(value);
    
    ++idx_a_zero;
    delay(dly);
  }

  int value = getValue();
  Serial.print("- ");
  Serial.println(value);
  delay(dly);
}
