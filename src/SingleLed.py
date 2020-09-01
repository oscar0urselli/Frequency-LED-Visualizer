import numpy as np
from time import sleep
import os
import wave

import pyaudio
import pyfirmata

def brightness(freq, leds = []):
    """Constants"""
    CONV_1_TO_RGB = 0.00390625
    CONV_HZ_TO_RGB = 7.28597268 
    
    if freq <= 0:
        var = 0
    else:
        var = (freq / CONV_HZ_TO_RGB) * CONV_1_TO_RGB
        
    for i in leds:
        i.write(var)

def set_pins(pin = []):
    pin_set = []
    for i in pin: pin_set.append(board.get_pin('d:' + str(i) + ":p"))

    return pin_set

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
# Set digital pin in PWM mode for the led
pin_ls = set_pins([3])


"""Variables for the frequency detection"""
CHUNK = 2048

while True:
    # Opening the wav file
    wf = wave.open(play(path), 'rb')

    swidth = wf.getsampwidth()
    RATE = wf.getframerate()
    # Use of a Blackman window
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

        # Unpcak the data and multiplicate it by the hamming window
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
    
        if not np.isnan(thefreq):
            brightness(freq = thefreq, leds = pin_ls)

        # Read more data
        data = wf.readframes(CHUNK)

    # Set to 0 the leds value
    for p in pin_ls: p.write(0)
    
stream.close()
p.terminate()
