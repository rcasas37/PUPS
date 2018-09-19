/* SPI Pins and Basics:

SS is slave select (or CS), which goes to digital pin 8, or P2.7 on the Launchpad
SDI is the MISO and MOSI pins, which go to digital pinS 14/15, or P3.1 and P3.0 on the Launchpad
*Note: you do not need to set SDI to anything, it is handled by SPI.transfer()
CLK is clock, which goes to digital pin 7, or P3.2 on the Launchpad

*/

#include "SPI.h"  //include the SPI library

const int CS = 8; // Set SS equal to variable CS for use later


void setup() {


  pinMode (CS, OUTPUT);  // Set slave select as an output
  digitalWrite(CS, HIGH); // makes sure slave select is off for rn, SS needs LOW value to communicate between master/slave 
  SPI.setBitOrder(MSBFIRST);  //set bit order to most significant bit first
  SPI.setDataMode(SPI_MODE0);  //set data mode to SPI mode0 
  SPI.setClockDivider(SPI_CLOCK_DIV8);
  SPI.begin();

  //Setup Serial Comms
  Serial.begin(9600);
  //Write_MSP430F5529_Register (0x0D, B11000010); 
}

//int32_t adc;  //initiating adc variable, part of original code; will probably delete later
//int32_t deeznuts;


void loop(){
    //uint8_t HB,MB,LB=0, CTRL=0000;;
    //CTRL =(MSP430F5529_Register_Address<<1); //left shift address one digit for write command
    //CTRL |= 1; //Turn on Read Operation by toggling last bit on
    char theresult;
    digitalWrite(CS, LOW);
    theresult = SPI.transfer(0x45); // transfer data
   // deeznuts = digitalRead(P3_2);
   // Serial.print("Pin 3_2:  ");
   // Serial.println(deeznuts);
    digitalWrite(CS, HIGH);
    
    Serial.print("Result: ");
    Serial.println(theresult);
    delay(1000);  

}

  /*
  //adc = Read_MSP430F5529_24bit(0x00);
  Read_MSP430F5529_Register(0x0D);
  //Serial.print("Ch0 :  ");
  //Serial.println(adc);
  delay(100); 
  deeznuts = digitalRead(P3_2);
  Serial.println(deeznuts);
}*/
/*
//overall write funtion below
uint8_t Write_MSP430F5529_Register (uint8_t MSP430F5529_Register_Address, uint8_t Command) {
  delay(100); 
  Serial.print("Command Register Received: ");
  Serial.print(MSP430F5529_Register_Address,HEX); // HEX is obviously the value in hex
  Serial.print(" - Command Received: ");
  Serial.println(Command); //difference between print and print"ln" is it is supposed to print in readable ASCII value
  //BIN means whatever the value of Command but in Binary, which doesnt make too much sense yet
  delay(100); 
// stuff after this seems like whatever original code was trying to do but contains useful code to learn from, will probably cut out
  MSP430F5529_Register_Address <<= 1;   //left shift address one digit
  MSP430F5529_Register_Address &= B00111110; // and ensure last digit is a zero for write command
  delay(100); 
  digitalWrite(CS, LOW); // now take CS low to enable SPI device
  delay(100); 
  SPI.transfer(MSP430F5529_Register_Address); // send address with write command to 
  delay(100); 
  SPI.transfer(Command); //now send payload
  delay(100); 
  digitalWrite(CS, HIGH); // deselect the CS pin. 
  
  Serial.print(" Write Command Byte Sent: ");
  Serial.println(MSP430F5529_Register_Address,BIN); // verify what command was sent (i.e. address and write bit = 0)

  delay(100); 
 
  //Now Verify all went well. If so, have the function return value of one,
  //otherwise, alert the user that something is amiss. 
  uint8_t Response = Read_MSP430F5529_Register (MSP430F5529_Register_Address>>1);
  if (Response == Command){
    return 1;  
    delay(100); 
  }
  else 
  {
    Serial.println("");
    Serial.print("Error for register: ");
    Serial.print(MSP430F5529_Register_Address>>1,BIN);
    Serial.print(" - Command Sent: ");
    Serial.print(Command,BIN);
    Serial.print(" - Response Received: ");
    Serial.println(Response,BIN);
    Serial.println("");
    return 0;
    delay(100); 
  }
}

//overall read function below
uint8_t Read_MSP430F5529_Register (uint8_t MSP430F5529_Register_Address) {
  delay(100); 
  //i think this is used to switch between reading and writing
  MSP430F5529_Register_Address <<=1; //left shift address one bit for command byte 
  MSP430F5529_Register_Address |=1; // Ensure read bit is set
  
  Serial.print("  Read Byte Command Sent: ");
  Serial.print(MSP430F5529_Register_Address,BIN);
  
  delay(100); 
  
  digitalWrite(CS, LOW); 
  delay(100); 
  SPI.transfer(MSP430F5529_Register_Address); // send address with read command to 
  delay(100); 
  uint8_t Response = SPI.transfer(0x00); 
  delay(100); 
  digitalWrite(CS, HIGH);
  
  Serial.print(" - Response Received: ");
  Serial.println(Response,BIN);
  return Response;
  delay(100); 
}
*/
//pretty sure this is bs from original code too, try commmenting out before completely deleting
/*void Reset_ADC()
{
 // Puts ADC into Reset Mode, i.e. stops ADC conversions until setup is complete.
  Write_MSP430F5529_Register (0x0D, B11000010); 
}
*/
//i dunno below, think it is also part of read function
/*
int32_t Read_MSP430F5529_24bit( uint8_t MSP430F5529_Register_Address)
  {
    uint8_t HB,MB,LB=0, CTRL=0;;
    int32_t adc0code=0;
    CTRL = 0;
    CTRL =(MSP430F5529_Register_Address<<1); //left shift address one digit for write command
    CTRL |= 1; //Turn on Read Operation by toggling last bit on
    
    digitalWrite(CS, LOW);
    delay(100); 
    SPI.transfer(CTRL); // send command byte to
    delay(100);  
    HB = SPI.transfer(0x0);//receive High Byte
    delay(100); 
    MB = SPI.transfer(0x0);//receive Middle Byte
    delay(100); 
    LB = SPI.transfer(0x0);//receive Low Byte
    delay(100); 
    digitalWrite(CS, HIGH);
    delay(100); 
    
    adc0code = HB;
    adc0code = adc0code<<8;
    adc0code |= MB;
    adc0code = adc0code<<8;
    adc0code |= LB;         //connecting the 3 bytes to one number
    
    
    return adc0code;// returning result
  }*/
