import pyaudio
import wave
import numpy as np
import pyfirmata
from os import system
from time import sleep

"""Tracks"""
tracks = {
    1: ('Song 1', 'directory/Song1.wav')
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

def brightness(freq, led = []):
    CONV_1_TO_RGB = 0.00390625
    CONV_HZ_TO_RGB = 7.28597268
    
    if freq <= 0:
        var = 0
    else:
        var = (freq / CONV_HZ_TO_RGB) / CONV_1_TO_RGB
        
    for i in led:
        i.write(var)


"""Variables for Arduino"""
board = pyfirmata.Arduino('COM4')

it = pyfirmata.util.Iterator(board)
it.start()

# Set digital pin 3 in PWM mode
led_pin1 = board.get_pin('d:3:p')


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
        brightness(freq = thefreq, led = [led_pin1])

    data = wf.readframes(CHUNK)


led_pin1.write(0)
    
stream.close()
p.terminate()
