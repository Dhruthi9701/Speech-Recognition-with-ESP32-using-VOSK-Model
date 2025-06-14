# Speech-Recognition-with-ESP32-using-VOSK-Model

• This project transforms your **ESP32 and DFPlayer Mini** into a smart, hands‑free **audio assistant**. Speak simple keywords like **“jarvis”, “hello”, “hi”, “play”, or “hammer time”** to trigger different MP3 tracks.\
• This setup uses **Vosk speech‑recognition** on your laptop to detect commands, sends them over serial to the ESP32, which then plays the matching audio - and even deep‑sleeps after “hammer time.” \
• The result is a seamless wake‑word‑controlled playback experience.

## 🗂️ Table of Contents:

1. Features
2. Hardware Components
3. Wiring & Connections
4. Software Requirements
5. Arduino Sketch Overview
6. Python Wake-Word Listener
7. Directory Structure
8. Step-by-Step Setup & Usage
9. Configuration Options
10. Troubleshooting


## 🧩 1. Features:

**✔️ Multiple Triggers:**

  • “jarvis” → play 0001.mp3 ("Did someone say genius?")\
  • “hello” → play 0002.mp3 ("Hello, I'm Listening.")\
  • “hi” → play 0003.mp3 ("Yes Boss!")\
  • “play” → play 0004.mp3 (Music(larger mp3 file))

**💤 Deep‑Sleep Mode:**

  • “hammer time” → play 0005.mp3 ("OK.... Hammer Time."), then enter deep‑sleep 

**🎵 Standalone Playback:**

  • ESP32 + DFPlayer handle MP3 after trigger

**🖥️ PC‑Side Wake‑Word Detection:**

  • Uses Vosk on your mic, sends serial commands




## 💡 2. Hardware Components:

1. ESP32 Dev Module
2. DFPlayer Mini MP3 Module
3. 8 Ω Speaker (up to 3 W)
4. MicroSD Card (FAT32; files 0001.mp3–0005.mp3)
5. Micro‑USB Cable (for programming ESP32)
6. Jumper Wires




## 🔌 3. Wiring & Connections:

1. ESP32 VIN (5 V)    → DFPlayer VCC  
2. ESP32 GND          → DFPlayer GND  
3. ESP32 GPIO19       → DFPlayer RX (soft‑TX) 
4. ESP32 GPIO18       ← DFPlayer TX (soft‑RX)  
5. DFPlayer SPK_1     → Speaker +  
6. DFPlayer SPK_2     → Speaker – 




## 📦 4. Software Requirements:

**Arduino IDE Side:**\
  • Arduino IDE ≥ 1.8.x

**ESP32 Board Support:**\
  • Tools → Boards Manager → “esp32 by Espressif Systems”

**DFRobotDFPlayerMini Library:**\
  • Sketch → Include Library → Manage Libraries...

**Python Host Side:**\
  • pip install vosk sounddevice pyserial\
  ✅ Download and extract a Vosk model (e.g. vosk-model-small-en-us-0.15) into your project folder.




## 🎯 5. Arduino Sketch Overview:

At the top of esp32_to_dfplayer.ino:

#include <Arduino.h>\
#include <HardwareSerial.h>\
#include <DFRobotDFPlayerMini.h>

📟 The ESP32 listens for serial bytes over UART2 (GPIO18/19):

  • 0x01 → PLAY1 (0001.mp3)  
  • 0x02 → PLAY2 (0002.mp3)  
  • 0x03 → PLAY3 (0003.mp3)  
  • 0x04 → PLAY4 (0004.mp3)  
  • 0x05 → SLEEP → PLAY5 (0005.mp3) then deep‑sleep





## 🗣️ 6. Python Wake‑Word Listener:

Located in py_to_esp32/:\
• **mic_list.py** : list audio devices & indices\
• **mic_rms.py** : display RMS levels for mic gain\
• **test_serial.py** : verify ESP32 COM port (default: COM5)\
• **wakeword_vosk_to_esp32.py** : listen for keywords, send trigger byte





## 🗃️ 7. Directory Structure:

Speech-Recognition-with-ESP32-using-VOSK-Model/ \
├─ esp32_to_dfplayer/ \
│   └─ esp32_to_dfplayer.ino \
├─ py_to_esp32/ \
│   ├─ mic_list.py \
│   ├─ mic_rms.py \
│   ├─ test_serial.py \
│   ├─ wakeword_vosk_to_esp32.py \
│   └─ vosk-model-small-en-us-0.15/ \
└─ README.md (this file)




## 🚀 8. Step‑by‑Step Setup & Usage:

🗂️ Copy 0001.mp3...0005.mp3 to SD card; insert into DFPlayer 

🔌 Wire all hardware as described 

📲 Upload sketch: compile, upload, open Serial Monitor (115200), wait for [INFO] DFPlayer Initialized., then close

**💻 Install Python dependencies:**\
  • cd py_to_esp32 \
  • pip install vosk sounddevice pyserial


**🎧 Identify mic index:** \
  • python mic_list.py


**(Optional) Adjust and test mic levels:** \
  • python mic_rms.py


**🔎 Verify serial port access:** \
  • python test_serial.py


**🎙️ Start wake‑word listener:** \
  • python wakeword_vosk_to_esp32.py


Speak a trigger word **(“jarvis”, “hello”, “hi”, “play”, “hammer time”)** → ESP32 plays matched track





## ⚙️ 9. Configuration Options

In Python scripts:

MIC_INDEX = "your mic index" \
PORT      = "COM5"                # or correct ESP32 port \
MODEL_PATH= "vosk-model-small-en-us-0.15" 

In Arduino sketch, modify trigger bytes: 

#define TRIGGER_BYTE_PLAY1   0x01 \
#define TRIGGER_BYTE_PLAY2   0x02 \
#define TRIGGER_BYTE_PLAY3   0x03 \
#define TRIGGER_BYTE_PLAY4   0x04 \
#define TRIGGER_BYTE_SLEEP   0x05 





## ⚠️ 10. Troubleshooting

• **🔇 No Audio:** Check SD filenames (0001.mp3–0005.mp3); verify speaker polarity 

• **🔌 Serial Errors:** Ensure PORT matches Device Manager; close other COM-using apps 

• **🛑 Wake-Word Not Detected:** Use mic_rms.py to confirm mic input; stay in quiet environment or use a larger Vosk model

