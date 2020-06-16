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
    if freq < 0: freq = 0
    else: freq = int(freq)

    if freq < 40:
        red = 255
        green = 0
        blue = 0
    elif freq >= 40 and freq <= 77:
        b = int((freq - 40) * (255 / 37))
        red = 255
        green = 0
        blue = b
    elif freq > 77 and freq <= 205:
        r = int(255 - ((freq - 78) * 2))
        red = r
        green = 0
        blue = 255
    elif freq >= 206 and freq <= 238:
        g = int((freq - 206) * (255 / 32))
        red = 0
        green = g
        blue = 255
    elif freq <= 239 and freq <= 250:
        r = int((freq - 239) * (255 / 11))
        red = r
        green = 255
        blue = 255
    elif freq >= 251 and freq <= 270:
        red = 255
        green = 255
        blue = 255
    elif freq >= 271 and freq <= 398:
        rb = int(255 - ((freq - 271) * 2))
        red = rb
        green = 255
        blue = rb
    elif freq >= 398 and freq <= 653:
        red = 0
        green = int(255 - (freq - 398))
        blue = int(freq - 398)
    else:
        red = 255
        green = 0
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

sleep(0.5)
for i in range(150):
    ArduinoSerial.write(pack('>BBB', 0, 0, 0))
    sleep(0.01)
stream.close()
p.terminate()
