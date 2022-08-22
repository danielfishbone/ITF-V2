
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  pinMode(LED_BUILTIN,OUTPUT);
  digitalWrite(LED_BUILTIN,HIGH);
  digitalWrite(LED_BUILTIN,LOW);

}

// the loop routine runs over and over again forever:
void loop() {
  unsigned long sensorValue = 0;
  for(int i = 0; i<100; i++){
   sensorValue += analogRead(A0);
   }
   sensorValue /= 100;
  String valu = "{";
  valu += String(sensorValue); 
  valu += "}";
  Serial.println(valu);
//  Serial1.print('\n');
  delay(100);        // delay in between reads for stability
}
