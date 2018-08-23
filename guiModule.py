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
SCREEN_SIZE = (FRAME_WIDTH*2, 900)
CAM_ID = 0

class GuiModule(rm.ProtoModule):
    def __init__(self, addr, port):
        self.subscriptions = [MsgType.CAMERA_FRAME_MSG, MsgType.SENSOR_MSG, MsgType.FIREBASE_MSG]
        super().__init__(addr, port, message_buffers, MsgType, FREQUENCY, self.subscriptions)
        self.frames = {}
        self.sentences = []
        pygame.init()
        pygame.font.init()
        self.text_surf = pygame.Surface((FRAME_WIDTH-10, 800))
        self.firebase_data_surf = pygame.Surface((SCREEN_SIZE[0]-10, 200))
        self.firebase_json = ''
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
        self.display = pygame.display.set_mode(SCREEN_SIZE)

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # We receive pickled frames here.
        if msg_type == MsgType.CAMERA_FRAME_MSG:
            if msg.id == CAM_ID:
                self.frames[msg.id] = msg.cameraFrame
        elif msg_type == MsgType.SENSOR_MSG:
            self.sentences = msg.sentences
        elif msg_type == MsgType.FIREBASE_MSG:
            self.firebase_json = msg.json
        
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit('quit')
        self._display_frames()
        self._draw_speech()
        self._draw_firebase_data()
        pygame.display.update()

    def _draw_speech(self):
        self.text_surf.fill((0,0,0))
        red = (255, 0, 0)
        green = (0, 255, 0)
        white = (255, 255, 255)
        y = 0
        for sentence in self.sentences:
            sentence_surf = self.font.render(f'Sentence: {sentence.sentence}', True, (255, 255, 255))
            self.text_surf.blit(sentence_surf, (0, y))
            y += 40
            col = white
            if sentence.sentiment > 0:
                col = green
            elif sentence.sentiment < 0:
                col = red
            sentiments_surf = self.font.render(f'Sentiment score: {round(sentence.sentiment, 3)}', True, col)
            self.text_surf.blit(sentiments_surf, (0, y))
            y += 40
            questions_surf = self.font.render('Questions:', True, (255, 255, 255))
            self.text_surf.blit(questions_surf, (0, y))
            y += 40
            for q in sentence.questions:
                q_surf = self.font.render(q, True, (255, 255, 255))
                self.text_surf.blit(q_surf, (30, y))
                y += 40
            commands_surf = self.font.render('Commands:', True, (255, 255, 255))
            self.text_surf.blit(commands_surf, (0, y))
            y += 40
            for cmd in sentence.commands:
                cmd_surf = self.font.render(cmd, True, (255, 255, 255))
                self.text_surf.blit(cmd_surf, (30, y))
                y += 40
            conditions_surf = self.font.render('Conditions:', True, (255, 255, 255))
            self.text_surf.blit(conditions_surf, (0, y))
            y += 40
            for cond in sentence.conditions:
                cond_surf = self.font.render(cond, True, (255, 255, 255))
                self.text_surf.blit(cond_surf, (30, y))
                y += 40
            y += 40
        self.display.blit(self.text_surf, (SCREEN_SIZE[0]-FRAME_WIDTH+10, 10))

    def _draw_firebase_data(self):
        self.firebase_data_surf.fill((0,0,0))
        white = (255, 255, 255)
        sentence_surf = self.font.render(self.firebase_json, True, white)
        self.firebase_data_surf.blit(sentence_surf, (0, 0))
        self.display.blit(self.firebase_data_surf, (0, SCREEN_SIZE[1]-50))

    def _display_frames(self):
        cur_x = 0
        if CAM_ID in self.frames:
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
    module = GuiModule(ADDRESS, PORT)
    module.run()
    pygame.quit()

if __name__ == "__main__":
    main()
