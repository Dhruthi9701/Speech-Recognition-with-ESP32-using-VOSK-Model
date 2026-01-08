#include <Arduino.h>
#include <DFRobotDFPlayerMini.h>
#include "esp_sleep.h"

#define DFPLAYER_RX_PIN 18
#define DFPLAYER_TX_PIN 19

HardwareSerial DFSerial(2);
DFRobotDFPlayerMini dfplayer;

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(10); }
  Serial.println("\n[ESP32] DFPlayer (jarvis/hello/hi/play + hammer time) starting…");

  DFSerial.begin(9600, SERIAL_8N1, DFPLAYER_RX_PIN, DFPLAYER_TX_PIN);
  delay(200);

  if (!dfplayer.begin(DFSerial)) {
    Serial.println("[ERROR] Could not find DFPlayer! Check wiring & SD‐card.");
    while (true) { delay(1000); }
  }
  Serial.println("[OK] DFPlayer initialized.");
  dfplayer.setTimeOut(500);
  dfplayer.volume(25);
  dfplayer.EQ(DFPLAYER_EQ_NORMAL);
  dfplayer.outputDevice(DFPLAYER_DEVICE_SD);

  Serial.println("[READY] Waiting for PLAY1/PLAY2/PLAY3/PLAY4/SLEEP commands…");
}



void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    Serial.print("[ESP32] Received: ");
    Serial.println(cmd);

    if (cmd.equalsIgnoreCase("PLAY1")) {
      Serial.println("[ESP32] → Playing 0001.mp3");
      dfplayer.play(1);
    }
    else if (cmd.equalsIgnoreCase("PLAY2")) {
      Serial.println("[ESP32] → Playing 0002.mp3");
      dfplayer.play(2);
    }
    else if (cmd.equalsIgnoreCase("PLAY3")) {
      Serial.println("[ESP32] → Playing 0003.mp3");
      dfplayer.play(3);
    }
    else if (cmd.equalsIgnoreCase("PLAY4")) {
      Serial.println("[ESP32] → Playing 0004.mp3");
      dfplayer.play(4);
    }
    else if (cmd.equalsIgnoreCase("SLEEP")) {
      Serial.println("[ESP32] → “hammer time” triggered. Playing 0005.mp3 then deep‐sleep.");
      dfplayer.play(5);
      delay(2000);
      dfplayer.stop();
      Serial.flush();
      delay(100);
      esp_deep_sleep_start();
    }
    else {
      Serial.println("[ESP32] → Unrecognized command.");
    }
  }
  delay(10);
}



/*
  ESP32 + DFPlayer Mini (GPIO18/19) with “hammer time” → play & deep-sleep

  - PLAY1  → play 0001.mp3
  - PLAY2  → play 0002.mp3
  - PLAY3  → play 0003.mp3
  - PLAY4  → play 0004.mp3
  - SLEEP  → play 0005.mp3 (“hammer time”), then deep-sleep
  All the mp3 files are to be stored in an SD Card which is then inserted to the DFPlayer.

  Wiring:
    ESP32 GPIO19  → DFPlayer RX
    ESP32 GPIO18  ← DFPlayer TX
    ESP32 VIN (5 V)→ DFPlayer VCC
    ESP32 GND     → DFPlayer GND
    DFPlayer SPK_1/SPK_2 → Speaker

  Required installations for this project:
    1. “ESP32 by Espressif Systems” (via Arduino Boards Manager)
    2. “DFRobotDFPlayerMini” library (via Arduino Library Manager)
*/

