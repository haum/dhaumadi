#!/usr/bin/env python3

import sys
import serial
from collections import defaultdict

inhib = 0
touches = {}
oldgroups = set()
groupstability = 0
laststablegroups = set()
debounce = defaultdict(lambda: [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]])

ser = serial.Serial('/dev/ttyACM0', 115200)

while True:
  line = ser.readline()
  if line == '':
    break
  if len(line) < 5:
    continue

  # Decode values
  a = str(line).split(' ')
  pad = a[0][-1:]
  nb = (~int(a[1][:-5])) & 0x7F
  values = []
  while nb:
    values.append(nb & 1)
    nb >>= 1
  values = (values + [0] * 7)[:7]

  # Debounce
  debounce_max = 6
  for i, v in enumerate(values):
    debounce[pad][i][0] += v * 2 - 1
    if debounce[pad][i][0] > debounce_max:
      debounce[pad][i][0] = debounce_max
      debounce[pad][i][1] = 1
    elif debounce[pad][i][0] < 0:
      debounce[pad][i][0] = 0
      debounce[pad][i][1] = 0
  value = sum(1<<i for i, j in enumerate(debounce[pad]) if j[1] == 1)

  # Compute groups
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
        sys.stdout.flush()
    inhib = value
  else:
    value &= ~inhib
    value |= 1<<int(pad)
  touches[pad] = value
