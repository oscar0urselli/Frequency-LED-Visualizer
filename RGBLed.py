import pyaudio
import wave
import numpy as np
import pyfirmata
from time import sleep
from os import system

"""Track"""
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
    22: ('Neo Fresco - Sublimation Original Mix', 'C:/Users/Oscar/Music/wav/Neo Fresco - Sublimation Original Mix.wav')
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

"""
def set_RGB_color(freq, red = 2, green = 5, blue = 6):
    set_52 = 0.203125
    set_235 = 0.91796875
    CONV_1_TO_RGB = 0.00390625
    CONV_HZ_TO_RGB = 7.28597268

    # B+
    if freq <= 1333.333:
        red.write(set_235)
        green.write(set_52)
        blue.write((freq / CONV_HZ_TO_RGB) * CONV_1_TO_RGB)
    # R-
    elif freq > 1333.333 and freq <= 2666.666:
        red.write((freq / CONV_HZ_TO_RGB) * CONV_1_TO_RGB)
        green.write(set_52)
        blue.write(set_235)
    # G+
    elif freq > 2666.666 and freq <= 4000:
        red.write(set_52)
        green.write((freq / CONV_HZ_TO_RGB) * CONV_1_TO_RGB)
        blue.write(set_235)
    # B-
    elif freq > 4000 and freq <= 5333.333:
        red.write(set_52)
        green.write(set_235)
        blue.write((freq / CONV_HZ_TO_RGB) * CONV_1_TO_RGB)
    # R+
    elif freq > 5333.333 and freq <= 6666.666:
        red.write((freq / CONV_HZ_TO_RGB) * CONV_1_TO_RGB)
        green.write(set_235)
        blue.write(set_52)
    # G-
    else:
        red.write(set_235)
        green.write((freq / CONV_HZ_TO_RGB) * CONV_1_TO_RGB)
        blue.write(set_52)
"""
        
def set_RGB_color(freq, red = [], green = [], blue = []):
    CONV_1_TO_RGB = 0.00390625

    if freq < 40:
        for i in red: i.write(1)
        for i in green: i.write(0)
        for i in blue: i.write(0)
    elif freq >= 40 and freq <= 77:
        var = ((freq - 40) * (255 / 37)) * CONV_1_TO_RGB
        for i in red: i.write(1)
        for i in green: i.write(0)
        for i in blue: i.write(var)
    elif freq > 77 and freq <= 205:
        var = (255 - ((freq - 78) * 2)) * CONV_1_TO_RGB
        for i in red: i.write(var)
        for i in green: i.write(0)
        for i in blue: i.write(1)
    elif freq >= 206 and freq <= 238:
        var = ((freq - 206) * (255 / 32)) * CONV_1_TO_RGB
        for i in red: i.write(0)
        for i in green: i.write(var)
        for i in blue: i.write(1)
    elif freq >= 239 and freq <= 250:
        var = ((freq - 239) * (255 / 11)) * CONV_1_TO_RGB
        for i in red: i.write(var)
        for i in green: i.write(1)
        for i in blue: i.write(1)
    elif freq >= 251 and freq <= 270:
        for i in red: i.write(1)
        for i in green: i.write(1)
        for i in blue: i.write(1)
    elif freq >= 271 and freq <= 398:
        var = (255 - ((freq - 271) * 2)) * CONV_1_TO_RGB
        for i in red: i.write(var)
        for i in green: i.write(1)
        for i in blue: i.write(var)
    elif freq >= 398 and freq <= 653:
        for i in red: i.write(0)
        for i in green: i.write((255 - (freq - 398)) * CONV_1_TO_RGB)
        for i in blue: i.write((freq - 398) * CONV_1_TO_RGB)
    else:
        for i in red: i.write(1)
        for i in green: i.write(0)
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
chunk = 2048

wf = wave.open(choosen_track, 'rb')

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
    else:
        thefreq = which * RATE / chunk

    print("The frequency is {0} Hz".format(thefreq))

    if not np.isnan(thefreq):
        set_RGB_color(freq = thefreq, red = [redLedPin1, redLedPin2], green = [greenLedPin1, greenLedPin2], blue = [blueLedPin1, blueLedPin2])

    data = wf.readframes(chunk)

if data:
    stream.write(data)

redLedPin1.write(0)
greenLedPin1.write(0)
blueLedPin1.write(0)

redLedPin2.write(0)
greenLedPin2.write(0)
blueLedPin2.write(0)

stream.close()
p.terminate()
