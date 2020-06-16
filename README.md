# ledSync
Sync led with music, using Arduino and Python.

There are some scripts. This is the list that explain all:
1) RGBLed.py
Using the firmware Firmata and the module PyFirmata, one or more RGB leds attached to the PWM port of Arduino go in sync with a .wav file.

Things needed:
- Arduino UNO board (or similiar)
- RGB led (one or more)
- 220 ohm resistors (three for each RGB led)
- A USB cable to connect Arduino with a computer
- Python 3.6 or newer installed

Install PyFirmata, PyAudio and NumPy with pip.

Upload StandardFirmata on your Arduino board from Arduino IDE.

In the Python script, write in the dictonary under """Tracks""" the name of the song and its directory (remember, the song must be a .wav).

Connect one or more RGB led to the Arduino board and run the Python script.


2) SingleLed.py
Same thing with "RGBLed.py", but with a single color led.


3) RealTimeRGBLed.py
Like the preovius two, with this a RGB led goes in sync with music or some sound, but in real time with a microphone connected to the computer.


4) RGBLedStripPySerial.py and ControlRGBLesStrip.ino
With these two programs you can control a RGB led strip while you are playing music like in the "RGBLed.py" case.
