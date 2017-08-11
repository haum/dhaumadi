#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# sequence.py
#
# Copyright © 2017 Mathieu Gaborit (matael) <mathieu@matael.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Mathieu (matael) Gaborit wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#

"""

"""

import logging
import random


class Sequence:
    """ Sequence

    Get's a set of primary elements to be combined into items.
    Has function to lengthen the sequence with an item of a given complexity.
    """

    def __init__(self, pads, min_combo=2, rounding_fun=round):
        self.round = rounding_fun
        self.min_combo = min_combo
        self.pads = pads
        self.padids = list(range(len(pads)))
        self.mean_complexity = min_combo  # allow for easy init
        self.seq = []

    def __str__(self):
        return '\n'.join(map(lambda _: ' '.join(map(str, _)), self.seq))

    def __repr__(self):
        return '\n'.join(map(lambda _: ' '.join(map(str, _)), self.seq))

    def __getitem__(self, n):
        return self.seq[n]

    def __len__(self):
        return len(self.seq)

    def str_combination(self, n):
        if n > -1 and n < len(self.seq):
            return ' '.join(map(str, self.seq[n]))
        else:
            return None

    def lengthen(self, n=1, added_complexity=0):
        """
        Lengthen by n the sequence.
        """

        for _ in range(n):
            if len(self.seq) >= 2 and self.seq[-1] == self.seq[-2]:
                avoid = self.seq[-1]
                new = self.seq[-1]
            else:
                avoid = []
                new = []

            # find size for the new item
            size_new = int(added_complexity)+random.randint(self.min_combo, self.round(self.mean_complexity)+1)
            if size_new >= len(self.pads):
                size_new = len(self.pads)-1
            while new == avoid:

                new = set()
                while len(new)<size_new:
                    new.add(random.choice(self.padids))

                new = list(new)

            self.seq.append(new)
            self.compute_complexity()

        return self.seq

    def compute_complexity(self):
        self.mean_complexity = sum(map(len, self.seq))/len(self.seq)

    def play_item(self, item, audio_out=None):

        if audio_out is not None:
            notes_to_play = []
            for padid in item:
                notes_to_play += self.pads[int(padid)].notes

            notes_to_play = set(notes_to_play)
            audio_out.play_notes(notes_to_play, time=1000)

        for padid in item:
            self.pads[int(padid)].lighton()

    def play(self, audio_out=None):

        for seqitem in self.seq:
            self.play_item(seqitem, audio_out=audio_out)
        logging.debug(f"Expected and played sequence: \n {str(self)}")
