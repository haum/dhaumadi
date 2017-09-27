#! /usr/bin/env python3
# -*- coding:utf8 -*-
#
# leds.py
#
# Copyright © 2017 HAUM <contact@haum.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# jblb wrote parts of this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#

from neopixel import *  # works from https://github.com/jgarff/rpi_ws281x

# LED strip configuration:
LED_COUNT      = 7       # Number of LED pixels.
LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 50      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering


class Leds:
    """ LEDs direct connection abstraction layer """

    def __init__(self):
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    def setPixelColor(self, pixel, r, g, b):
        """ Set the color of all the leds pixel of the Leds strip
        pixel -- LED ID (0~xxx)
        r -- red byte
        g -- green byte
        b -- blue byte
        """
        self.strip.setPixelColor(pixel, Color(r, g, b))
        self.strip.show()
