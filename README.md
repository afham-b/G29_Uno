# G29_Uno – Logitech G29 Pedals on Arduino Uno via vJoy

Use Logitech **G29** (and similar) pedals as a **standalone USB controller** using:

1. An **Arduino Uno** as an analog reader  
2. A **Python** bridge script  
3. A **vJoy** virtual joystick device on Windows  

This bypasses Logitech G Hub, the original steering base, and any proprietary wiring. Other G29–to–microcontroller boards exist, but this project focuses on doing it with a simple **Uno** over **COM/serial**.

---

## Hardware Required

- Logitech **G29** (or G25 / G27 / G920-style) 3-pedal set  
- **Arduino Uno** (original or compatible)  
- **Female DB9 (DE-9)** breakout / adapter  
- USB cable for the Uno  
- A few jumper wires  

---
Steps
1) Wiring
2) Arduino Setup
3) Windows and vJoy
4) Calibration and Tweaks
5) How to Run
6) Troubleshooting
---


## 1. Wiring

Looking into the **female DB9 connector** (holes facing you, screw posts left/right):

> If you look carefully at the plastic around the pins, you’ll see small numbers by each pinhole.

- Top row (left → right): **1 2 3 4 5**  
- Bottom row (left → right): **6 7 8 9**

Typical G29 pedal pinout used here:

| DB9 Pin | Function | Uno Pin |
|---------|----------|---------|
| 1       | Ground   | GND     |
| 2       | Throttle | A2      |
| 3       | Brake    | A1      |
| 4       | Clutch   | A0      |
| 6       | +5V      | 5V      |
| 9       | +5V      | 5V      |

You can use a DB9 breakout or solder wires directly onto a female DB9 connector.

**DB9 → Uno summary:**

- Pin **1 →** Uno **GND**  
- Pin **2 →** Uno **A2** (Throttle)  
- Pin **3 →** Uno **A1** (Brake)  
- Pin **4 →** Uno **A0** (Clutch)  
- Pin **6 →** Uno **5V**  
- Pin **9 →** Uno **5V**  

> You technically only need one 5V pin, but tying both 6 and 9 to 5V is common.

---

## 2. Arduino Setup

1. Install the **Arduino IDE** and any necessary drivers.  
2. Plug your **Arduino Uno** into your computer.  
3. Open `G29_Uno_Pedals.ino` in the IDE.  

In the Arduino IDE:

- Go to **Tools → Board → Arduino Uno**  
- Go to **Tools → Port →** select the COM port for your Uno  

Then:

- Click **Verify/Compile**, then **Upload** the sketch.  

> Optional: open **Tools → Serial Plotter** at **115200 baud** and press the pedals. You should see three lines moving if everything is wired correctly.

---

## 3. Windows & vJoy Setup

1. Download and install **vJoy** for Windows:  
   - <https://www.vjoy.org/download-for-windows>
2. Open the vJoy configuration tool and:
   - Ensure **Device 1** is **enabled**  
   - Enable at least **3 axes** (X, Y, Z)  
   - Click **Apply/Save**  

### Python Dependencies

From your project directory (or globally), install the required Python packages:

```bash
pip install pyserial pyvjoy
```

`g29_pedals_vjoy.py` opens the Uno’s serial port, parses the pedal values, and writes them into vJoy axes.

**You must edit the COM port line in line 4** of the Python script to match where your Uno is plugged in.

- Find your Uno's COM port in the Arduino IDE (Tools → Port). Update the COM_PORT variable in `g29_pedals_vjoy.py`

⚠️ Important: Make sure the Arduino IDE’s Serial Monitor/Plotter is closed before running the script—only one program can open the COM port at a time.


---

## 4. Calibration & Tweaks

**Calibration:**
Min and Max values for each pedal can be manually recorded using the Arduino IDE by compiling -> uploading the `G29_Uno_Pedals.ino` Sketch and opening Tool->Serial monitor and pressing the pedals 

```bash
C: X  B: x  T: X 
```
> Your output for clutch (C), brake (B), and throttle(T) will print out here and you can record the rest values when the pedals are not pressed and then the values at their maximum depression positions. It is normal if these numerical values are inverted.

Modify the `g29_pedals_vjoy.py` script, between lines 17-23 with your values. These are example output from my G29 (note how my values are inverted) 

```bash
THROTTLE_MIN_RAW = 950
THROTTLE_MAX_RAW = 65 
BRAKE_MIN_RAW    = 970 
BRAKE_MAX_RAW    = 300
CLUTCH_MIN_RAW   = 930 
CLUTCH_MAX_RAW   = 60 
```

Calibration will ensure that the program works withing the range of your specific G29 and adjusts for ADC of your unit. 


**Axis mapping:**
Change which vJoy axis each pedal uses by editing:

```bash
j.data.wAxisX = throttle_v
j.data.wAxisY = brake_v
j.data.wAxisZ = clutch_v
```

**Inversion:**

The map_axis function inside of `g29_pedals_vjoy.py` should detect and invert for pedals that are inverted, but in the case this fails: 
If pedals feel reversed (full press reads as low value), uncomment the inversion lines in the Arduino sketch:
Using the Arduino IDE to modify `G29_Uno_Pedals.ino` , add in these lines: 

```bash
clutchFilt   = 1023 - clutchFilt;
brakeFilt    = 1023 - brakeFilt;
throttleFilt = 1023 - throttleFilt;
```
>Similair software like assetto corsa has invert options in the control setting you can turn on to mitigate this issue. 

**Dead zones & curves:**
You can implement dead zones or non-linear curves either in:
The Arduino sketch (edit raw values), or
The Python script (before mapping to vJoy).

Within `g29_pedals_vjoy.py` there is deadzone function that zeros all input below 2%, 
```bash
def apply_deadzone(v, threshold=0.02):
```
>You can increase or decrese this parameter for a differnt or **NO** deadzone. 


## 5. How to Run

- Plug in the Uno with the G29 pedals connected.
- Confirm the **COMx** port in Arduino IDE (Tools → Port), then update COM_PORT in `g29_pedals_vjoy.py`
- Close the Arduino IDE (or at least close Serial Monitor/Plotter).

From a terminal in the project folder:

```bash
python g29_pedals_vjoy.py
```

You should see:
```bash
Opening serial on COMx
Connected to vJoy device 1
```

### Open Windows Game Controllers (Win + R → joy.cpl) and select vJoy Device:
    Press each pedal and verify the corresponding axes move.

---
---

## 6. Troubleshooting

Some possible and common errors: 

Python Error 
```bash
 could not open port ‘COMx’: PermissionError(13)
```
> Another program is using the COM port (likely Arduino Serial Monitor/Plotter). Close it and try again.

No movement in Game Controllers
>Confirm the Python script is running without errors.
>Make sure vJoy Device 1 is enabled and has X/Y/Z axes.
>Check wiring on DB9 pins and Uno A0–A2/5V/GND.

Serial Monitor shows nothing
>Confirm upload succeeded and Serial.begin(115200) matches the baud in Serial Monitor.
>Make sure the correct COM port is selected.


---

## License
      Use, modify, and share as you like.
      If you fork this or improve the mapping/calibration, feel free to open PRs or notes so others can benefit.


