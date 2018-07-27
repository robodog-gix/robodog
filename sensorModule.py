#!/usr/bin/env python3

import os, random
import robomodules as rm
from messages import *
import speech as sm

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 1

class SensorModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = []
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY)

    def msg_received(self, msg, msg_type):
        return

    def tick(self):
        sentences = sm.capture_speech()

        if len(sentences) > 0:
            msg = SensorMsg()
            for sentence in sentences:
                sentence_msg = msg.sentences.add()
                sentence_msg.conditions.extend(sentence['conditions'])
                sentence_msg.commands.extend(sentence['commands'])
                sentence_msg.questions.extend(sentence['questions'])
                sentence_msg.sentence = sentence['sentence']
                sentence_msg.sentiment = sentence['sentiment']

            msg = msg.SerializeToString()
            self.write(msg, MsgType.SENSOR_MSG)

def main():
    module = SensorModule(ADDRESS, PORT)
    module.run()

if __name__ == "__main__":
    main()
