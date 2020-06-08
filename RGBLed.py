import pyaudio
import wave
import numpy as np
import pyfirmata

"""Tracks"""
tracks = {
    1: ('Song 1', 'directory/song1.wav')
    }

print("Choose a track:")
for i in tracks:
    print(str(i) + ")", tracks[i][0])

while True:
    choosen_track = int(input())
    if choosen_track in tracks:
        choosen_track = tracks[choosen_track][1]
        break
    else:
        print("This track doesn't exist!")
        sleep(2)
        system('cls')


def set_RGB_color(freq, red = [], green = [], blue = []):
    CONV_1_TO_RGB = 0.00390625
    CONV_HZ_TO_RGB = 7.28597268

    if freq <= 1333.333:
        for i in red: i.write(1)
        for i in green: i.write(0)
        for i in blue: i.write((freq / CONV_HZ_TO_RGB) * CONV_1_TO_RGB)
    elif freq > 1333.333 and freq <= 2666.666:
        for i in red: i.write((freq / CONV_HZ_TO_RGB) * CONV_1_TO_RGB)
        for i in green: i.write(0)
        for i in blue: i.write(1)
    elif freq > 2666.666 and freq <= 4000:
        for i in red: i.write(0)
        for i in green: i.write((freq / CONV_HZ_TO_RGB) * CONV_1_TO_RGB)
        for i in blue: i.write(1)
    elif freq > 4000 and freq <= 5333.333:
        for i in red: i.write(0)
        for i in green: i.write(1)
        for i in blue: i.write((freq / CONV_HZ_TO_RGB) * CONV_1_TO_RGB)
    elif freq > 5333.333 and freq <= 6666.666:
        for i in red: i.write((freq / CONV_HZ_TO_RGB) * CONV_1_TO_RGB)
        for i in green: i.write(1)
        for i in blue: i.write(0)
    else:
        for i in red: i.write(1)
        for i in green: i.write((freq / CONV_HZ_TO_RGB) * CONV_1_TO_RGB)
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

wf = wave.open(choosen_track, 'rb')

swidth = wf.getsampwidth()
RATE = wf.getframerate()

window = np.blackman(CHUNK)

p = pyaudio.PyAudio()
stream = p.open(
    format = p.get_format_from_width(wf.getsampwidth()),
    channels = wf.getnchannels(),
    rate = RATE,
    output = True
)

data = wf.readframes(CHUNK)

while len(data) == CHUNK * swidth:
    stream.write(data)

    indata = np.array(wave.struct.unpack("%dh" % (len(data) / swidth), data)) * window

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

    data = wf.readframes(CHUNK)


redLedPin1.write(0)
greenLedPin1.write(0)
blueLedPin1.write(0)

redLedPin2.write(0)
greenLedPin2.write(0)
blueLedPin2.write(0)

stream.close()
p.terminate()
