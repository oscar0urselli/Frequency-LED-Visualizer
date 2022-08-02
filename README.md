# Frequency LED Visualizer
Visualize the frequency of the music with a led using: Arduino, Python and [FFT (Fast Fourier transform)](https://en.wikipedia.org/wiki/Fast_Fourier_transform).

## Descriptions
- ### RGBLed.py
  - Create a realtime visualizer of the frequency of the music reproduced on the computer using a RGB LED.
- ### SingleLed.py
  - Same effect of _RGBLed.py_ but with a normal LED with a single color.
- ### RealTimeRGBLed.py
  - Visualize with a RGB LED, the frequency of a sound captured by a microphone attached to the computer.
- ### RGBLedStripPySerial.py
  - As _RGBLed.py_ reproduce a .wav file and calculate the frequency, then convert the value to RGB and send it to Arduino, where _ControlRGBLedStrip.ino_ will control the strip.

## Things needed for every program:
- Arduino UNO board (or similiar)
- A USB cable to connect Arduino with a computer
- Python 3.6 or newer installed
- A computer, possibly not an IBM 701 :)

Install [PyFirmata](https://pypi.org/project/pyFirmata/), [PyAudio](https://pypi.org/project/PyAudio/), [PySerial](https://pypi.org/project/pyserial/) and [NumPy](https://pypi.org/project/numpy/) with pip if not already installed.

## How to upload StandardFirmata on Arduino.
In order to upload StandardFirmata you need to install the [Arduino IDE](https://www.arduino.cc/en/main/software) first. Then inside the editor go: _File -> Examples -> Firmata -> StandardFirmata_. And once you selected it, click the button to load on the Arduino board.

**NOTE**:
- **If you don't find Firmata, this means you have an old version of the Arduino IDE and you should update it.**


## Setup the programs
- ### RGBLed.py
  - Connect one or more RGB leds to the [PWM](https://www.arduino.cc/en/tutorial/PWM) ports of Arduino (one port for one color), then in _RGBLed.py_:
    - at row **71** write inside ```path = ""``` the full path of the folder containing the .wav files;
    - instead at the row **76**, you'll find ```board = pyfirmata.Arduino('COM4')``` change the _COM4_ to somthing else if you use a different serial port;
    - finally at **83**, fill the three lists passed as parameters of the function with the PWM pins you want to use.
  - Don't forget to upload StandardFirmata on the Arduino board.


- ### SingleLed.py
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

**NOTE**:
  - **In order to use _ControlRGBLedStrip.ino_ you need to install the [FastLED](https://github.com/FastLED/FastLED) library**
    
## Useful links
For the creation of these programs I followed a lot of articles, wikis, videos and forums.
This is the list of the sources that helped me:
- [Python frequency detection](https://stackoverflow.com/a/2649540/13340183)
- [How to send an int from Python to an Arduino in order to use it as an argument for the neopixel function setPixelcolor()?](https://stackoverflow.com/a/56321187/13340183)
- [HOW TO USE WS2812B NEOPIXELS WITH FASTLED ON ARDUINO](https://youtu.be/YgII4UYW5hU) (video)
- [LED-Music-Visualizer](https://github.com/DevonCrawford/LED-Music-Visualizer)
- [Arduino With Python: How to Get Started](https://realpython.com/arduino-python/)
