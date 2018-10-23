#include <Wire.h>

// most launchpads have a red LED
#define LED P4_7
int count = 0;

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
  delay(5);                     // wait
  digitalWrite(LED, LOW);         // turn the LED off by making the voltage LOW
  delay(5);                     // wait
  

  digitalWrite(P2_4, HIGH);    //allow the GPS Sensor to start running
  Wire.requestFrom(16, 8);    // request 8 bytes from slave device #16
 
  char GPSArray[75];                //GPS Array
  
  for(int i = 0; i<75; i++)                              
  {  
    GPSArray[i] = '_';
  }
  
  char c = Wire.read();
  delay(2);
  
  if(c == '$')
  {
    c = Wire.read();
    delay(2);
    //Serial.print(c);
    if(c == 'G')
    {
      c = Wire.read();
      delay(2);
      //Serial.print(c);
      if(c == 'N')
      {
        c = Wire.read();
        delay(2);
        //Serial.print(c);
        if(c == 'G')
        {
          c = Wire.read();
          delay(2);
          //Serial.print(c);
          if(c == 'G')
          {
            c = Wire.read();
            delay(2);
            //Serial.print(c);
            if(c == 'A')
            {
              c = Wire.read();
              delay(2);
              GPSArray[0] = 'L';
              
              //Fill Array with GPS data (time, lat, long) separated by commas
              for(int i = 1; c != '*'; i++)
              {
                GPSArray[i] = c;
                //Serial.print(c);
                c = Wire.read();
                Wire.requestFrom(16, 1);
                delay(2);

                count = i;
              }
              GPSArray[count+1] = ';';  //Append the terminating character to the array
              Serial.println("\n"); 
            }
          }
        }
      }
    }
  }
  //GPSArray[count] = ';';   //Append the terminating character to the array
  for(int i = 0; i<count; i++)                              
  {  
    if(GPSArray[i] != '_')
    {
        Serial.print(GPSArray[i]);
    }
  }
  
}














