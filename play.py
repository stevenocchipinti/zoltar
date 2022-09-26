import RPi.GPIO as GPIO
import vlc
import random
import os

AUDIO_DIR = "files"

media_player = vlc.MediaPlayer()
files = os.listdir("files")

def button_callback(channel):
    print("Button pressed!")
    file = random.choice(files)
    print("Playing file: " + file)
    media_player.set_media(vlc.Media(AUDIO_DIR + "/" + file))
    media_player.play()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # initially pulled low (off)
GPIO.add_event_detect(10, GPIO.RISING, callback=button_callback)

input("Press any key to quit")

GPIO.cleanup()
