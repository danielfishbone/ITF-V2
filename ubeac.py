
import time
from datetime import datetime
import json
import requests
from random import randint

url = "http://fishbone.hub.ubeac.io/fishbonefiverr"
url = "http://itfiot.hub.ubeac.io/ITFV2"
uid = "RPI"
uid ="POT"

try:
    while True:
        temperature = randint(0,100) 
        data = {
                "id": uid,
                "sensors":[{
                  'id': 'potentiometer',
                  'data': temperature
                }]
            }
        
        r = requests.post(url, verify=False, json=data)
        print(r.status_code)
        print(datetime.now())
        print(time.time())
        time.sleep(.5)
 
except KeyboardInterrupt:
    pass
