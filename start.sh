#!/bin/sh
sleep 10
/usr/local/bin/python3.6 /home/pi/dhaumadi/dhaumadi.py | /usr/local/bin/python3.6 /home/pi/dhaumadi/game/game.py 2> /home/pi/dhaumadi/log.txt


