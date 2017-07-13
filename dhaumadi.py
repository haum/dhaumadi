#!/usr/bin/env python

import serial

inhib = 0
touches = {}
oldgroups = set()
groupstability = 0
laststablegroups = set()

ser = serial.Serial('/dev/ttyACM0', 115200)

while True:
    line = ser.readline()
    if line == '':
        break

    a = str(line).split(' ')
    pad = a[0][-1:]
    value = (~int(a[1][:-5])) & 0x7F

    if pad == '-':
        groups = set()
        for pad in touches:
            pads = ''
            i = 1
            value = touches[pad]
            while value > 0:
                if value & 1:
                    pads += str(i)
                value >>= 1
                i += 1
            if len(pads) > 1:
                groups.add(pads)
        if groups != oldgroups:
            oldgroups = groups
            groupstability = 0
        else:
            groupstability += 1
            if groupstability == 3 and laststablegroups != groups:
                laststablegroups = groups
                print(' '.join(groups))
        inhib = value
    else:
        value &= ~inhib
        value |= 1<<int(pad)
    touches[pad] = value
