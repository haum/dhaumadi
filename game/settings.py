#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# settings.py
#
# Copyright © 2017 Mathieu Gaborit (matael) <mathieu@matael.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Mathieu (matael) Gaborit wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#

"""
Settings for the game

PRIMARY_PADS: describe pads (Laumio's IP, set of notes and color)
"""

PRIMARY_PADS = [
    {'ip': '192.168.42.1',
     'notes': [76],
     'color': (0, 0, 255)},
    {'ip': '192.168.42.2',
     'notes': [77],
     'color': (0, 0, 255)},
    {'ip': '192.168.42.3',
     'notes': [78],
     'color': (0, 0, 255)},
    {'ip': '192.168.42.4',
     'notes': [79],
     'color': (0, 0, 255)},
    {'ip': '192.168.42.5',
     'notes': [80],
     'color': (0, 0, 255)},
]
