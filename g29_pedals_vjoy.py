import serial
import pyvjoy

# === CONFIG ===
COM_PORT = "COM4"   # change this to your Uno's COM port
BAUD     = 115200

# vJoy axis range is usually 1..32768
VJOY_MIN = 1
VJOY_MAX = 32768


# === RAW calibration values (replace these with your measured values) ===
# you can measure these using the arduino ide and running g29_pedals.ino (compile-> upload) 
# and opening Tools -> serial monitor

THROTTLE_MIN_RAW = 950
THROTTLE_MAX_RAW = 65 
BRAKE_MIN_RAW    = 970 
BRAKE_MAX_RAW    = 300
CLUTCH_MIN_RAW   = 930 
CLUTCH_MAX_RAW   = 60 


def map_axis(value, in_min, in_max,
             out_min=VJOY_MIN, out_max=VJOY_MAX):
    """
    Maps an input value from [in_min, in_max] to [out_min, out_max].

    Works for both:
      - normal ranges:  in_min < in_max
      - reversed ranges: in_min > in_max  (like your pedals: high at rest, low when pressed)
    """

    # Normal case: increasing range
    if in_min < in_max:
        # Clamp
        if value < in_min:
            value = in_min
        if value > in_max:
            value = in_max

        return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    # Reversed range: in_min > in_max
    # Example: rest = 950, pressed = 65
    else:
        hi = in_min  # rest position (higher value)
        lo = in_max  # pressed position (lower value)

        # Clamp to [lo, hi]
        if value > hi:
            value = hi
        if value < lo:
            value = lo

        # Normalize so:
        #   value = hi   -> 0.0
        #   value = lo   -> 1.0
        span = hi - lo
        if span == 0:
            norm = 0.0
        else:
            norm = (hi - value) / span

        return int(norm * (out_max - out_min) + out_min)

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

def apply_deadzone(v, threshold=0.02):
    span = VJOY_MAX - VJOY_MIN
    if v - VJOY_MIN < threshold * span:
        return VJOY_MIN
    return v

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
        # clutch_v   = map_axis(clutch)
        # brake_v    = map_axis(brake)
        # throttle_v = map_axis(throttle)

       # Map using your measured raw ranges
        throttle_v = map_axis(throttle, THROTTLE_MIN_RAW, THROTTLE_MAX_RAW)
        brake_v    = map_axis(brake,    BRAKE_MIN_RAW,    BRAKE_MAX_RAW)
        clutch_v   = map_axis(clutch,   CLUTCH_MIN_RAW,   CLUTCH_MAX_RAW)

        #include a deadzone of 2% 
        throttle_v = apply_deadzone(throttle_v)
        brake_v    = apply_deadzone(brake_v)
        clutch_v   = apply_deadzone(clutch_v)

        # Assign them to axes (choose whatever mapping you want)
        j.data.wAxisX = throttle_v   # X = throttle
        j.data.wAxisY = brake_v      # Y = brake
        j.data.wAxisZ = clutch_v     # Z = clutch

        j.update()

if __name__ == "__main__":
    main()




