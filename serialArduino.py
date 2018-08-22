
from time import sleep
import datetime
import serial
#import urllib2, urllib, httplib
import json
import os 
from functools import partial


ser =serial.Serial('/dev/ttyACM0',115200);
data={"distance":0,"mt1":0,"mt2":0,"mt3":0}
status=0

def serReadWrite():
    print(ser.readline())
    ser.flushInput()
    lines=ser.readline().strip()
    values=lines.decode('ascii').split(',')
    if len(values)==4:
        mt1,mt2,mt3,distance=[float(s) for s in values]
        print(ser) 
        data = {"distance": distance,"mt1":mt1,"mt2":mt2,"mt3":mt3}
        print(data)
    #status will be received from pc, for eye light
    try:
        if data["distance"]<=10:    
            status=0
        elif data["distance"]<30:    
            status=1
        else:  
            status=2
        ser.write(str(status).encode())
    except NameError:
        data={"distance":0,"mt1":0,"mt2":0,"mt3":0}
        status=0
    print(status)  
    
        
while True:
	serReadWrite()
	sleep(.1)	
        #sleepTime  = int(sleepTime)
		