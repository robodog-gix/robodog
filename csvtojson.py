import json
import csv

csvfile= open('/home/pi/Downloads/Voice Interactions - Sheet1.csv', newline='')
reader = csv.reader(csvfile, quotechar='|')

with open('/home/pi/Downloads/file.json', 'w') as file:
    data=[]
    for row in reader:
        info={'question':row[0],'answer':row[1]}
        data.append(info)
    file.write(json.dumps(data))
    file.close()

