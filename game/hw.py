#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# hw.py
#
# Copyright © 2017 Mathieu Gaborit (matael) <mathieu@matael.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Mathieu (matael) Gaborit wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#

"""
Hardware related classes
"""

import os
import sys
import logging


# add the submodule to the path (make sure submodules are initialized)
submodule_path = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../_submodules/laumio/python'
))
sys.path.append(submodule_path)
if os.path.exists(submodule_path):
    from laumio import Laumio
else:
    logging.critical('Please initialize submodules first')
    sys.exit(1)


class Pad(object):
    """Pad object holds the configuration of a pad (laumio + associated chord)"""

    def __init__(self, laumio_ip=None, color=None, notes=None):
        """ Constr.

        Either laumio_ip & color or notes must be provided
        """

        if laumio_ip is None and notes is None:
            raise RuntimeError('Either notes or laumio_ip/color must be provided')

        if color is not None and laumio_ip is not None:
            self.laumio = Laumio(laumio_ip)
            self.color = color
        else:
            self.laumio = None

        self.notes = notes
        if type(self.notes) == int:
            self.notes = [self.notes]

    def lighton(self):
        if self.laumio is not None:
            self.laumio.fillColor(*self.color)

    def lightoff(self):
        if self.laumio is not None:
            self.laumio.wipeOut()
