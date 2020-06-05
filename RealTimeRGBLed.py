import pyaudio
import wave
import numpy as np
import pyfirmata
from time import sleep
from os import system

def set_RGB_color(freq, red = 2, green = 5, blue = 6):
    CONV_1_TO_RGB = 0.00390625
    
    if freq < 40:
        red.write(1)
        green.write(0)
        blue.write(0)
    elif freq >= 40 and freq <= 77:
        var = ((freq - 40) * (255 / 37)) * CONV_1_TO_RGB
        red.write(1)
        green.write(0)
        blue.write(var)
    elif freq > 77 and freq <= 205:
        var = (255 - ((freq - 78) * 2)) * CONV_1_TO_RGB
        red.write(var)
        green.write(0)
        blue.write(1)
    elif freq >= 206 and freq <= 238:
        var = ((freq - 206) * (255 / 32)) * CONV_1_TO_RGB
        red.write(0)
        green.write(var)
        blue.write(1)
    elif freq >= 239 and freq <= 250:
        var = ((freq - 239) * (255 / 11)) * CONV_1_TO_RGB
        red.write(var)
        green.write(1)
        blue.write(1)
    elif freq >= 251 and freq <= 270:
        red.write(1)
        green.write(1)
        blue.write(1)
    elif freq >= 271 and freq <= 398:
        var = (255 - ((freq - 271) * 2)) * CONV_1_TO_RGB
        red.write(var)
        green.write(1)
        blue.write(var)
    elif freq >= 398 and freq <= 653:
        red.write(0)
        green.write((255 - (freq - 398)) * CONV_1_TO_RGB)
        blue.write((freq - 398) * CONV_1_TO_RGB)
    else:
        red.write(1)
        green.write(0)
        blue.write(0)


"""Variables for Arduino"""
board = pyfirmata.Arduino('COM4')

it = pyfirmata.util.Iterator(board)
it.start()

# Set digital pin in PWM mode for RGB led
redLedPin = board.get_pin('d:3:p')
greenLedPin = board.get_pin('d:5:p')
blueLedPin = board.get_pin('d:6:p')


"""Variables for the frequency detection"""
CHUNK = 2048
WIDTH = 2
CHANNELS = 1
RATE = 44100

window = np.blackman(CHUNK)

p = pyaudio.PyAudio()
stream = p.open(
    format = p.get_format_from_width(WIDTH),
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = CHUNK
)


print("* Start recording")

while True:
    data = stream.read(CHUNK)
    stream.write(data)

    indata = np.array(wave.struct.unpack("%dh" % (len(data) / WIDTH), data)) * window

    fftData = abs(np.fft.rfft(indata)) ** 2

    which = fftData[1:].argmax() + 1

    if which != len(fftData) - 1:
        y0, y1, y2 = np.log(fftData[which - 1: which + 2])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)

        thefreq = (which + x1) * RATE / CHUNK
    else:
        thefreq = which * RATE / CHUNK

    print("The frequency is {0} Hz".format(thefreq))

    if not np.isnan(thefreq):
        set_RGB_color(freq = thefreq, red = redLedPin, green = greenLedPin, blue = blueLedPin)

redLedPin.write(0)
greenLedPin.write(0)
blueLedPin.write(0)

stream.stop_stream()
stream.close()
p.terminate()