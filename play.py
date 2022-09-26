#!/use/bin/env python
import RPi.GPIO as GPIO
import vlc
import random
import os
from signal import pause

media_player = vlc.MediaPlayer()

files_path = os.path.join(os.path.dirname(_file_), "files")
files = os.listdir(files_path)

def play(filename):
    print("Playing file: " + filename)
    full_path = os.path.join(os.path.dirname(_file_), filename)
    media_player.set_media(vlc.Media(full_path))
    media_player.play()

def button_callback(channel):
    play("files/" + random.choice(files))

try:
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # initially pulled low (off)
    GPIO.add_event_detect(10, GPIO.RISING, callback=button_callback)

    play("boot.mp3")
    pause()

except KeyboardInterrupt:
    print("Thanks for playing")

finally:
    print("Cleaning up...")
    GPIO.cleanup()
