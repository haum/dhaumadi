#!/usr/bin/env python

import serial

inhib = 0
touches = {}
oldgroups = set()
groupstability = 0
laststablegroups = set()

ser = serial.Serial('/dev/ttyACM0', 115200)

groups_dict = {}

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
        # remove from dict all absent of the new groupset
        groups -= set(['1234567'])
        diff = set(groups_dict.keys())-groups
        for d in diff:
            groups_dict.pop(d)
            laststablegroups -= diff
        for g in groups:
            groups_dict[g] = groups_dict.get(g, 0) + 1
            if groups_dict[g] == 4 and g not in laststablegroups:
                laststablegroups.add(g)
                print(' '.join(groups))
        inhib = value
    else:
        value &= ~inhib
        value |= 1<<int(pad)
    touches[pad] = value
