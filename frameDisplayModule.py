#!/usr/bin/env python3

import os, sys
import cv2
import robomodules as rm
import pygame
import numpy as np
from messages import message_buffers, MsgType

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 11297)

FREQUENCY = 20

FRAME_WIDTH = 640
SCREEN_SIZE = (FRAME_WIDTH, 480)
CAM_ID = 1

class FrameDisplayModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.CAMERA_FRAME_MSG]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.frames = {}
        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode(SCREEN_SIZE)

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # We receive pickled frames here.
        if msg_type == MsgType.CAMERA_FRAME_MSG:
            if msg.id == CAM_ID:
                self.frames[msg.id] = msg.cameraFrame
        
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit('quit')
        self._display_frames()
        pygame.display.update()

    def _display_frames(self):
        cur_x = 0
        raw_frame = self.frames[CAM_ID]
        nparr = np.frombuffer(raw_frame, np.uint8)
        frame = cv2.imdecode(nparr, -1)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        cur_width = frame.get_width()
        cur_height = frame.get_height()
        new_height = int(cur_height * FRAME_WIDTH/cur_width)
        frame = pygame.transform.scale(frame, (FRAME_WIDTH, new_height))
        self.display.blit(frame,(cur_x,0))
        cur_x += frame.get_width()

def main():
    module = FrameDisplayModule(ADDRESS, PORT)
    module.run()
    pygame.quit()

if __name__ == "__main__":
    main()
