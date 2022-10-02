#!/use/bin/env python
import RPi.GPIO as GPIO
import vlc
import random
import os
import time
import signal

AUDIO_FILES_DIR = "files"
STARTUP_AUDIO = "boot.mp3"

BUTTON_PIN = 10
SERVO_PIN = 8

SERVO_MIN_ANGLE = 0
SERVO_MAX_ANGLE = 180
SERVO_INCREMENT = 0.5
SERVO_INTERVAL = 0.5
SERVO_TIME_TO_MOVE = 0.5

files_path = os.path.join(os.path.dirname(__file__), AUDIO_FILES_DIR)
files = os.listdir(files_path)

media_player = vlc.MediaPlayer()
servo = None

# BUG: Currently there is 2x delays:
#   1. move_jaw
#   2. jaw_sequence

def move_jaw(angle, time_to_move=SERVO_TIME_TO_MOVE):
    print(f"Moving to {angle} degrees")
    servo.ChangeDutyCycle(2+(angle/18))
    time.sleep(time_to_move)
    servo.ChangeDutyCycle(0)

def jaw_sequence():
    current = SERVO_MIN_ANGLE
    while current + SERVO_INCREMENT <= SERVO_MAX_ANGLE:
        current = current + SERVO_INCREMENT
        move_jaw(current)
        time.sleep(SERVO_INTERVAL)
    while current - SERVO_INCREMENT >= SERVO_MIN_ANGLE:
        current = current - SERVO_INCREMENT
        move_jaw(current)
        time.sleep(SERVO_INTERVAL)

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
    # move_jaw(random.randint(0,180))
    jaw_sequence()
    # play(AUDIO_FILES_DIR + random.choice(files))

try:
    GPIO.setmode(GPIO.BOARD)

    # Start with the pin initially pulled low (off)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=button_callback)

    GPIO.setup(SERVO_PIN, GPIO.OUT)
    servo = GPIO.PWM(SERVO_PIN ,50)
    servo.start(0)

    move_jaw(SERVO_MIN_ANGLE)
    play(STARTUP_AUDIO)

    signal.pause()

except KeyboardInterrupt:
    move_jaw(SERVO_MIN_ANGLE)
    print("Thanks for playing")

finally:
    print("Cleaning up...")
    servo.stop()
    GPIO.cleanup()
