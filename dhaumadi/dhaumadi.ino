const int pins[] = {
  A2, A3, A4, A5, A1, A0, 13
};

void setup() {
  Serial.begin(115200);
  for (auto pin : pins) {
    pinMode(pin, OUTPUT);
    digitalWrite(pin, HIGH);
    pinMode(pin, INPUT);
    digitalWrite(pin, LOW);
  }
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
  const int dly = 500;
  int idx_a_zero = 0;
  for (auto pin_a_zero : pins) {
    pinMode(pin_a_zero, OUTPUT);
    delayMicroseconds(dly);

    int value = getValue();

    digitalWrite(pin_a_zero, HIGH);
    pinMode(pin_a_zero, INPUT);
    digitalWrite(pin_a_zero, LOW);

    Serial.print(idx_a_zero);
    Serial.print(' ');
    Serial.println(value);

    ++idx_a_zero;
  }

  int value = getValue();
  Serial.print("- ");
  Serial.println(value);
  delayMicroseconds(dly);
  delay(50);
}
