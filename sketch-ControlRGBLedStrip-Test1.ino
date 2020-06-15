#include <FastLED.h>

#define LED_PIN 6
#define NUM_LEDS 150

CRGB leds[NUM_LEDS];

int colors[3];

void setup() {
  Serial.begin(9600); //initialize serial COM at 9600 baudrate
  
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
}

void loop() {
  while (Serial.available() >= 3) {
    for (int i = 0; i < 3; i++) {
      colors[i] = Serial.read();
    }

    leds[0] = CRGB(colors[0], colors[1], colors[2]);

    FastLED.show();
  }
}
