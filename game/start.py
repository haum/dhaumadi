#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# start.py
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
logging.getLogger().setLevel(logging.DEBUG)


from simon import Simon
from settings import PRIMARY_PADS
from audio import AsciiAudio


def main():
    game = Simon(
        pads_settings=PRIMARY_PADS,
        initial_complexity=2,
        initial_length=1,
        end_of_game=42,
        audio=AsciiAudio()
    )

    game.start()

if __name__=='__main__':
    main()


