
// what's the name of the hardware serial port?
#define XBeeSerial Serial1

// most launchpads have a red LED
#define LED RED_LED

//declare packets recieved from ROV and Command Center
char PacketRxCC[100];
char PacketRxROV[100];

void setup() {
  // wait for hardware serial to appear
  while (!Serial);
  
  // initialize the digital pin as an output.
  pinMode(LED, OUTPUT);     

  // 9600 baud rate for Serial port
  Serial.begin(9600);

  // 9600 baud is the default rate for the Ultimate GPS
  XBeeSerial.begin(9600);
}

     
void loop() {
  /*digitalWrite(LED, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);               // wait for a second
  digitalWrite(LED, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);               // wait for a second*/
    
  if (Serial.available()){
    
    for(int i = 0; i < 100; i++){
      PacketRxCC[i] = Serial.read();
    }
    //Serial.println(PacketRx);
    
    char* command = strtok(PacketRxCC, "0x42");
    while (command = 0)
    {
      digitalWrite(LED, HIGH);    // turn the LED on by making the voltage LOW
    }
    if (command != 0){
      digitalWrite(LED, LOW);    // turn the LED off by making the voltage LOW
    }
    Serial.write(PacketRxCC);
    Serial.write("Repeat Echo");
  }
  if (XBeeSerial.available()) {
    for(int i = 0; i < 100; i++){
      PacketRxROV[i] = XBeeSerial.read();
    }
    XBeeSerial.write(PacketRxROV);
  }
}

  
