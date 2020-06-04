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
    18: ('Danger - 1:42', 'C:/Users/Oscar/Music/wav/Danger - 142.wav')
    }

global freq_range, increase_const
freq_range = []

# Max frequency, length range, increase const, start point
settings = {1: (8000, 20, 0.0025, 20), 2: (3500, 2, 0.0005714286, -100), 3: (8000, 2, 0.0005, 2)}

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

while True:
    system('cls')
    print("Select a setting:")
    print("1) Standard")
    print("2) Bass")
    print("3) High sensibility")
    setting_type = int(input())

    if setting_type in settings:
        break
    else:
        print("This setting doesn't exist!")
        sleep(2)


for i in range(settings[setting_type][3], settings[setting_type][0], settings[setting_type][1]):
    freq_range.append((i - settings[setting_type][1], i))
increase_const = settings[setting_type][2]

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
        print("The frequency is {0} Hz".format(thefreq))
    else:
        thefreq = which * RATE / chunk

        print("The frequency is {0} Hz".format(thefreq))

    brightness(freq = thefreq, led = led_pin)

    data = wf.readframes(chunk)

if data:
    stream.write(data)

led_pin.write(0)
    
stream.close()
p.terminate()
