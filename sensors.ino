

// 
//   FILE:  dht11_test1.pde
// PURPOSE: DHT11 library test sketch for Arduino
//


#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2561_U.h>
#include <dht11.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 5

OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensors(&oneWire);


dht11 DHT11;
Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 12345);
float Celcius=0;
int led=0;

int pump1=0;
#define DHT11PIN 2

void setup()
{
  Serial.begin(115200);
  
   tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_13MS);
  tsl.enableAutoRange(true);  
  //Serial.println("DHT11 TEST PROGRAM ");
  //Serial.print("LIBRARY VERSION: ");
  //Serial.println(DHT11LIB_VERSION);
  //Serial.println();
  sensors.begin();
  pinMode(10,OUTPUT);
  digitalWrite(10,HIGH);
}

void loop()
{
 // Serial.println("\n");
  sensors_event_t event;
  tsl.getEvent(&event);
 
 sensors.requestTemperatures(); 
 

  int chk = DHT11.read(DHT11PIN);

  //Serial.print("Read sensor: ");
  switch (chk)
  {
    case DHTLIB_OK: 
    //Serial.println("OK"); 
    break;
    case DHTLIB_ERROR_CHECKSUM: 
    //Serial.println("Checksum error"); 
    break;
    case DHTLIB_ERROR_TIMEOUT: 
    //Serial.println("Time out error"); 
    break;
    default: 
    //Serial.println("Unknown error"); 
    break;
  }
  //Serial.print("Water Level: ");
Serial.print(analogRead(A0));
Serial.print(",");
  //Serial.print("Humidity (%): ");
  Serial.print(float(DHT11.humidity), 2);
Serial.print(",");
  //Serial.print("Temperature (C): ");
  Serial.print(float(DHT11.temperature), 2);
   /* Display the results (light is measured in lux) */
    Serial.print(",");
  if (event.light)
  {
    Serial.print(event.light);
   
  }
  Celcius=sensors.getTempCByIndex(0);
  Serial.print(",");
  Serial.print(Celcius);
  while(Serial.available()>0){
    String serIn= Serial.readString();
    
 
    StaticJsonBuffer<200> jsonBuffer;

JsonObject& root = jsonBuffer.parseObject(serIn);

 led = root["LED"];

 pump1= root["Pump1"];
if(pump1==0){
  digitalWrite(10, HIGH);}
  else if(pump1==1){
  digitalWrite(10,LOW);}
  delay(200);
}

  Serial.println("");
  
}
//
// END OF FILE
//
