#Scan for and verify availability of the ESP32’s COM port (default: COM5).
import serial
try:
    ser = serial.Serial("COM5", 115200, timeout=1)
    print("✔️  Opened COM5 successfully.")
    ser.close()
except Exception as e:
    print("❌  ERROR opening COM5:", e)
