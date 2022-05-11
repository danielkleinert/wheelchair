#include <Arduino.h>
#include <Encoder.h>
#include <arduino-timer.h>

auto timer = timer_create_default();

const volatile long SAMPLING_RATE = 10;
//   Best Performance: both pins have interrupt capability (2, 3)
//   Good Performance: only the first pin has interrupt capability
//   Low Performance:  neither pin has interrupt capability
Encoder leftWheel(3, 5);
Encoder rightWheel(2, 4);

bool sendData(void *) {
    Serial.print(leftWheel.read());
    Serial.print(",");
    Serial.println(-rightWheel.read());
    rightWheel.write(0);
    leftWheel.write(0);
    return true; // keep timer active
}

void setup() {
    Serial.begin(57600);
    timer.every(1000/SAMPLING_RATE, sendData);
}

void loop() {
    timer.tick();
}
