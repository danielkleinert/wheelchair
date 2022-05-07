#include <Arduino.h>
#include <EnableInterrupt.h>

const volatile long SAMPLING_RATE = 10;
const volatile long DEBOUNCE_MILLIS = 2;
const volatile int LEFT = 0;
const volatile int RIGHT = 1;
const volatile int CLK_PIN[2] = {3, 5};
const volatile int DATA_PIN[2] = {2, 4};

volatile int ticks[2] = {0, 0};
volatile unsigned long lastChanged[2] = {0, 0};

void stepped(int wheelIndex) {
    const unsigned long currentMillis = millis();
    if (lastChanged[wheelIndex] + DEBOUNCE_MILLIS > currentMillis) return;
    const int direction_rectifier = wheelIndex ? 1 : -1; // forward is different as axles point in opposite directions
    ticks[wheelIndex] += (digitalRead(DATA_PIN[wheelIndex]) ? 1 : -1) * direction_rectifier;
    lastChanged[wheelIndex] = currentMillis;
}

void steppedLeft() {
    stepped(LEFT);
}

void steppedRight() {
    stepped(RIGHT);
}

void setup() {
    pinMode(DATA_PIN[LEFT], INPUT_PULLUP);
    pinMode(CLK_PIN[LEFT], INPUT_PULLUP);
    enableInterrupt(CLK_PIN[LEFT], steppedLeft, FALLING);    pinMode(DATA_PIN[LEFT], INPUT_PULLUP);
    pinMode(DATA_PIN[RIGHT], INPUT_PULLUP);
    pinMode(CLK_PIN[RIGHT], INPUT_PULLUP);
    enableInterrupt(CLK_PIN[RIGHT], steppedRight, FALLING);

    Serial.begin(57600);
}

void loop() {
    Serial.print(ticks[LEFT]);
    Serial.print(",");
    Serial.println(ticks[RIGHT]);
    ticks[LEFT] = ticks[RIGHT] = 0;
    delay(1000/SAMPLING_RATE);
}

