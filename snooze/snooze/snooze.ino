// SNOOZE
// I2C controlled power-saving self-shutdown
// for Raspberry Pi, implemented on a Trinket
// companion microcontroller
//
// When I2C commands, power is shut off
// requested period.
//

// global counter variables for sleep timing
byte off_ctr = 0;
unsigned int on_ctr = 0;

// flashing LED utilities

#define LED_PIN 13

#define DELAY_TIME 500

void fast_blink_delay(){
  int ii;
  for (ii=0;ii<5;ii++){
    digitalWrite(LED_PIN,HIGH);
    delay(DELAY_TIME);
    digitalWrite(LED_PIN,LOW);
    delay(DELAY_TIME);
  }
}

void slow_blink_delay(){
  int ii;
  digitalWrite(LED_PIN,HIGH);
  delay(DELAY_TIME);
  digitalWrite(LED_PIN,LOW);
  for (ii=0;ii<9;ii++){
    delay(DELAY_TIME);
  }
}

void led_on_delay(){
  int ii;
  digitalWrite(LED_PIN,HIGH);
  for (ii=0;ii<10;ii++){
    delay(DELAY_TIME);
  }
}

#define PWR_PIN 2

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_PIN, OUTPUT);
  pinMode(PWR_PIN, OUTPUT);
  off_ctr = 0;
  on_ctr = 0;
  digitalWrite(PWR_PIN, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
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