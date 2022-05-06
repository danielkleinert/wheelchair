#include <Arduino.h>
#include <EnableInterrupt.h>
#define NUM_TRIGGERS 10

volatile long lastChanged = 0;
const volatile long debounceMillis = 2;
const volatile long movementTimeoutMillis = 150;
volatile bool stopped = false;

struct Trigger {
    Trigger()
            : milliSeconds(milliSeconds)
            , dir(true)
    { }
    Trigger(long milliSeconds, bool dir)
            : milliSeconds(milliSeconds)
            , dir(dir)
    { }
    long milliSeconds;
    bool dir;
};

Trigger triggers[NUM_TRIGGERS] = {};
int triggerIndex = 0;

float getSpeed() {
    int directionCounter = 0;
    for (int i = 0; i < NUM_TRIGGERS; i++) {
        directionCounter += triggers[i].dir ? 1 : -1;
    }
    const long firstTriggerTime = triggers[(triggerIndex + 1) % NUM_TRIGGERS].milliSeconds;
    const long dur = millis() - firstTriggerTime;
    const float speed = 1000.0f / dur;
    return speed * (directionCounter < 0 ? 1.0f : -1.0f);
}


void stepped() {
    const int dir = digitalRead(2);
    const long currentMillis = millis();
    if (lastChanged + debounceMillis > currentMillis) return;

    //Serial.println(dir);
    if (triggerIndex % 2 == 0) {
        Serial.println((int) ceil(getSpeed()));
    }
    lastChanged = millis();

    triggers[triggerIndex] = Trigger(currentMillis, dir);
    triggerIndex = (triggerIndex + 1) % NUM_TRIGGERS;
    stopped = false;
}

void setup() {
    pinMode(2, INPUT_PULLUP);
    pinMode(3, INPUT_PULLUP);

    enableInterrupt(3, stepped, FALLING);

    Serial.begin(57600);
    Serial.println("start");
}

void loop() {
    if (!stopped)
    {
        const long currentMillis = millis();
        if (lastChanged + movementTimeoutMillis < currentMillis) {
            Serial.println("0");
            lastChanged = currentMillis;
            stopped = true;
            for (int i = 0; i < NUM_TRIGGERS; i++) {
                triggers[i] = Trigger(currentMillis - 100, i % 2 == 0);
            }
        }
    }
    delay(10);
}

