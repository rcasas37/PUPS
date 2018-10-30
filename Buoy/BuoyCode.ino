
// what's the name of the hardware serial port?
#define ROVSerial Serial
#define XBeeSerial Serial1


// most launchpads have a red LED
#define LED RED_LED

//declare packets recieved from ROV and Command Center
char PacketRxCC[100];
char PacketRxROV[100];

void setup() {
  // initialize the digital pin as an output.
  pinMode(LED, OUTPUT);     

  // wait for hardware serial to appear
  while (!Serial);
  Serial.begin(9600);    // 9600 baud rate for Serial port
  
  // wait for hardware serial to appear
  while (!Serial1);
  Serial1.begin(9600);   // 9600 baud rate for Serial port
}

     
void loop() {
  //Heartbeat of the board to ensure it is working
  digitalWrite(LED, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(200);               // wait for a second
  digitalWrite(LED, LOW);    // turn the LED off by making the voltage LOW
  delay(200);               // wait for a second*/
 
  ////////////////////////////////////////////////Serial Communication for Command Center to Buoy////////////////////////////////////  
  if (XBeeSerial.available()){
    
    char x;
    int count = 0;
    
    //receive each char and add to an array
    for(count; x != ';'; count++){
      x = XBeeSerial.read();
      PacketRxCC[count] = x;
    }
     Serial.println(PacketRxCC);
    //add one to count for size of array
    count = count++;
    
    //create a Packet for TX to the Command Center
    char PacketTxCC[count];

    for(int i=0; i<count; i++){
      PacketTxCC[i] = PacketRxCC[i];
    }
  Serial.println(PacketTxCC);
  XBeeSerial.write(PacketTxCC);
  }

  //Clean TX Buffer for CC
  XBeeSerial.flush();
  
  //Clean RX buffer for CC
  XBeeSerial.read();
    
  ////////////////////////////////////Serial Communication for ROV to Buoy//////////////////////////////////////////////////////////
  if (ROVSerial.available()) {
    for(int i = 0; i < 10; i++){
      PacketRxROV[i] = ROVSerial.read();
    }

    ROVSerial.write(PacketRxROV);
 }
 
 char* command = strchr(PacketRxROV, '0x42');
    if (command != 0)
    {
      Serial.println("End");
    }
 
  //Clean TX Buffer for ROV
  ROVSerial.flush();
  
  //Clean RX buffer for ROV
  ROVSerial.read();
}







    

  
