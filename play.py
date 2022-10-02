#!/use/bin/env python
import RPi.GPIO as GPIO
import vlc
import random
import os
import time
import signal

files_path = os.path.join(os.path.dirname(__file__), "files")
files = os.listdir(files_path)

media_player = vlc.MediaPlayer()
servo = None

def move_jaw(angle):
    servo.ChangeDutyCycle(2+(angle/18))
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

def move_jaw_while_playing(delay=0.5):
    time.sleep(delay)
    while media_player.is_playing():
        print(".", end="", flush = True)
        time.sleep(0.3)
    print(";")

def play(filename):
    print("Playing file: " + filename)
    full_path = os.path.join(os.path.dirname(__file__), filename)
    media_player.set_media(vlc.Media(full_path))
    media_player.play()
    move_jaw_while_playing()

def button_callback(channel):
    move_jaw(random.randint(0,180))
    # play("files/" + random.choice(files))

try:
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # initially pulled low (off)
    GPIO.add_event_detect(10, GPIO.RISING, callback=button_callback)

    GPIO.setup(8, GPIO.OUT)
    servo = GPIO.PWM(8 ,50)
    servo.start(0)

    play("boot.mp3")

    signal.pause()

except KeyboardInterrupt:
    print("Thanks for playing")

finally:
    print("Cleaning up...")
    servo.stop()
    GPIO.cleanup()
