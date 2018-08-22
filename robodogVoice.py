
import datetime
import os 
from functools import partial

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
from time import sleep
from gpiozero import PWMOutputDevice
from time import sleep
from gpiozero import Servo
    
import csv
import json

pwmL=PWMOutputDevice(4)
pwmR=PWMOutputDevice(27)

def main():
    
   
    
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('turn off the light')
    recognizer.expect_phrase('turn on the light')
    recognizer.expect_phrase('blink')

    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()
    
   
    
#    file= open('/home/pi/Downloads/file.json','r')
 #   for line in file:
  #      list=(json.loads(line))
    
    while True:
        print('Press the button and speak')
        button.wait_for_press()
        print('Listening...')
        text = recognizer.recognize()
        print('You said "', text, '"')
        if text is None:
            print('Sorry, I did not hear you.')
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
            
                #update status to rainbow cycle 
      #      elif 'goodbye' in text:
     #           break
#            for row in list:
 #               if(row['question']==text):
  #                  answer=row['answer']
   #                 answer=answer.replace('{temp}',str(db.child('sensor').child('temperature').get().val()),1)
    #              answer=answer.replace('{wl}',str(db.child('sensor').child('water level').get().val()),1)
       #             answer=answer.replace('{wt}',str(db.child('sensor').child('water temp').get().val()),1)
        #            aiy.audio.say(answer)    

def spin(rad=1,speed=1):
    pwmL.value=0.2
    pwmR.value=1.0
    sleep(2)
    pwmL.off()
    pwmR.off()
    
def figEight(rad=1,speed=1):
    pwmL.value=0.2
    pwmR.value=1.0
    sleep(2)
    pwmL.value=1.0
    pwmR.value=0.2
    sleep(2)
    pwmL.off()
    pwmR.off()

def turn(deg=90):
    if deg>0:
        pwmL.value=0.2
        pwmR.value=1.0
    if deg<=0:
        pwmL.value=1
        pwmR.value=0.2
    sleep(abs(deg/180))
    pwmL.off()
    pwmR.off()


if __name__ == '__main__':
    main()
