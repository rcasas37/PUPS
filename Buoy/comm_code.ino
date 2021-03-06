//-----INCLUDE LIBRARY FOR I2C-----//
#include <Wire.h>

//-----DEFINE PIN 4.7 AS OUTPUT FOR LED-----//
#define LED P4_7

//-----INITIALIZE LARGE CHAR ARRAYS FOR MESSAGE RECEIVING-----//
char PacketRxCC[75];
char PacketRxROV[75];

//-----EXAMPLE CONTROL PACKET FOR TEST/DEBUG-----//
//char test[] = "C,LTx1200,LTy1000,RTx0,RTy-800,AVa10,Xva10;";

//-----PACKET IDS-----//
char SensorID = 'S';
char ControlID = 'C';
char GPSID = 'L';
char PauseID = 'p';
char Order66ID = 'f';
char ShutdownID = 'b';
char InitID = 'z';

int gpscount = 0;
int countb = 0;

//-----SETUP FOR PINS AND SERIAL COMMUNICATION-----//
void setup() {
  
  //-----WAIT FOR HARDWARE SERIAL TO APPEAR-----//
  while (!Serial);
  while (!Serial1);

  //-----BEGIN I2C-----//
  Wire.begin();
  
  //-----INITIALIZE DIGITAL PIN AS OUTPUT-----//
  pinMode(LED, OUTPUT);

  //-----BEGIN BACKCHANNEL UART AT 9600 BAUD RATE-----//
  Serial.begin(19200);
  
  //-----BEGIN REGULAR UART AT 9600 BAUD RATE-----//
  Serial1.begin(19200);

  //-----DELAY TO ALLOW UART COMMS TO BEGIN
  //delay(1000);

  pinMode(P2_4, OUTPUT);
  digitalWrite(P2_4, LOW);

  pinMode(P1_6, INPUT);

  pinMode(P2_5, OUTPUT);
  digitalWrite(P2_5, HIGH);

  //-----CLEAR TX AND RX BUFFERS-----//

  //-----CLEAR REGULAR UART TX BUFFER-----//
  Serial1.flush();
  //-----CLEAR REGULAR UART RX BUFFER-----//
  //Serial1.read();
  //-----CLEAR BACKCHANNEL UART TX BUFFER-----//
  Serial.flush();
  //-----CLEAR BACKCHANNEL UART RX BUFFER-----//
  //Serial.read();
  Serial.println("SETUP DONE");
}


//-----MAIN LOOP OF BUOY PROGRAM-----//
void loop() {
  //-----BLINK LED FOR DEBUG/TEST HEARTBEAT-----//
  digitalWrite(LED, HIGH);
  delay(1);
  //Serial.println("Debug 1");
  if(gpscount != 20){    //-----CHECK IF GPSCOUNT IS GREATER THAN OR EQUAL TO 5, OTHERWISE CONTINUE (SO WE ARE NOT SENDING GPS DATA EVERY ITERATION)-----//
  
  //-----INITAIALIZE ARRAYS TO 0'S-----//
  for(int i = 0; i < 75; i++){
    PacketRxROV[i] = '0';
    PacketRxCC[i] = '0';
  }

  //-----INITIALIZE CHAR X VARIABLE TO CHECK
  char x = '0';
  char y = '0';

  //-----INITIALIZE COUNT FOR ARRAY SIZE/PLACEMENT-----//
  int count = 0;
  
  //Serial.flush();

  //-----RECEIVE EACH CHAR AND ADD TO ARRAY, STOP WHEN CHAR EQUALS SEMICOLON-----//    
  //if(Serial1.available()){
    x = Serial1.read();
    if(x == ControlID || x == PauseID || x == InitID || x == Order66ID){
      PacketRxCC[0] = x;
      count++;
      Serial.write(x);
      while(x != ';') {
        if (Serial1.available()) {
          x = Serial1.read();
          PacketRxCC[count] = x;
          //if(PacketRxCC[0] == ControlID || PacketRxCC[0] == PauseID || PacketRxCC[0] == InitID || PacketRxCC[0] == Order66ID){
            Serial.write(PacketRxCC[count]);
          //}
          if(PacketRxCC[0] == ShutdownID){
            Serial.write("Buoy Shutdown;");//BOUY shutdown
          }
          count++;
        }
      }
    }
  //}
  //Serial.write("C,44,33,22,11,0,0,0;");
  //Serial.println("Debug 2");
  //-----RECEIVE EACH CHAR AND ADD TO ARRAY, STOP WHEN CHAR EQUALS SEMICOLON-----//

  //Reset count variable to 
  count = 0;
  //if(Serial.available()){
    y = Serial.read();
    if (y == SensorID){
      PacketRxROV[count] = y;
      count++;
      Serial1.write(y);
      while(y != ';') {
        if (Serial.available()) {
          y = Serial.read();
          PacketRxROV[count] = y;
          //if(PacketRxROV[0] == SensorID){
            Serial1.write(PacketRxROV[count]);
          //}
          count++;
        }
      }
    }
  //}
    //Serial1.write("S,55,44,33,22,11,0,0,0;");
    //Serial.println("Debug 3");
  } else {
 //----------GPS/I2C SECTION----------//
    
    gpscount = 0;    //-----RESET GPSCOUNT-----//
    digitalWrite(P2_4, HIGH);    //-----ALLOW THE GPS SENSOR TO START RUNNING-----//
    Wire.requestFrom(16, 8);    //-----REQUEST 8 BYTES FROM SLAVE DEVICE #16 (GPS)-----//
   
    char GPSArray[75];    //-----INITIALIZE GPS ARRAY-----//
    
    for(int l = 0; l<75; l++)    //-----SET GPS ARRAY VALUES TO "_"-----//                            
    {  
      GPSArray[l] = '_';
    }
    char c = Wire.read();    //-----SET READ BYTE TO CHAR C-----//
    delay(2);
    //Serial.println("-----Debug 4");
    //-----PARSE THROUGH GPS DATA AND ISOLATE NECESSARY LOCATION DATA-----//
    if(c == '$')    //-----IF C IS EQUAL TO $ SIGN, CONTINUE-----//
    {
      c = Wire.read();
      delay(2);
      //Serial.print(c);
      if(c == 'G')    //-----IF NEXT C IS EQUAL TO G, CONTINUE-----//
      {
        c = Wire.read();
        delay(2);
        //Serial.print(c);
        if(c == 'N')    //-----IF NEXT C IS EQUAL TO N, CONTINUE-----//
        {
          c = Wire.read();
          delay(2);
          //Serial.print(c);
          if(c == 'G')    //-----IF NEXT C IS EQUAL TO G, CONTINUE-----//
          {
            c = Wire.read();
            delay(2);
            //Serial.print(c);
            if(c == 'G')    //-----IF NEXT C IS EQUAL TO G, CONTINUE-----//
            {
              c = Wire.read();
              delay(2);
              //Serial.print(c);
              if(c == 'A')    //-----IF NEXT C IS EQUAL TO A, CONTINUE-----//
              {
                c = Wire.read();    //-----USE NEXT C TO BUILD ARRAY-----//
                delay(2);
                GPSArray[0] = 'L';    //-----SET FIRST CHAR OF ARRAY TO L FOR GPS DATA PACKET ID-----//
                
                //-----FILL ARRAY WITH GPS DATA (TIME, LATITUDE, LONGITUDE) SEPARATED BY COMMAS UNTIL "*" IS REACHED-----//
                for(int l = 1; c != '*'; l++)
                {
                  GPSArray[l] = c;    //-----SET CHAR C EQUAL TO SPOT IN GPSARRAY BASED ON I, STARTING AT ONE-----//
                  //Serial.print(c);
                  c = Wire.read();
                  Wire.requestFrom(16, 1);
                  delay(2);
  
                  countb = l;
                }
                GPSArray[countb+1] = ';';    //-----APPEND TERMINATING CHAR (SEMICOLON) TO ARRAY-----//
                //Serial.println("\n"); 
              }
            }
          }
        }
      }
    }
    //Serial.println("-----Debug 5");
    //-----SEND EACH BYTE OF ARRAY THROUGH TETHER 
    for(int l = 0; l < countb; l++)                              
    {  
      if(GPSArray[l] != '_')
      {
          Serial.print(GPSArray[l]);
      }
    }
    //Serial.println("----------Debug 6");
  }
  gpscount++;    //-----ONCE THE ABOVE IS COMPLETED, INCREASE COUNT AND CONTINUE-----//

  digitalWrite(LED, LOW);
  delay(1);
}
