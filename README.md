# G29_Uno
Use Logitech G29 (and similar) pedals as a standalone USB  controller using:  1) Arduino Uno as an analog reader  2) Python bridge script  3) vJoy virtual joystick device on Windows, bypassing the need for Logitech Hub software, or using steering base or any proprietary wiring. 

Other g29 serial to microcontroller boards have worked, but I only had an uno to make this with com and serial. 


Hardware Required
  Logitech G29 (or G25/G27/G920-style) 3-pedal set
  Arduino Uno (original or compatible)
  Female DB9 (DE-9) breakout / adapter
  USB cable for the Uno
  A few jumper wires

Steps. 

1. Wiring

Looking into the female DB9 connector (holes facing you, screw posts left/right):
(looking carefully on the front will reveal small numbers by their respective pinholes) 

Top row (left → right): 1 2 3 4 5
Bottom row (left → right): 6 7 8 9

Typical pinout (G29 style):
Serial:G29 :      Uno 
  1    Ground     GND
  2    Throttle   A2
  3    Brake      A1
  4    Clutch     A0 
  6    power      5V
  9    power      5V 

You can choose ot use a breakout conenctor or solder wires directly onto the female DB9 serial connector. 

So on your DB9 breakout:
Pin 1 → Uno GND
Pin 2 → Uno A2
Pin 3 → Uno A1
Pin 4 → Uno A0
Pin 6 → uno 5v 
Pin 9 → Uno 5V

2. Arduino Setup 

Install Arduino IDE and drivers, plug your board into your computer
Open G29_Uno_Pedals.ino in the IDE.

Make sure:
  Tools → Board → Arduino Uno
  Tools → Port → the COM port for your Uno

Click compile, and upload sketch 
(Optional) Test in Tools → Serial Plotter @ 115200: you should see three lines moving when you press the pedals.

3. Windows and vJoy setup
   
Download and install vJoy
https://www.vjoy.org/download-for-windows
(make sure Device 1 is enabled with at least 3 axes [xyz]. Apply/Save settings.) 

You will need to install these repos in your directory: 
pip install pyserial pyvjoy

g29_pedals_vjoy.py opens the Uno’s serial port, parses the pedal values, and writes them into vJoy axes.

You will need to edit the com port line in line 4 of the python script to match where your Uno is plugged in. 



