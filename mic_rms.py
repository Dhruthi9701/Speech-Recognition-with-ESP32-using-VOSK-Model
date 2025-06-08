# mic_rms.py

import sounddevice as sd
import numpy as np

DEVICE = 1  # replace with your mic index

def callback(indata, frames, time_info, status):
    rms = np.sqrt(np.mean(indata.astype(np.float32)**2))
    print(f"RMS = {rms:.2f}")

try:
    with sd.InputStream(
        samplerate=16000,
        channels=1,
        dtype='int16',
        callback=callback,
        device=DEVICE
    ):
        print("Speaking into mic—watch RMS values. (Ctrl+C to stop.)")
        sd.sleep(1000000)
except Exception as e:
    print("ERROR:", e)
