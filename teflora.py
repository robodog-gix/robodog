
import datetime
from firebase import firebase
from firebase_admin import db
import pyrebase

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



def main():
    
    config = {
    "apiKey": "AIzaSyCJvtBdqcl8Xv-Y1Sic9_kbw1mfvwYSCHc",
    "authDomain": "farmina-5c940.firebaseapp.com",
    "databaseURL": "https://farmina-5c940.firebaseio.com",
    "projectId": "farmina-5c940",
    "storageBucket": "farmina-5c940.appspot.com"
    }
    firebase=pyrebase.initialize_app(config)
    db=firebase.database()
    
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('turn off the light')
    recognizer.expect_phrase('turn on the light')
    recognizer.expect_phrase('blink')

    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()
    
    file= open('/home/pi/Downloads/file.json','r')
    for line in file:
        list=(json.loads(line))
    
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
                print("c")
            elif 'turn off the light' in text:
                print("a")
            elif 'blink' in text:
                print("b")
            elif 'goodbye' in text:
                break
            for row in list:
                if(row['question']==text):
                    answer=row['answer']
                    answer=answer.replace('{temp}',str(db.child('sensor').child('temperature').get().val()),1)
                    answer=answer.replace('{lux}',str(db.child('sensor').child('lux').get().val()),1)
                    answer=answer.replace('{hum}',str(db.child('sensor').child('humidity').get().val()),1)
                    answer=answer.replace('{wl}',str(db.child('sensor').child('water level').get().val()),1)
                    answer=answer.replace('{wt}',str(db.child('sensor').child('water temp').get().val()),1)
                    aiy.audio.say(answer)    


if __name__ == '__main__':
    main()
