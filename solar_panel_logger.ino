int analogPin = A1;
int val = 0;
void setup() {
  Serial.begin(9600);           //  setup serial
  Serial.setTimeout(1);
  Serial.println("Hello world");
}

void loop() {
  // while (Serial.availableForWrite());
  // Serial.println("Hello world");
  
  val = analogRead(analogPin);  // read the input pin
  Serial.println(val);          // debug value
  delay(1000);                       // wait for a second
}
// void setup() {
//   // put your setup code here, to run once:
//   Serial.begin()
// }

// void loop() {
//   // put your main code here, to run repeatedly:

// }
// the setup function runs once when you press reset or power the board
// void setup() {
//   // initialize digital pin LED_BUILTIN as an output.
//   pinMode(LED_BUILTIN, OUTPUT);
// }

// // the loop function runs over and over again forever
// void loop() {
//   digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
//   delay(1000);                       // wait for a second
//   digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
//   delay(1000);                       // wait for a second
// }