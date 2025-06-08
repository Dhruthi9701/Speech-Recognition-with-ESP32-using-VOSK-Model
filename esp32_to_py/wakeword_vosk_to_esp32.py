# Listens via Vosk ASR on the laptop mic for:
#   • “jarvis”      → PLAY1
#   • “hello”       → PLAY2
#   • “hi”          → PLAY3
#   • “play”        → PLAY4
#   • “hammer time” → SLEEP (play 0005.mp3 then exit)
#
# Dependencies:
#   pip install vosk sounddevice pyserial


import os
import sys
import queue
import json
import time
import sounddevice as sd
import vosk
import serial

# ——— CONFIGURATION ———

# 1) Vosk model folder name 
MODEL_DIR_NAME = "vosk-model-small-en-us-0.15"

# 2) Serial port where your ESP32 is listening ("COM5" on Windows)
SERIAL_PORT = "COM5"
SERIAL_BAUD = 115200

# 3) Debounce interval (seconds) to avoid multiple triggers from one utterance
DEBOUNCE_SECONDS = 1.0

# 4) Microphone device index (use mic_list.py to find the correct index)
MIC_DEVICE_INDEX = 1  # ← replace this with your actual mic index

# 5) List of (phrase, command) in priority order
PHRASES = [
    ("jarvis",      "PLAY1"),
    ("hello",       "PLAY2"),
    ("hi",          "PLAY3"),
    ("play",        "PLAY4"),
    ("hammer time", "SLEEP")
]
# ————————————————————

def main():
    # 1) Verify Vosk model folder exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, MODEL_DIR_NAME)
    if not os.path.isdir(model_path):
        print(f"ERROR: Vosk model folder not found at:\n  {model_path}")
        sys.exit(1)

    print(f"[INFO] Loading Vosk model from:\n  {model_path}")
    try:
        model = vosk.Model(model_path)
    except Exception as e:
        print(f"ERROR: Failed to load Vosk model:\n  {e}")
        sys.exit(1)

    recognizer = vosk.KaldiRecognizer(model, 16000)

    # 2) Open Serial port to ESP32
    try:
        ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=0.1)
        print(f"[INFO] Opened serial {SERIAL_PORT} @ {SERIAL_BAUD} baud.")
        time.sleep(2)  # give ESP32 a moment to reset if needed
    except Exception as e:
        print(f"ERROR: Cannot open serial port {SERIAL_PORT}:\n  {e}")
        sys.exit(1)

    # 3) Prepare an audio-callback queue
    q = queue.Queue()
    def audio_callback(indata, frames, time_info, status):
        if status:
            print(f"[WARN] Audio status: {status}")
        q.put(bytes(indata))

    # 4) Start streaming from the specified mic device
    try:
        stream = sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,    # roughly 0.5 s of audio at 16 kHz
            dtype="int16",
            channels=1,
            callback=audio_callback,
            device=MIC_DEVICE_INDEX
        )
        stream.start()
    except Exception as e:
        print(f"ERROR: Could not open microphone stream:\n  {e}")
        ser.close()
        sys.exit(1)

    print("\n[INFO] Listening for “jarvis”, “hello”, “hi”, “play”, or “hammer time”… (Ctrl+C to quit)\n")
    last_trigger_time = 0.0

    try:
        while True:
            audio_bytes = q.get()
            if recognizer.AcceptWaveform(audio_bytes):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower().strip()

                # DEBUG: print recognized text (uncomment if you need to troubleshoot)
                # print(f"[DEBUG] Recognized: “{text}”")

                # Check each phrase in priority order
                for phrase, cmd in PHRASES:
                    if phrase in text:
                        now = time.time()
                        if now - last_trigger_time > DEBOUNCE_SECONDS:
                            print(f"[{time.strftime('%H:%M:%S')}] Detected “{phrase}” → sending {cmd}")
                            try:
                                ser.write(cmd.encode("ascii") + b"\n")
                            except Exception as e:
                                print(f"ERROR: Failed to write to serial:\n  {e}")

                            last_trigger_time = now

                            # If “hammer time” → exit Python immediately
                            if phrase == "hammer time":
                                print("[INFO] “hammer time” command issued—exiting Python script.")
                                raise KeyboardInterrupt
                        break
            # We ignore partial results for simplicity
    except KeyboardInterrupt:
        print("\n[INFO] Exiting on hammer time command or user interrupt.")
    finally:
        stream.stop()
        stream.close()
        ser.close()

if __name__ == "__main__":
    main()
