import RPi.GPIO as GPIO
import time
buttonPin = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin,GPIO.IN)
prev_input =0
while True:
  input = GPIO.input(14)
  if ((not prev_input) and input):
    print("Button pressed")
  prev_input = input
  time.sleep(0.05)
