import serial
import pyvjoy

# === CONFIG ===
COM_PORT = "COM4"   # change this to your Uno's COM port
BAUD     = 115200

# vJoy axis range is usually 1..32768
VJOY_MIN = 1
VJOY_MAX = 32768

def map_axis(value, in_min=0, in_max=1023,
             out_min=VJOY_MIN, out_max=VJOY_MAX):
    # Clamp first
    value = max(in_min, min(in_max, value))
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def parse_line(line):
    """
    Expect lines like: C:512 B:800 T:100
    Returns dict {'C': 512, 'B': 800, 'T': 100}
    """
    result = {}
    parts = line.strip().split()
    for part in parts:
        if ":" in part:
            key, val = part.split(":", 1)
            if val.isdigit():
                result[key] = int(val)
    return result

def main():
    print("Opening serial on", COM_PORT)
    ser = serial.Serial(COM_PORT, BAUD, timeout=1)

    j = pyvjoy.VJoyDevice(1)  # vJoy Device ID 1
    print("Connected to vJoy device 1")

    while True:
        line = ser.readline().decode(errors="ignore")
        if not line:
            continue

        data = parse_line(line)
        if not data:
            continue

        clutch   = data.get("C", 0)
        brake    = data.get("B", 0)
        throttle = data.get("T", 0)

        # Map Arduino 0–1023 to vJoy axis range
        clutch_v   = map_axis(clutch)
        brake_v    = map_axis(brake)
        throttle_v = map_axis(throttle)

        # Assign them to axes (choose whatever mapping you want)
        j.data.wAxisX = throttle_v   # X = throttle
        j.data.wAxisY = brake_v      # Y = brake
        j.data.wAxisZ = clutch_v     # Z = clutch

        j.update()

if __name__ == "__main__":
    main()
