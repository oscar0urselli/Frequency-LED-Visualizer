#include <FastLED.h>

#define LED_PIN 6  // Pin of the signal
#define NUM_LEDS 150  // Number of leds

CRGB leds[NUM_LEDS];

int colors[3];  // Colors of the led

#define updateLEDS 1

void setup() {
  Serial.begin(9600); //initialize serial COM at 9600 baudrate
  
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[1] = CRGB(0, 0, 0);
  }
  FastLED.show();
}

void loop() {
  while (Serial.available() >= 3) {
    for (int i = 0; i < 3; i++) {
      colors[i] = Serial.read();
    }

    for (int i = NUM_LEDS - 1; i >= updateLEDS; i--) {
      leds[i] = leds[i - updateLEDS];
    }
    for (int i = 0; i < updateLEDS; i++) {
      leds[i] = CRGB(colors[0], colors[1], colors[2]);
    }

    FastLED.show();
  }
}
