#include <Wire.h>
char GPSArray[20];                //GPS Array

// most launchpads have a red LED
#define LED RED_LED
char x;
void setup()
{
  Wire.begin();        // join i2c bus (address optional for master)
    
  // initialize the digital pin as an output.
  pinMode(LED, OUTPUT);     

  Serial.begin(9600);    // 9600 baud rate for Serial port
  
  pinMode(P2_4, OUTPUT);      //initalizing the Reset pin P2.4
  digitalWrite(P2_4, LOW);    //setting the Reset pin P2.4 to low active
  
  pinMode(P1_6, INPUT);        //initalizing the interrupt pin P1.6
  
  pinMode(P2_5, OUTPUT);      //initalizing the Wake pin P2.5
  digitalWrite(P2_5, HIGH);    //setting the Wake pin P2.5 to High active
  
  Serial.println("\nSetup Done\n");
}

void loop()
{  
  //Heartbeat of the board to ensure it is working
  digitalWrite(LED, HIGH);         // turn the LED on (HIGH is the voltage level)
  delay(200);                     // wait
  digitalWrite(LED, LOW);         // turn the LED off by making the voltage LOW
  delay(200);                     // wait
  

  digitalWrite(P2_4, HIGH);    //allow the GPS Sensor to start running
  int arraysize = Wire.requestFrom(16, 4);    // request 16 bytes from slave device #16


  for(int i = 0; i < arraysize; i++)                              
  {  
    x = Wire.read(); 
    GPSArray[i] = x;
  }
  
    for(int i = 0; i<arraysize; i++)                              
  {  
    Serial.print(GPSArray[i]);
  }
}






























  //Serial.print(biglandon);
//  int landon = digitalRead(P1_6);
//  //Serial.print(landon);
//  
//  while(landon == 1)
//  {
//    x = Wire.read();
//    Serial.print(x);
//  }



//  for(int i = 0; Wire.available(); i++)                              
//  {  
//    x = Wire.read(); 
//    if(x != '$')
//    {
//      if(x == '*')
//      {
//        //Serial.print("\n");
//        break;
//      }
//      GPSArray[i] = x;
//    }
//  }
