import numpy as np
from time import sleep
import os
import wave

import pyaudio
import pyfirmata

def set_RGB_color(freq, red = [], green = [], blue = []):
    """Constants"""
    CONV_1_TO_RGB = 0.00390625
    CONV_HZ_TO_RGB = 7.28597268

    if freq <= 0: var = 0
    else: var = (freq / CONV_HZ_TO_RGB) * CONV_1_TO_RGB

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

def set_pins(red = [], green = [], blue = []):
    red_set, green_set, blue_set = [], [], []
    for i in red: red_set.append(board.get_pin('d:' + str(i) + ":p"))
    for i in green: green_set.append(board.get_pin('d:' + str(i) + ":p"))
    for i in blue: blue_set.append(board.get_pin('d:' + str(i) + ":p"))

    return red_set, green_set, blue_set

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

"""Variables for Arduino"""
# Serial port used for the comunication with Arduino.
# Change if you use a different one
board = pyfirmata.Arduino('COM4')

it = pyfirmata.util.Iterator(board)
it.start()

"""List of pin to set"""
# Set digital pin in PWM mode for RGB led
red_ls, green_ls, blue_ls = set_pins(red = [3], green = [5], blue = [6])

"""Variables for the frequency detection"""
CHUNK = 2048

while True:
    # Opening the wav file
    wf = wave.open(play(path), 'rb')

    swidth = wf.getsampwidth()
    RATE = wf.getframerate()
    # Use of the Blackman window
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

        # Unpack the data and multiplicate it by the hamming window
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
            set_RGB_color(freq = thefreq, red = red_ls, green = green_ls, blue = blue_ls)

        # Read more data
        data = wf.readframes(CHUNK)

    # Set to 0 the RGB value
    for r in red_ls: r.write(0)
    for g in green_ls: g.write(0)
    for b in blue_ls: b.write(0)

stream.close()
p.terminate()
