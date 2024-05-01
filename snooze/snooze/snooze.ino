// SNOOZE
// I2C controlled power-saving self-shutdown
// for Raspberry Pi, implemented on a Trinket
// companion microcontroller
//
// When I2C commands, wait for a time, then 
// the power is shut off for requested period.
//
// I2C should send three bytes:
//  1 is time-off delay
//  2 and 3 are time-on delay
// Units are five second increments
//

#include <Wire.h>

// global counter variables for sleep timing
byte off_ctr = 0;
unsigned int on_ctr = 0;

// flashing LED utilities

#define LED_PIN 13

#define BLINK_TIME 250
#define BLINKS_PER_CYC 20

void fast_blink_delay(){
  int ii;
  for (ii=0;ii<BLINKS_PER_CYC;ii+=2){
    digitalWrite(LED_PIN,HIGH);
    delay(BLINK_TIME);
    digitalWrite(LED_PIN,LOW);
    delay(BLINK_TIME);
  }
}

void slow_blink_delay(){
  int ii;
  digitalWrite(LED_PIN,HIGH);
  delay(BLINK_TIME);
  digitalWrite(LED_PIN,LOW);
  for (ii=1;ii<BLINKS_PER_CYC;ii++){
    delay(BLINK_TIME);
  }
}

void led_on_delay(){
  int ii;
  digitalWrite(LED_PIN,LOW);
  delay(BLINK_TIME);
  digitalWrite(LED_PIN,HIGH);
  for (ii=1;ii<BLINKS_PER_CYC;ii++){
    delay(BLINK_TIME);
  }
}

#define PWR_PIN 3

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_PIN, OUTPUT);
  pinMode(PWR_PIN, OUTPUT);
  off_ctr = 0;
  on_ctr = 0;
  digitalWrite(PWR_PIN, HIGH);
  // initialize the I2C
  Wire.begin(4);
  Wire.onReceive(i2c_recv);
  // serial debugging
  Serial.begin(9600);
}

void i2c_recv(int how_many){
  int ii;
  Serial.printf("Got %d bytes\n", how_many);
  if (how_many==4) {
    off_ctr = Wire.read();
    // will discard next byte - now many bytes coming
    unsigned int on_tmp = Wire.read();
    //assert(on_tmp==2);
    // now the two byte off timer value, high then low
    on_tmp = Wire.read();
    on_tmp = on_tmp << 8;
    on_tmp |= Wire.read();
    on_ctr = on_tmp;
  }
  else {
    for (ii=0;ii<how_many;ii++) {
      Serial.printf("%d ", Wire.read());
    }
  }
  Serial.printf("\n");
}

void loop() {
  // debug output
  Serial.printf("off_ctr %d on_ctr %d \n",off_ctr,on_ctr);
  // timer logic
  if (off_ctr>0) {
    // waiting to shutdown
    off_ctr--;
    fast_blink_delay();
    if (off_ctr==0) {
      digitalWrite(PWR_PIN, LOW);
    }
  }
  else if (on_ctr>0) {
    // snooze! - waiting to come back on
    on_ctr--;
    slow_blink_delay();
  }
  else {
    digitalWrite(PWR_PIN, HIGH);
    led_on_delay();
  }
}
