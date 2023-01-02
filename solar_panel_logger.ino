// The pin we read analog data from.
// Can change depending on which slot the live wire is connected to (from A0 to A5)
int analogPin = A1;
void setup() {
  // The integer argument for Serial.begin() must be the same as the baudrate in solar_panel_reader.py
  Serial.begin(9600);
  Serial.setTimeout(1);
  Serial.println("Arduino starting output...");
}

void loop() {
  // Read the input pin. This value is just a raw int between 0 and 1023.
  // Its meaning (in volts) is determined by solar_panel_reader.py
  int val = analogRead(analogPin);
  // Pass the value to standard output
  Serial.println(val);
  // Wait a second before reading the pin again
  delay(1000);
}
