// G29 pedals -> Arduino Uno -> Serial output
// Uno will NOT be a USB joystick by itself.
// It just streams pedal positions to the PC.

const int CLUTCH_PIN   = A0;  // DB9 pin 4
const int BRAKE_PIN    = A1;  // DB9 pin 3
const int THROTTLE_PIN = A2;  // DB9 pin 2

// Optional simple smoothing (bigger = smoother but slower)
const int SMOOTHING = 4;

int clutchFilt   = 0;
int brakeFilt    = 0;
int throttleFilt = 0;

void setup() {
  Serial.begin(115200);

  pinMode(CLUTCH_PIN,   INPUT);
  pinMode(BRAKE_PIN,    INPUT);
  pinMode(THROTTLE_PIN, INPUT);

  // Prime filters
  clutchFilt   = analogRead(CLUTCH_PIN);
  brakeFilt    = analogRead(BRAKE_PIN);
  throttleFilt = analogRead(THROTTLE_PIN);
}

void loop() {
  int clutchRaw   = analogRead(CLUTCH_PIN);   // 0–1023
  int brakeRaw    = analogRead(BRAKE_PIN);
  int throttleRaw = analogRead(THROTTLE_PIN);

  // Simple low-pass filter
  clutchFilt   = clutchFilt   + (clutchRaw   - clutchFilt)   / SMOOTHING;
  brakeFilt    = brakeFilt    + (brakeRaw    - brakeFilt)    / SMOOTHING;
  throttleFilt = throttleFilt + (throttleRaw - throttleFilt) / SMOOTHING;

  // Invert if needed (some sets are "high when released")
  // Uncomment these if pressing the pedal makes the value go DOWN:
  // clutchFilt   = 1023 - clutchFilt;
  // brakeFilt    = 1023 - brakeFilt;
  // throttleFilt = 1023 - throttleFilt;

  // Send one line per frame: C:xxxx B:yyyy T:zzzz
  Serial.print("C:");
  Serial.print(clutchFilt);
  Serial.print(" B:");
  Serial.print(brakeFilt);
  Serial.print(" T:");
  Serial.println(throttleFilt);

  delay(10);  // ~100 Hz
}
