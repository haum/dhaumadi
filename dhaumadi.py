#!/usr/bin/env python

import serial

inhib = 0
touches = {}

ser = serial.Serial('/dev/ttyACM0', 115200)
while True:
    line = ser.readline()
    if line == '':
        break

    a = str(line).split(' ')
    pad = a[0][-1:]
    value = (~int(a[1][:-5])) & 0x7F

    if pad == '-':
        inhib = value
    else:
        value &= ~inhib
        value |= 1<<int(pad)

    if not pad in touches or touches[pad][0] != value:
        touches[pad] = [value, 0]
    elif touches[pad][1] == 0:
        print((pad, value))
        touches[pad][1] = 1
