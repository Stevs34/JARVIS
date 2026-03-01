// JARVIS Arduino Controller
// Controls LEDs, fan motor, and physical buttons
// Communicates with Python via Serial

// LED Pins
const int RED_LED = 2;
const int GREEN_LED = 3;
const int BLUE_LED = 4;
const int YELLOW_LED = 5;
const int RGB_RED = 6;
const int RGB_GREEN = 9;
const int RGB_BLUE = 10;

// Button Pins
const int BTN_1 = 7;   // Movie mode
const int BTN_2 = 8;   // Study mode
const int BTN_3 = 11;  // Party mode
const int BTN_4 = 12;  // Good morning
const int BTN_5 = 13;  // Stop/Cancel

// Motor Pin (via L298N)
const int MOTOR_PIN = 44;
const int MOTOR_SPEED = 45; // PWM pin for speed control

// Status LED states
bool isListening = false;
bool isProcessing = false;

// Button debounce
unsigned long lastDebounce = 0;
const int DEBOUNCE_DELAY = 200;

void setup() {
  Serial.begin(9600);

  // Set LED pins as output
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(RGB_RED, OUTPUT);
  pinMode(RGB_GREEN, OUTPUT);
  pinMode(RGB_BLUE, OUTPUT);

  // Set button pins as input with pullup
  pinMode(BTN_1, INPUT_PULLUP);
  pinMode(BTN_2, INPUT_PULLUP);
  pinMode(BTN_3, INPUT_PULLUP);
  pinMode(BTN_4, INPUT_PULLUP);
  pinMode(BTN_5, INPUT_PULLUP);

  // Set motor pins as output
  pinMode(MOTOR_PIN, OUTPUT);
  pinMode(MOTOR_SPEED, OUTPUT);

  // Boot animation
  bootAnimation();

  Serial.println("JARVIS_READY");
}

void loop() {
  // Check for commands from Python
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    handleCommand(command);
  }

  // Check physical buttons
  checkButtons();
}

void handleCommand(String cmd) {
  if (cmd == "STATUS_LISTENING") {
    setRGB(0, 0, 255);        // Blue — listening
    digitalWrite(GREEN_LED, LOW);
  }
  else if (cmd == "STATUS_PROCESSING") {
    setRGB(255, 165, 0);      // Orange — processing
  }
  else if (cmd == "STATUS_SPEAKING") {
    setRGB(0, 255, 0);        // Green — speaking
  }
  else if (cmd == "STATUS_IDLE") {
    setRGB(0, 0, 20);         // Dim blue — idle
    allLedsOff();
  }
  else if (cmd == "LIGHTS_ON") {
    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(YELLOW_LED, HIGH);
    Serial.println("LIGHTS_ON_OK");
  }
  else if (cmd == "LIGHTS_OFF") {
    allLedsOff();
    Serial.println("LIGHTS_OFF_OK");
  }
  else if (cmd == "MOVIE_MODE") {
    allLedsOff();
    setRGB(20, 0, 40);        // Deep purple
    Serial.println("MOVIE_MODE_OK");
  }
  else if (cmd == "STUDY_MODE") {
    allLedsOff();
    setRGB(255, 255, 255);    // Bright white
    digitalWrite(GREEN_LED, HIGH);
    Serial.println("STUDY_MODE_OK");
  }
  else if (cmd == "PARTY_MODE") {
    partyMode();
    Serial.println("PARTY_MODE_OK");
  }
  else if (cmd == "GOOD_MORNING") {
    allLedsOff();
    setRGB(255, 147, 41);     // Warm orange
    Serial.println("GOOD_MORNING_OK");
  }
  else if (cmd == "FAN_ON") {
    digitalWrite(MOTOR_PIN, HIGH);
    analogWrite(MOTOR_SPEED, 200);
    Serial.println("FAN_ON_OK");
  }
  else if (cmd == "FAN_OFF") {
    digitalWrite(MOTOR_PIN, LOW);
    analogWrite(MOTOR_SPEED, 0);
    Serial.println("FAN_OFF_OK");
  }
  else if (cmd.startsWith("FAN_SPEED_")) {
    int speed = cmd.substring(10).toInt();
    analogWrite(MOTOR_SPEED, map(speed, 0, 100, 0, 255));
    Serial.println("FAN_SPEED_OK");
  }
  else if (cmd == "ALERT") {
    alertAnimation();
  }
}

void checkButtons() {
  if (millis() - lastDebounce < DEBOUNCE_DELAY) return;

  if (digitalRead(BTN_1) == LOW) {
    Serial.println("BTN_MOVIE_MODE");
    lastDebounce = millis();
  }
  else if (digitalRead(BTN_2) == LOW) {
    Serial.println("BTN_STUDY_MODE");
    lastDebounce = millis();
  }
  else if (digitalRead(BTN_3) == LOW) {
    Serial.println("BTN_PARTY_MODE");
    lastDebounce = millis();
  }
  else if (digitalRead(BTN_4) == LOW) {
    Serial.println("BTN_GOOD_MORNING");
    lastDebounce = millis();
  }
  else if (digitalRead(BTN_5) == LOW) {
    Serial.println("BTN_STOP");
    lastDebounce = millis();
  }
}

void setRGB(int r, int g, int b) {
  analogWrite(RGB_RED, r);
  analogWrite(RGB_GREEN, g);
  analogWrite(RGB_BLUE, b);
}

void allLedsOff() {
  digitalWrite(RED_LED, LOW);
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(BLUE_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  setRGB(0, 0, 0);
}

void bootAnimation() {
  // Sequence through all LEDs on startup
  digitalWrite(RED_LED, HIGH);    delay(100);
  digitalWrite(GREEN_LED, HIGH);  delay(100);
  digitalWrite(BLUE_LED, HIGH);   delay(100);
  digitalWrite(YELLOW_LED, HIGH); delay(100);
  setRGB(255, 0, 0);              delay(100);
  setRGB(0, 255, 0);              delay(100);
  setRGB(0, 0, 255);              delay(100);
  setRGB(255, 255, 255);          delay(200);
  allLedsOff();
}

void partyMode() {
  for (int i = 0; i < 5; i++) {
    setRGB(255, 0, 0);   delay(100);
    setRGB(0, 255, 0);   delay(100);
    setRGB(0, 0, 255);   delay(100);
    setRGB(255, 0, 255); delay(100);
    setRGB(255, 255, 0); delay(100);
  }
  setRGB(255, 0, 128);
}

void alertAnimation() {
  for (int i = 0; i < 3; i++) {
    setRGB(255, 0, 0);
    digitalWrite(RED_LED, HIGH);
    delay(200);
    allLedsOff();
    delay(200);
  }
}
