#!/usr/bin/env python3

import os, random
import robomodules as rm
from messages import *
import requests
import json


ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)


URL = "https://robodog-gix.firebaseio.com/wearable/MPU9250.json"

FREQUENCY = 10

class FirebaseCommsModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = []
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)

    def msg_received(self, msg, msg_type):
        return

    def tick(self):
        r = requests.get(url = URL)
        data = r.json()
        msg = FirebaseMsg()
        msg.json = json.dumps(data)
        msg = msg.SerializeToString()
        self.write(msg, MsgType.FIREBASE_MSG)

def main():
    module = FirebaseCommsModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
