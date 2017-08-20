#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# game.py
#
# Copyright © 2017 HAUM <contact@haum.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Mathieu (matael) Gaborit wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#

import pdb # TODO

import os
import sys
import termios
import random
import socket
import time
import logging
import multiprocessing.dummy as mp
from enum import Enum, auto

logging.getLogger().setLevel(logging.DEBUG)

# add the submodule to the path (make sure submodules are initialized)
submodule_path = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../_submodules/laumio/python'
))
sys.path.append(submodule_path)
if os.path.exists(submodule_path):
    from laumio import Laumio
else:
    logging.critical('Please initialize submodules first')
    sys.exit(1)

PADS = list(range(7))


def flush_stdin():
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)


# Readline state
class RS(Enum):
    SEQ_COMPLETE = auto()
    ERROR = auto()
    CONTINUE = auto()

class FluidSynthClient:

    NOTES = (57, 59, 61, 64, 66, 69, 71)

    def __init__(self, ip='localhost', port=9800):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((ip, port))
            self.socket.send(b'gain 5\n')
        except ConnectionRefusedError:
            logging.warning('Unable to conect to FluidSynth server')
            self.socket = False

    def note(self, pad, on):
        onoff = 'off'
        if on: onoff = 'on'
        note = FluidSynthClient.NOTES[pad]
        if self.socket:
            self.socket.send(f'note{onoff} 0 {note} 127\n'.encode())

class PadsManager(Laumio):

    def __init__(self, ip='localhost'):
        super().__init__(ip)

    def display_item(self, item, on):
        color = (0, 0, 0)
        if on:
            color = (255, 0, 0)
        for pad in item:
            self.led(pad, color)

    def led(self, pad, color):
        self.setPixelColor(pad*4+0, *color)
        self.setPixelColor(pad*4+1, *color)
        self.setPixelColor(pad*4+2, *color)
        self.setPixelColor(pad*4+3, *color)

class Game:

    def __init__(self, speed=.8, audio=FluidSynthClient(), pads=PadsManager()):
        self.speed = speed
        self.audio = audio
        self.pads = pads

        self.sequence = []
        self.player_seqidx = 0
        self.workers = mp.Pool(processes=4)

    def start(self):
        result = RS.SEQ_COMPLETE
        while result != RS.ERROR:

            if result == RS.SEQ_COMPLETE:
                self.add_item()
                self.output_seq()
                flush_stdin()

            for line in sys.stdin:
                result = self.process_line(line.strip())
                if result != RS.CONTINUE:
                    break

    def output_seq(self):
        for item in self.sequence:
            self.__play_item(item)

    def __play_item(self, item, speed=None):
        speed = self.speed if speed is None else speed
        self.show_item(item, on=True)
        time.sleep(speed)
        self.show_item(item, on=False)
        time.sleep(speed)

    def show_item(self, item, on=True):
        logging.debug(', '.join(map(str, item))+f' ON:{on}')
        self.pads.display_item(item, on)
        for pad in item:
            self.audio.note(pad, on)

    def add_item(self, length=2):
        new_item = [0]*length
        while len(set(new_item)) != length:
            new_item = random.choices(PADS, k=length)
        self.sequence.append(tuple(new_item))

    def process_line(self, line):
        """
        Returns false if line triggered loss

        Choosen strategy :

        1. empty lines are ignored
        2. if a pad not expected is touched => game over
        3. if expected pads are touched but not all linked => wait next line for confirmation
        4. if all expected pads are linked together => got to next item
        """
        # 1. filter out useless
        if line.strip() == '':
            return

        groups = line.split(' ')
        # make some noise to show we got something
        for g in groups:
            self.workers.apply_async(self.__play_item, [tuple(map(int, list(g))), self.speed/2])
            time.sleep(self.speed/4)

        time.sleep(self.speed/2*len(groups))



        # 2. check if players lost
        expected_item = self.sequence[self.player_seqidx]
        for pad_id in line:
            if pad_id == ' ':
                continue
            elif int(pad_id) not in expected_item:
                return RS.ERROR

        # 3. correct pads but not connected
        if len(groups) > 1:
            return RS.CONTINUE

        # 4. all pads grouped together ?
        difference = set(expected_item) - set(map(int, list(groups[0])))
        if difference == set():
            self.player_seqidx += 1
            if self.player_seqidx == len(self.sequence):
                self.player_seqidx = 0
                return RS.SEQ_COMPLETE
            else:
                return RS.CONTINUE
        else:
            return RS.CONTINUE



def main():
    g = Game()
    g.start()


if __name__ == "__main__":
    main()
