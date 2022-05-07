#include <Arduino.h>

const long SAMPLING_RATE = 10;
const long SAMPLING_INTERVAL = 1000 / SAMPLING_RATE;

const int LEFT = 0;
const int RIGHT = 1;
const int CLK_PIN[2] = {3, 5};
const int DATA_PIN[2] = {2, 4};

static uint8_t prevNextCode[] = {0,0};
static uint16_t store[] = {0,0};
int ticks[2] = {0, 0};
unsigned long lastUpdate = millis();

void setup() {
    pinMode(DATA_PIN[LEFT], INPUT_PULLUP);
    pinMode(CLK_PIN[LEFT], INPUT_PULLUP);
    pinMode(DATA_PIN[RIGHT], INPUT_PULLUP);
    pinMode(CLK_PIN[RIGHT], INPUT_PULLUP);
    Serial.begin(57600);
}


// https://www.best-microcontroller-projects.com/rotary-encoder.html
int8_t read_rotary(int wheelIndex) {
    static int8_t rot_enc_table[] = {0,1,1,0,1,0,0,1,1,0,0,1,0,1,1,0};

    prevNextCode[wheelIndex] <<= 2;
    if (digitalRead(DATA_PIN[wheelIndex])) prevNextCode[wheelIndex] |= 0x02;
    if (digitalRead(CLK_PIN[wheelIndex])) prevNextCode[wheelIndex] |= 0x01;
    prevNextCode[wheelIndex] &= 0x0f;

    // If valid then store as 16 bit data.
    if  (rot_enc_table[prevNextCode[wheelIndex]] ) {
        store[wheelIndex] <<= 4;
        store[wheelIndex] |= prevNextCode[wheelIndex];
        if ((store[wheelIndex]&0xff)==0x2b) return -1;
        if ((store[wheelIndex]&0xff)==0x17) return 1;
    }
    return 0;
}

void send() {
    Serial.print(ticks[LEFT]);
    Serial.print(",");
    Serial.println(ticks[RIGHT]);
    ticks[LEFT] = ticks[RIGHT] = 0;
}

void loop() {
    ticks[LEFT] += read_rotary(LEFT);
    ticks[RIGHT] += read_rotary(RIGHT);

    unsigned long now = millis();
    if (lastUpdate + SAMPLING_INTERVAL < now) {
        send();
        lastUpdate = now;
    }
}
