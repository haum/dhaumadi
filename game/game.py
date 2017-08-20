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
import time
import logging
from enum import Enum, auto

logging.getLogger().setLevel(logging.DEBUG)

PADS = list(range(7))


def flush_stdin():
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)


# Readline state
class RS(Enum):
    SEQ_COMPLETE = auto()
    ERROR = auto()
    CONTINUE = auto()

class Game:

    def __init__(self, speed=.8):
        self.speed = speed

        self.sequence = []
        self.player_seqidx = 0

    def start(self):
        result = RS.SEQ_COMPLETE
        while result != RS.ERROR:

            if result == RS.SEQ_COMPLETE:
                self.add_item()
                self.output_seq()
                flush_stdin()

            for line in sys.stdin:
                logging.debug(line)
                result = self.process_line(line.strip())
                if result != RS.CONTINUE:
                    break

    def output_seq(self):
        for item in self.sequence:
            self.show_item(item, on=True)
            time.sleep(self.speed)
            self.show_item(item, on=False)
            time.sleep(self.speed)

    def show_item(self, item, on=True):
        logging.debug(', '.join(map(str, item))+f' ON:{on}')
        # TODO

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
        # TODO
        # for g in groups:
        #     self.seq.play_item(list(g), self.audio)

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
