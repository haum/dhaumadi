#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# simon.py
#
# Copyright © 2017 Mathieu Gaborit (matael) <mathieu@matael.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Mathieu (matael) Gaborit wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#

"""
Main class for the Simon Says
"""

import os
import sys
import logging
import termios

from hw import Pad
from sequence import Sequence
from audio import AsciiAudio
import settings


class Simon:

    def __init__(self, pads_settings=settings.PRIMARY_PADS, initial_complexity=2,
            initial_length=1, end_of_game=42, audio=AsciiAudio()):
        """ Constr.
        pads_settings -- ip, color and notes for pads
        initial_complexity -- length of the first items of the sequence (number of pads)
        initial_length -- length of the sequence for the first round
        end_of_game -- length of sequence to match in order to win the game
        audio -- audio abstracted object to use
        """

        self.__pads = [
            Pad(
                laumio_ip=_['ip'],
                color=_['color'],
                notes=_['notes']
            ) for _ in pads_settings]

        self.initial_complexity = initial_complexity
        self.initial_length = initial_length
        self.end_of_game = end_of_game
        self.audio = audio

        self.reinit_game()

    def __str__(self):
        return str(self.seq) + '\n' + "(sequence length: " + str(len(self.seq)) + ')'
    
    def __repr__(seq):
        return repr(self.seq) + '\n' + "(sequence length: " + repr(len(self.seq)) + ')'

    def reinit_game(self, initial_complexity=None, initial_length=None):

        if initial_complexity is not None:
            self.initial_complexity = initial_complexity
        if initial_length is not None:
            self.initial_length = initial_length

        self.seq = Sequence(self.__pads, min_combo=self.initial_complexity)
        self.seq.lengthen(n=self.initial_length)
        self.__seq_pointer = 0
        self.added_complexity = 0
        self.succeses_since_complexity_bump = 0

        self.seq.play(self.audio)

    def process_line(self, line):
        """
        Choosen strategy :

        1. empty lines are ignored
        2. if a pad not expected is touched => game over
        3. if expected pads are touched but not all linked => wait next line for confirmation
        4. if all expected pads are linked together => got to next item
        """
        # 1. filter out useless
        if line.strip() == '':
            return

        # make some noise to show we got something
        groups = line.split(' ')
        for g in groups:
            self.seq.play_item(list(g), self.audio)

        # 2. check if players lost
        expected_combo = self.seq[self.__seq_pointer]
        for pad_id in line:
            if pad_id == ' ':
                continue
            elif int(pad_id) not in expected_combo:
                self.game_over()

        # 3. correct pads but not connected
        if len(groups) > 1:
            return

        # 4. all pads grouped together ?
        difference = set(expected_combo) - set(map(int, list(groups[0])))
        if difference == set():
            self.__seq_pointer += 1
            if self.__seq_pointer > self.end_of_game:
                self.win()
            if self.__seq_pointer == len(self.seq):
                self.ack_seq()
                self.__seq_pointer = 0
                if self.succeses_since_complexity_bump == 2:
                    self.added_complexity += 1
                    self.succeses_since_complexity_bump = 0
                else:
                    self.succeses_since_complexity_bump += 1
                self.seq.lengthen(1, added_complexity=self.added_complexity)
                logging.debug(f"Expected sequence: \n{str(self)}")
                self.seq.play(self.audio)
            logging.debug(f"Expected combination no {str(self.__seq_pointer)}: {self.seq.str_combination(self.__seq_pointer)}")
        else:
            logging.debug(f"Missing pads: {str(difference)}")
            return

    def start(self):
        """ Read lines on standard input and process them """
        self.__flush_stdin()
        for line in sys.stdin:
            self.process_line(line.strip())

    def __flush_stdin(self):
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

    def win(self):
        """ Animation to play when the game is finished """
        self.__flush_stdin()
        logging.info("Win !")
        pass

    def ack_seq(self):
        """ Correct sequence acknoledge move """
        self.__flush_stdin()
        pass

    def game_over(self):
        """ Game over move """
        logging.info('Game Over')
