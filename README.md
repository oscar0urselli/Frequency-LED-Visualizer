# ledSync
Sync led with music, using Arduino and Python.

Things needed for every program:
- Arduino UNO board (or similiar)
- A USB cable to connect Arduino with a computer
- Python 3.6 or newer installed
- A computer, possibly not an IBM 701 :)

Install [PyFirmata](https://pypi.org/project/pyFirmata/), [PyAudio](https://pypi.org/project/PyAudio/) and [NumPy](https://pypi.org/project/numpy/) with pip if not already installed.

## How to upload StandardFirmata on Arduino.
In order to upload StandardFirmata you need to install the [Arduino IDE](https://www.arduino.cc/en/main/software) first. Then inside the editor go: _File -> Examples -> Firmata -> StandardFirmata_. And once you selected it, click the button to load on the Arduino board.

NOTE:
> **If you don't find Firmata, means you have an old version of the Arduino IDE and you should up date it.**


## Setup the programs
- ### RGBLed.py
  - Connect one or more RGB leds to the [PWN](https://www.arduino.cc/en/tutorial/PWM) ports of Arduino (one port for one color), then in _RGBLed.py_:
    - at row **71** write inside ```path = ""``` the full path of the folder containing the .wav files;
    - instead at the row **76**, you'll find ```board = pyfirmata.Arduino('COM4')``` change the _COM4_ to somthing else if you use a different serial port;
    - finally at **83**, fill the three lists passed as parameters of the function with the PWM pins you want to use.
  - Don't forget to upload StandardFirmata on the Arduino board.


- ### SingleLed.py:
  - Same thing with _RGBLed.py_, but with a normal led with just a color.


- ### RealTimeRGBLed.py
  - This is very similiar to the two before, but this time you don't need to specify the path of a folder and you have to attach a microphone to your computer.


- ### RGBLedStripPySerial.py and ControlRGBLedStrip.ino
  - With these two programs you can control a RGB led strip while you are playing music like with _RGBLed.py_. But instead of having loaded StandardFirmata in your Arduino board, **you need to use ControlRGBLedStrip.ino**.
Another time, inside _RGBLedStripPySerial.py_ you'll need to do this steps:
    - at row **79** write inside ```path = ""``` the full path of the folder containing the .wav files;
    - at **83** modify ```n_leds = 150``` with the number of leds that your strip has;
    - in ```board = pyfirmata.Arduino('COM4', 9600)``` change **ONLY** _COM4_ if necessary.
  - It's important also to change something inside _ControlRGBLedStrip.ino_:
    - change ```#define LED_PIN 6``` if you want to use another pin (remember to attach the strip to the pin wrote here);
    - ```#define NUM_LEDS 150``` change only with the number written inside _RGBLedStripPySerial.py_ at row **83**.
