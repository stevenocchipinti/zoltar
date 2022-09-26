import RPi.GPIO as GPIO
import vlc
import random
import os

media_player = vlc.MediaPlayer()
files = os.listdir("files")

def play(file):
    print("Playing file: " + file)
    media_player.set_media(vlc.Media(file))
    media_player.play()

def button_callback(channel):
    play("files/" + random.choice(files))

GPIO.setmode(GPIO.BOARD)

GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # initially pulled low (off)
GPIO.add_event_detect(10, GPIO.RISING, callback=button_callback)

play("boot.mp3")
input("Press any key to quit")

GPIO.cleanup()
