

// Code to use SoftwareSerial
#include <SoftwareSerial.h>
SoftwareSerial espSerial =  SoftwareSerial(2,3);      // arduino RX pin=2  arduino TX pin=3    connect the arduino RX pin to esp8266 module TX pin   -  connect the arduino TX pin to esp8266 module RX pin



#include <DHT.h>        
#define DHTPIN 8                
#define DHTTYPE DHT22 
DHT dht(DHTPIN, DHTTYPE);
int lpgA0 = A5;

String apiKey = "UTQ0MV0MCGDTU6IN";     

String ssid="TECNO SPARK 4";    // Wifi network SSID
String password ="qqqqwwww";  // Wifi network password

boolean DEBUG=true;

//======================================================================== showResponce
void showResponse(int waitTime){
    long t=millis();
    char c;
    while (t+waitTime>millis()){
      if (espSerial.available()){
        c=espSerial.read();
        if (DEBUG) Serial.print(c);
      }
    }
                   
}

//========================================================================
boolean thingSpeakWrite(float value1, float value2, float value3, float value4){
  String cmd = "AT+CIPSTART=\"TCP\",\"";                  // TCP connection
  cmd += "184.106.153.149";                               // api.thingspeak.com
  cmd += "\",80"; 
  espSerial.println(cmd);
  if (DEBUG) Serial.println(cmd);
  if(espSerial.find("Error")){
    if (DEBUG) Serial.println("AT+CIPSTART error");
    return false;
  }
  
  
  String getStr = "GET /update?api_key=";   // prepare GET string
  getStr += apiKey;
  
  getStr +="&field1=";
  getStr += String(value1);
  getStr +="&field2=";
  getStr += String(value2);
  getStr +="&field3=";
  getStr += String(value3);
  getStr +="&field4=";
  getStr += String(value4);
  // ...
  getStr += "\r\n\r\n";

  // send data length
  cmd = "AT+CIPSEND=";
  cmd += String(getStr.length());
  espSerial.println(cmd);
  if (DEBUG)  Serial.println(cmd);
  
  delay(100);
  if(espSerial.find(">")){
    espSerial.print(getStr);
    if (DEBUG)  Serial.print(getStr);
  }
  else{
    espSerial.println("AT+CIPCLOSE");
    // alert user
    if (DEBUG)   Serial.println("AT+CIPCLOSE");
    return false;
  }
  return true;
}
//================================================================================ setup
void setup() {                
  DEBUG=true;           // enable debug serial
  Serial.begin(9600); 
  pinMode(lpgA0, INPUT);
  dht.begin();          // Start DHT sensor
  
  espSerial.begin(9600);  // enable software serial
                          // Your esp8266 module's speed is probably at 115200. 
                          // For this reason the first time set the speed to 115200 or to your esp8266 configured speed 
                          // and upload. Then change to 9600 and upload again
  
  //espSerial.println("AT+RST");         // Enable this line to reset the module;
  //showResponse(1000);

  //espSerial.println("AT+UART_CUR=9600,8,1,0,0");    // Enable this line to set esp8266 serial speed to 9600 bps
  //showResponse(1000);
  
  

  espSerial.println("AT+CWMODE=1");   // set esp8266 as client
  showResponse(1000);

  espSerial.println("AT+CWJAP=\""+ssid+"\",\""+password+"\"");  // set your home router SSID and password
  showResponse(5000);

   if (DEBUG)  Serial.println("Setup completed");
   pinMode(8,OUTPUT);
}


// ====================================================================== loop
void loop() {

  // Read sensor values
   float t = dht.readTemperature();
   float h = dht.readHumidity();
   float gconc = analogRead(lpgA0);
        if (isnan(t) || isnan(h)) {
        if (DEBUG) Serial.println("Failed to read from DHT");
      }
        if (isnan(gconc)){
        if (DEBUG) Serial.println("Failed to read from MQ sensor!");
        }
      else {
          if (DEBUG)  Serial.println("Temp="+String(t)+" *C");
          if (DEBUG) Serial.println("Humidity="+String(h)+" %");
          if (DEBUG) Serial.println("Concentration="+String(gconc)+"ppm");
          float alp = float(h+t+gconc);
          float man = float((((550-alp)/550)*100));
          if (DEBUG) Serial.println("Safety Level="+String(man)+"%");
          if (alp >550)
          {
             digitalWrite(8,HIGH);
             delay(1000);
             digitalWrite(8,LOW);

             
             delay(1000);
           thingSpeakWrite(t,h,gconc,man); // Write values to thingspeak
      }
  
    
  // thingspeak needs 15 sec delay between updates,     
  delay(16000);  
      }
  }
