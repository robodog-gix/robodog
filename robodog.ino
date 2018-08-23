#include <Wire.h>
#include <TimerOne.h>
#include <NewPing.h>
#include <ArduinoJson.h>

#define    MPU9250_ADDRESS            0x68
#define    MAG_ADDRESS                0x0C
#include <Adafruit_NeoPixel.h>


#define PIN 6

#define TRIGGER_PIN  3  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     2  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, PIN, NEO_GRB + NEO_KHZ800);

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.


// This function read Nbytes bytes from I2C device at address Address. 
// Put read bytes starting at register Register in the Data array. 
void I2Cread(uint8_t Address, uint8_t Register, uint8_t Nbytes, uint8_t* Data)
{
  // Set register address
  Wire.beginTransmission(Address);
  Wire.write(Register);
  Wire.endTransmission();
  
  // Read Nbytes
  Wire.requestFrom(Address, Nbytes); 
  uint8_t index=0;
  while (Wire.available())
    Data[index++]=Wire.read();
}

int response;
// Write a byte (Data) in device (Address) at register (Register)
void I2CwriteByte(uint8_t Address, uint8_t Register, uint8_t Data)
{
  // Set register address
  Wire.beginTransmission(Address);
  Wire.write(Register);
  Wire.write(Data);
  Wire.endTransmission();
  Serial.println("Hi2");
}



// Initial time
long int ti;

volatile bool intFlag=false;

String oldSerIn=0;
String serIn=0;

// Initializations
void setup()
{
  
  strip.begin();
  strip.setBrightness(64);
  strip.show(); // Initialize all pixels to 'off'
  // Arduino initializations
  Wire.begin();
  Serial.begin(115200);
  
  
  // Set by pass mode for the magnetometers
  I2CwriteByte(MPU9250_ADDRESS,0x37,0x02);
  
  // Request continuous magnetometer measurements in 16 bits
  I2CwriteByte(MAG_ADDRESS,0x0A,0x16);
  
   pinMode(13, OUTPUT);
  Timer1.initialize(10000);         // initialize timer1, and set a 1/2 second period
  Timer1.attachInterrupt(callback);  // attaches callback() as a timer overflow interrupt
  
  
  // Store initial time
  ti=millis();
  
}





// Counter
long int cpt=0;

void callback()
{ 
  intFlag=true;
  digitalWrite(13, digitalRead(13) ^ 1);
}

// Main loop, read and display data
void loop()
{
  
  while (!intFlag);
  intFlag=false;
  
  
  // Display time
  //Serial.print (millis()-ti,DEC);
  //Serial.print ("\t");

  
  // _______________
  // ::: Counter :::
  
  // Display data counter
//  Serial.print (cpt++,DEC);
//  Serial.print ("\t");
  
 
 
  
  // _____________________
  // :::  Magnetometer ::: 

  
  // Read register Status 1 and wait for the DRDY: Data Ready
  
  uint8_t ST1;
  do
  {
    I2Cread(MAG_ADDRESS,0x02,1,&ST1);
  }
  while (!(ST1&0x01));

  // Read magnetometer data  
  uint8_t Mag[7];  
  I2Cread(MAG_ADDRESS,0x03,7,Mag);
  

  // Create 16 bits values from 8 bits data
  
  // Magnetometer
  int mx=-(Mag[3]<<8 | Mag[2]);
  int my=-(Mag[1]<<8 | Mag[0]);
  int mz=-(Mag[5]<<8 | Mag[4]);
  
  float az;
  // Magnetometer
  if (my+180>=0){
  az = -atan((float)(mx+200)/(float)(my+180))*180/3.14+180;
  }
  if (my+180<0){
   az = atan((float)(mx+200)/(float)(my+
   180))*180/3.14+180;
  }
  
  
  Serial.print (mx+200,DEC); 
  Serial.print (",");
  Serial.print (my-70,DEC);
  Serial.print (",");
  Serial.print (mz-700,DEC);  
  Serial.print (",");
  Serial.print(az);
  Serial.print(",");
  
 
  
  //Serial.print("Ping: ");
  Serial.print(sonar.ping_cm()); // Send ping, get distance in cm and print result (0 = outside set distance range)
  //Serial.println("cm");
  
  
  
  
  while(Serial.available()>0){
    serIn= Serial.readString();
    Serial.print(serIn);
 
 if(serIn!=oldSerIn){
 if(serIn=="0"){
colorWipe(strip.Color(255, 0, 0), 1);} // Red
if(serIn=="1"){
  colorWipe(strip.Color(0, 255, 0), 1);} // Green
  if(serIn=="2"){
  colorWipe(strip.Color(0, 0, 255), 1);} // Blue
  }}
  oldSerIn=serIn;
      // End of line
  Serial.println("");
  delay(100);
}



void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }
}

