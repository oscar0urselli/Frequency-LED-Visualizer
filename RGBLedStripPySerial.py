import numpy as np
import serial
from struct import pack
from time import sleep
import os
import wave

import pyaudio

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

def play(directory):
    # List every .wav file inside the folder
    audio_files = [f for f in os.listdir(directory) if f.endswith(".wav")]

    print("Choose a track:")
    for i in audio_files:
        print(i + ")", directory + "/" + i)

    while True:
        choosen_track = int(input())
        if choosen_track < len(audio_files):
            choosen_track = directory + "/" + audio_files[choosen_track]
            return choosen_track
        else:
            print("This track doesn't exist!")
            sleep(2)
            os.system('cls')


"""Folder path"""
# The full path of the folder containing the .wav files
path = "" 

"""Strip length"""
# Number of leds in the strip
n_leds = 150

"""Set serial comunication with Arduino board"""
# Serial port used for the comunication with Arduino.
# Change if you use a different one
ArduinoSerial = serial.Serial('COM3', 9600)
sleep(2)

"""Variables for the frequency detection"""
CHUNK = 2048

while True:
    # Open the .wav file
    wf = wave.open(play(path), 'rb')

    swidth = wf.getsampwidth()
    RATE = wf.getframerate()

    # Use the Blackman window
    window = np.blackman(CHUNK)

    p = pyaudio.PyAudio()
    stream = p.open(
        format = p.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = RATE,
        output = True
    )

    data = wf.readframes(CHUNK)

    # Find the frequency of each chunk
    while len(data) == CHUNK * swidth:
        # Write data out to the audio stream
        stream.write(data)

        # Unpack the data and multiplicate it by the Hamming window
        indata = np.array(wave.struct.unpack("%dh" % (len(data) / swidth), data)) * window

        # Square each value of the fft
        fftData = abs(np.fft.rfft(indata)) ** 2

        # Find the maximum value
        which = fftData[1:].argmax() + 1

        # Use the quadratic interpolation around the max
        if which != len(fftData) - 1:
            y0, y1, y2 = np.log(fftData[which - 1: which + 2])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)

            thefreq = (which + x1) * RATE / CHUNK
        else:
            thefreq = which * RATE / CHUNK

        print("The frequency is {0} Hz".format(thefreq))

        # Check if the frequency is not detected
        if not np.isnan(thefreq):
            set_RGB_color(freq = thefreq)

        # Read more data
        data = wf.readframes(CHUNK)

    sleep(0.2)
    # Set to 0 the RGB value of each led on the strip
    for i in range(n_leds):
        ArduinoSerial.write(pack('>BBB', 0, 0, 0))
        sleep(0.05)

stream.close()
p.terminate()
