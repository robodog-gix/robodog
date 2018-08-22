
import datetime
import os 
from functools import partial

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import time
from gpiozero import PWMOutputDevice
from time import sleep
from gpiozero import Servo
    
import csv
import json
import keyboard

import serialArduino

pwmL=PWMOutputDevice(4)
pwmR=PWMOutputDevice(27)
ser =serial.Serial('/dev/ttyACM0',115200)
data={"distance":0,"mt1":0,"mt2":0,"mt3":0}
    
def voiceCommand():
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('turn off the light')
    recognizer.expect_phrase('turn on the light')
    recognizer.expect_phrase('blink')

    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()
    init_time = time.time()
    print('Press i and speak')
    ser.write(str(0).encode())
    #button.wait_for_press()
    if keyboard.is_pressed('i'):
        while True:
            print('Listening...')

            text = recognizer.recognize()
            print('You said "', text, '"')
            if text is None:
                print('Sorry, I did not hear you.')
                break
            else:
                if 'good boy' in text:
                    spin()               
                elif 'bad boy' in text:
                    aiy.audio.say("sorry")
                elif 'i love you' in text:
                    figEight()
                elif 'turn left' in text:
                    turn(deg=-90)
                elif 'turn right' in text:
                    turn(deg=90)
                elif time.time()- init_time >= 60:
                    break             

#To do: sending text to the computer

def spin(rad=1,speed=1):
    pwmL.value=0.2
    pwmR.value=1.0
    obstacleAvoid(2)
    pwmL.off()
    pwmR.off()
    
def figEight(rad=1,speed=1):
    pwmL.value=0.2
    pwmR.value=1.0
    obstacleAvoid(2)
    pwmL.value=1.0
    pwmR.value=0.2
    obstacleAvoid(2)
    pwmL.off()
    pwmR.off()

def turn(deg=90):
    if deg>0:
        pwmL.value=0.2
        pwmR.value=1.0
    if deg<=0:
        pwmL.value=1
        pwmR.value=0.2
    obstacleAvoid(abs(deg/180))
    pwmL.off()
    pwmR.off()

def obstacleAvoid(duration):
    start_time = time.time()
    while True:
        sensorData = serialArduino.serReadWrite()
        #data = {"distance": distance,"mt1":mt1,"mt2":mt2,"mt3":mt3}

        if sensorData.distance0 <= 20 or sensorData.distance1 <=20 or sensorData.distance2 <= 20:
            pwmL.off()
            pwmR.off()
        
        time = time.time()
        if time - start_time >= duration:
            break 




if __name__ == '__main__':
    main()
