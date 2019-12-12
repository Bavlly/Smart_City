#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

"""
main.py - main entry RFID demo program
scans key/card tags and when valid card, turns RGBLed green, else red.

@History:
2019-0910 OOP version, using pyscan_board specification

See https://docs.pycom.io for more information regarding library specifics
"""
from lopy4_board import *
import pyscan_board as board
from appnfc import AppNFC

import binascii
import time
import pycom
import _thread


DEBUG = False  # 2019-0910 changed, True to see debug messages
USE_RFID = True  # 2019-1025 added


if __name__ == '__main__':
    print('RFID demo started... {}'.format(USE_RFID))
    if USE_RFID:
        app = AppNFC()
        # This is the start of our main execution... start the thread
        _thread.start_new_thread(app.discovery_loop, ())

        time.sleep(1)
        # _thread.start_new_thread(app.send_sensor_data, ('Thread 2', 10))
    else:
        pycom.heartbeat(True)