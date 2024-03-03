#include <LiquidCrystal.h>
#include <FastLED.h>

#define NUM_LEDS 20
#define DATA_PIN 6

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

int piezo = A0;
// int past = 0;

float intensity;
CRGB color;

CRGB leds[NUM_LEDS];
CRGB temp[NUM_LEDS];

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);  // GRB ordering is assumed
 
  lcd.print("Piezo:");
  lcd.setCursor(0, 1);
  lcd.print(analogRead(piezo));
}

void loop() {
  while (!Serial.available());
  String data = Serial.readString();
  if (data.length() <= 3){
    int c = data.toInt();
    color = ColorFromPalette(RainbowColors_p, c);

  }
  else {
    intensity = data.toInt();
  }
  // int frequency;
  // for (int i = 0; i < data.length(); i++){
  //   int mid = data.indexOf("|");
  //   intensity = data.substring(0, mid-1).toInt();
  //   frequency = data.substring(mid, data.length()).toInt();

  // }
  
  Serial.println(data);
  // Serial.print("intensity" + intensity);
  // Serial.print(" frequency" + frequency);
  // int a = current/100;
  // int b =  current % 10 * 10 + current % 100;

  // if (b > 5) {
  //   color = CRGB::Red;
  // }
  // else{
  //   color = CRGB::Blue;
  // }
  
  for (int i = 0; i <= NUM_LEDS; i++) {
        // Serial.print(i);
    if (i <= intensity / 3000 * 10) {
      leds[i] = color;
      // if (i % 2 == 0 ) {
      //   i = 19 - i;
      // }

      // if (i > NUM_LEDS/2 - 1){
      //   i = map(i, 10, 20, 20, 10)
      //   leds[i] = CRGB::Red;
      // }
      
    } else {
      leds[i] = CRGB::Black;
    }
  }
  FastLED.show();


  // leds[past] = CRGB::HTMLColorCode;
  // past = current;
  // delay(50);
}
