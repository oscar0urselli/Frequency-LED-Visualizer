import pyaudio
import wave
import numpy as np
import pyfirmata
from time import sleep
from os import system

global freq_range, increase_const
freq_range = []
# Work in progress
"""
# Max frequency, length range, increase const
settings = {1: (8000, 20, 0.0025), 2: (2000, 2, 0.001)}

while True:
    system('cls')
    print("Select a setting:")
    print("1) Standard")
    print("2) Bass")
    print("3) **Work in progress**")
    setting_type = int(input())

    if setting_type in settings:
        break
    else:
        print("This setting doesn't exist!")
        sleep(2)

for i in range(settings[setting_type][1], settings[setting_type][0], settings[setting_type][1]):
    freq_range.append((i - settings[setting_type][1], settings[setting_type][1]))
increase_const = settings[setting_type][2]
"""

for i in range(20, 8020, 20):
    freq_range.append((i - 20, i))
increase_const = 0.0025

def brightness(freq, led = 13):
    for i in freq_range:
        if freq >= i[0] and freq <= i[1]:
            led.write(freq_range.index(i) * increase_const)
            break
        if i == freq_range[len(freq_range) - 1] and freq > i[1]:
            led.write(1)
            break


"""Variables for Arduino"""
board = pyfirmata.Arduino('COM4')

it = pyfirmata.util.Iterator(board)
it.start()

# Set digital pin 3 in PWM mode
led_pin = board.get_pin('d:3:p')


"""Variables for the frequency detection"""
chunk = 2048

#wf = wave.open('C:/Users/Oscar/Music/wav/ofdream-thelema.wav', 'rb')
#wf = wave.open('C:/Users/Oscar/Music/wav/MrRobotMainTheme.wav', 'rb')
#wf = wave.open('C:/Users/Oscar/Music/wav/Animadrop-Estrangement.wav', 'rb')
#wf = wave.open('C:/Users/Oscar/Music/wav/NEVRKNW-CantForgetYou.wav', 'rb')
#wf = wave.open('C:/Users/Oscar/Music/wav/GabidulinYarimov-Oman.wav', 'rb')
wf = wave.open('C:/Users/Oscar/Music/wav/StefanNixdorf-Megalomania.wav', 'rb')
#wf = wave.open('C:/Users/Oscar/Music/wav/Kuoga - Coquette Feat ivy.wav', 'rb')
#wf = wave.open('C:/Users/Oscar/Music/wav/2020-06-04-11-00-20-7868.wav', 'rb')
#wf = wave.open('C:/Users/Oscar/Music/wav/TIN - Ticking.wav', 'rb')

swidth = wf.getsampwidth()
RATE = wf.getframerate()

window = np.blackman(chunk)

p = pyaudio.PyAudio()
stream = p.open(
    format = p.get_format_from_width(wf.getsampwidth()),
    channels = wf.getnchannels(),
    rate = RATE,
    output = True
)

data = wf.readframes(chunk)

while len(data) == chunk * swidth:
    stream.write(data)

    indata = np.array(wave.struct.unpack("%dh" % (len(data) / swidth), data)) * window

    fftData = abs(np.fft.rfft(indata)) ** 2

    which = fftData[1:].argmax() + 1

    if which != len(fftData) - 1:
        y0, y1, y2 = np.log(fftData[which - 1: which + 2])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)

        thefreq = (which + x1) * RATE / chunk
        print("The frequency is {0} Hz".format(thefreq))
    else:
        thefreq = which * RATE / chunk

        print("The frequency is {0} Hz".format(thefreq))

    brightness(freq = thefreq, led = led_pin)

    data = wf.readframes(chunk)

if data:
    stream.write(data)

stream.close()
p.terminate()
