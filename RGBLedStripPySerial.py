import serial
import numpy as np
import pyaudio
import wave
from struct import pack
from time import sleep
from os import system

"""Tracks"""
tracks = {
    1: ('Song 1', 'directory\song1.wav')
    }

def set_RGB_color(freq):
    CONV_HZ_TO_RGB = 7.28597268

    if freq <= 0: var = 0
    else: var = int(freq / CONV_HZ_TO_RGB)

    if var > 255: var = 255

    if freq <= 1333.333:
        red = 1
        green = 0
        blue = var
    elif freq > 1333.333 and freq <= 2666.666:
        red = var
        green = 0
        blue = 1
    elif freq > 2666.666 and freq <= 4000:
        red = 0
        green = var
        blue = 1
    elif freq > 4000 and freq <= 5333.333:
        red = 0
        green = 1
        blue = var
    elif freq > 5333.333 and freq <= 6666.666:
        red = var
        green = 1
        blue = 0
    else:
        red = 1
        green = var
        blue = 0

    ArduinoSerial.write(pack('>BBB', red, green, blue))

print("Choose a track:")
for i in tracks: print(str(i) + ")", tracks[i][0])

while True:
    choosen_track = int(input())
    if choosen_track in tracks:
        choosen_track = tracks[choosen_track][1]
        break
    else:
        print("This track doesn't exist!")
        sleep(2)
        system('cls')


"""Set serial comunication with Arduino board"""
ArduinoSerial = serial.Serial('COM4', 9600)
sleep(2)


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

while len(data) == CHUNK * swidth: #Do this forever
    stream.write(data)

    indata = np.array(wave.struct.unpack("%dh" % (len(data) / swidth), data)) * window

    fftData = abs(np.fft.rfft(indata)) ** 2

    which = fftData[1:].argmax() + 1

    if which != len(fftData) - 1:
        y0, y1, y2 = np.log(fftData[which - 1: which + 2])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)

        thefreq = (which + x1) * RATE / CHUNK
    else: thefreq = which * RATE / CHUNK

    print("The frequency is {0} Hz".format(thefreq))

    if not np.isnan(thefreq): set_RGB_color(freq = thefreq)

    data = wf.readframes(CHUNK)

ArduinoSerial.write(pack('>BBB', 0, 0, 0))
stream.close()
p.terminate()
