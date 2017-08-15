#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# audio.py
#
# Copyright © 2017 Mathieu Gaborit (matael) <mathieu@matael.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Mathieu (matael) Gaborit wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#

"""
Abstraction on a sound playing system
"""

import logging
import socket

class Audio:
    """ Base class for audio system

    Abstraction of audio playing must be non-blocking
    (thread, subprocess, async, etc...)
    """

    def __init__(self):
        pass

    def play_notes(self, notes=[], time=1000):
        """
        Play notes

        notes -- list of int (midi notes)
        time -- time in millisecond
        """
        pass


class AsciiAudio(Audio):
    """ A dummy (non) audio abstraction that just prints notes on stdout """

    def __init__(self):
        super().__init__()

    def play_notes(self, notes=[], time=1000):
        notes_as_str = ' '.join(map(str, notes))
        print(f'Playing for {time}ms: {notes_as_str}')

class FluidSynthAudio(Audio):
    """ A class that sends notes to fluidsynth via its TCP shell """

    def __init__(self, ip='localhost', port=9800):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
        self.socket.send(b'gain 5\n')
        super().__init__()

    def play_notes(self, notes=[], time=1000):
        notes_as_str = ' '.join(map(str, notes))
        print(f'Playing for {time}ms: {notes_as_str}')
        buff = b''
        for note in map(str, notes):
            buff += b'noteon 0 '
            buff += bytes(note, 'utf-8')
            buff += b' 127\n'
        print(buff)
        self.socket.send(buff)


