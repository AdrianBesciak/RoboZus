constexpr uint8_t numOfSensors = 4;

struct sensorData{
  uint8_t triggerPin;
  uint8_t echoPin;
  uint32_t reading;
};

sensorData sensors[numOfSensors]{{3, 2, 0}, {5, 4, 0}, {7, 6, 0}, {9, 8, 0}};

uint16_t brightnessRaw;

void updateSensor(sensorData &s)
{
  digitalWrite(s.triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(s.triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(s.triggerPin, LOW);
  uint32_t duration = pulseIn(s.echoPin, HIGH);
  s.reading = duration*17/10;
}

void updateAllSensors()
{
  for(auto& sensor : sensors)
    updateSensor(sensor);
}

void updateBrightness()
{
  brightnessRaw = digitalRead(A0);
}

void setup() {
  // initialize both serial ports:
  Serial.begin(115200);
  for(auto& sensor : sensors)
  {
    pinMode(sensor.triggerPin, OUTPUT);
    pinMode(sensor.echoPin, INPUT);
  }
}

void sendDummy()
{
  Serial.write('X');
}

void sendSensorReadings()
{
  for(uint8_t i=0;i<numOfSensors;++i)
  {
    Serial.print(sensors[i].reading);
    Serial.write(";\n"[i==(numOfSensors-1)]);
  }
}

void sendBrightnessReading()
{
  Serial.print(brightnessRaw);
  Serial.write('\n');
}

void serveSerial()
{
  if (Serial.available()) {
    char command = Serial.read();
    switch(command){
    case 'S':
      sendSensorReadings();
      break;
    case 'B':
      sendBrightnessReading();
      break;
    default:
      sendDummy();
    }
  }
}

void loop() {
  updateAllSensors();
  updateBrightness();
  serveSerial();
  //Serial.println(millis());
}
