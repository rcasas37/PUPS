//-----CUSTOM NAME FOR SERIAL PORT, SERIAL IS "BACKCHANNEL UART" AND SERIAL1 IS "REGULAR UART"-----//
//#define XBeeSerial Serial1

#define LED P4_7

//-----SETUP FOR PINS AND SERIAL COMMUNICATION-----//
void setup() {
  
  //-----WAIT FOR HARDWARE SERIAL TO APPEAR-----//
  while (!Serial);
  while (!Serial1);

  //-----INITIALIZE DIGITAL PIN AS OUTPUT-----//
  pinMode(LED, OUTPUT);

  //-----BEGIN BACKCHANNEL UART AT 9600 BAUD RATE-----//
  Serial.begin(9600);
  
  //-----BEGIN REGULAR UART AT 9600 BAUD RATE-----//
  Serial1.begin(9600);
  delay(1000);
  
  Serial1.flush();
  Serial.flush();
  Serial.println("SETUP DONE");
}


//-----MAIN LOOP OF BUOY PROGRAM-----//
void loop() {
  
  //-----BLINK LED FOR DEBUG/TEST HEARTBEAT-----//
  digitalWrite(LED, HIGH);
  delay(10);
  digitalWrite(LED, LOW);
  delay(10);

   //while(Serial1.available()) {
      char x = '3';
      //delay(100);
      //Serial1.write("Hello");
      while(x != ';'){
        if(Serial1.available()){
            x = Serial1.read();
            Serial.print(x);
          }
      }
      //Serial.print(x);     //this should print ';'

  //}
  Serial.println();
}

