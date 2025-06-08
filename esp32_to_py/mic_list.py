#Enumerates all available audio input devices and prints their index numbers.
import sounddevice as sd

print("Available audio input devices:\n")
for idx, dev in enumerate(sd.query_devices()):
    if dev['max_input_channels'] > 0:
        print(f"Index {idx}: {dev['name']} (channels = {dev['max_input_channels']})")
