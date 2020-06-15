import serial
import numpy as np
import pyaudio
import wave
from struct import pack
from time import sleep
from os import system

"""Tracks"""
tracks = {
    1: ('ofdream - thelema', 'C:/Users/Oscar/Music/wav/ofdream-thelema.wav'), 
    2: ('Mr Robot Main Theme', 'C:/Users/Oscar/Music/wav/MrRobotMainTheme.wav'), 
    3: ('Animadrop - Estrangement', 'C:/Users/Oscar/Music/wav/Animadrop-Estrangement.wav'), 
    4: ('NEVRKNW - Cant Forget You', 'C:/Users/Oscar/Music/wav/NEVRKNW-CantForgetYou.wav'), 
    5: ('Gabidulin Yarimov - Oman', 'C:/Users/Oscar/Music/wav/GabidulinYarimov-Oman.wav'), 
    6: ('Stefan Nixdorf - Megalomania', 'C:/Users/Oscar/Music/wav/StefanNixdorf-Megalomania.wav'), 
    7: ('Kuoga - Coquette Feat ivy', 'C:/Users/Oscar/Music/wav/Kuoga - Coquette Feat ivy.wav'), 
    8: ('2020-06-04-11-00-20-7868', 'C:/Users/Oscar/Music/wav/2020-06-04-11-00-20-7868.wav'), 
    9: ('TIN - Ticking', 'C:/Users/Oscar/Music/wav/TIN - Ticking.wav'), 
    10: ('KEAN DYSSO - Do It Now', 'C:/Users/Oscar/Music/wav/KEAN DYSSO - Do It Now.wav'), 
    11: ('Bones - MustBeARealDragWakingUpAndBeingYou', 'C:/Users/Oscar/Music/wav/Bones - MustBeARealDragWakingUpAndBeingYou.wav'), 
    12: ('I spoke to the devil in miami Instrumental', 'C:/Users/Oscar/Music/wav/I spoke to the devil in miami Instrumental.wav'), 
    13: ('Meg Myers - Desire Hucci Remix', 'C:/Users/Oscar/Music/wav/Meg Myers - Desire Hucci Remix.wav'), 
    14: ('Arkana - Ein Sof', 'C:/Users/Oscar/Music/wav/Ein Sof.wav'), 
    15: ('DOS-88 - Race To Mars', 'C:/Users/Oscar/Music/wav/DOS-88 - Race To Mars.wav'), 
    16: ('Animadrop - Dancing in the Rain', 'C:/Users/Oscar/Music/wav/Animadrop - Dancing in the Rain.wav'), 
    17: ('DOS-88 - City Stomper', 'C:/Users/Oscar/Music/wav/DOS-88 - City Stomper.wav'), 
    18: ('Danger - 1:42', 'C:/Users/Oscar/Music/wav/Danger - 142.wav'),
    19: ('Unknown Brain - War Zone ft MIME', 'C:/Users/Oscar/Music/wav/Unknown Brain - War Zone ft MIME.wav'),
    20: ('Layto - Beauty', 'C:/Users/Oscar/Music/wav/Layto - Beauty.wav'),
    21: ('Kipher - Goons', 'C:/Users/Oscar/Music/wav/Kipher - Goons.wav'),
    22: ('Neo Fresco - Sublimation Original Mix', 'C:/Users/Oscar/Music/wav/Neo Fresco -Sublimation Original Mix.wav'),
    23: ('XXXTENTACION - ALONE LXRY Remix', 'C:/Users/Oscar/Music/wav/XXXTENTACION - ALONE LXRY Remix.wav'),
    24: ('EA7 - Lucky Luke - DRG feat Emie', 'C:/Users/Oscar/Music/wav/EA7 - Lucky Luke - DRG feat Emie.wav'),
    25: ('Barlas Mert - Killing Me', 'C:/Users/Oscar/Music/wav/Barlas Mert - Killing Me.wav'),
    26: ('LEViTTE - Maniac', 'C:/Users/Oscar/Music/wav/LEViTTE - Maniac.wav')
    }

def set_RGB_color(freq):
    CONV_HZ_TO_RGB = 7.28597268

    if freq <= 0: var = 0
    elif freq > 8000: var = 255
    else: var = int(freq / CONV_HZ_TO_RGB)
    print("Var is:", var)

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

stream.close()
p.terminate()