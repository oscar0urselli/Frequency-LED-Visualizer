import pyaudio
import wave
import numpy as np
import pyfirmata

def set_RGB_color(freq, red = [], green = [], blue = []):
    CONV_1_TO_RGB = 0.00390625
    CONV_HZ_TO_RGB = 7.28597268

    if freq <= 0:
        var = 0
    else:
        var = (freq / CONV_HZ_TO_RGB) * CONV_1_TO_RGB

    if freq <= 1333.333:
        for i in red: i.write(1)
        for i in green: i.write(0)
        for i in blue: i.write(var)
    elif freq > 1333.333 and freq <= 2666.666:
        for i in red: i.write(var)
        for i in green: i.write(0)
        for i in blue: i.write(1)
    elif freq > 2666.666 and freq <= 4000:
        for i in red: i.write(0)
        for i in green: i.write(var)
        for i in blue: i.write(1)
    elif freq > 4000 and freq <= 5333.333:
        for i in red: i.write(0)
        for i in green: i.write(1)
        for i in blue: i.write(var)
    elif freq > 5333.333 and freq <= 6666.666:
        for i in red: i.write(var)
        for i in green: i.write(1)
        for i in blue: i.write(0)
    else:
        for i in red: i.write(1)
        for i in green: i.write(var)
        for i in blue: i.write(0)


"""Variables for Arduino"""
board = pyfirmata.Arduino('COM4')

it = pyfirmata.util.Iterator(board)
it.start()

# Set digital pin in PWM mode for RGB led
redLedPin1 = board.get_pin('d:3:p')
greenLedPin1 = board.get_pin('d:5:p')
blueLedPin1 = board.get_pin('d:6:p')

redLedPin2 = board.get_pin('d:9:p')
greenLedPin2 = board.get_pin('d:10:p')
blueLedPin2 = board.get_pin('d:11:p')


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
        set_RGB_color(freq = thefreq, red = [redLedPin1, redLedPin2], green = [greenLedPin1, greenLedPin2], blue = [blueLedPin1, blueLedPin2])

        
redLedPin1.write(0)
greenLedPin1.write(0)
blueLedPin1.write(0)

redLedPin2.write(0)
greenLedPin2.write(0)
blueLedPin2.write(0)

stream.close()
p.terminate()
