from lopy4_board import *
import pyscan_board as board
import urequests
import json

import binascii
import time
import pycom
import _thread

DEBUG = False  # 2019-0910 changed, True to see debug messages
USE_RFID = True  # 2019-1025 added

RGB_BRIGHTNESS = 0x8
RGB_RED = (RGB_BRIGHTNESS << 16)
RGB_GREEN = (RGB_BRIGHTNESS << 8)
RGB_BLUE = (RGB_BRIGHTNESS)

class AppNFC:

    def __init__(self):
        # shortcuts to avoid much editing
        self.py = board.py
        self.nfc = board.nfc
        self.lt = board.lt
        self.li = board.li
        # Make sure heartbeat is disabled before setting RGB LED
        pycom.heartbeat(False)
        # Initialise the MFRC630 with some settings
        self.nfc.mfrc630_cmd_init()

    @property
    def VALID_CARDS(self):
        # 2019-0910 added my valid card ID's
        return [[0x43, 0x95, 0xDD, 0xF8],
                [0x43, 0x95, 0xDD, 0xF9],
                [0xD7, 0x47, 0x80, 0x34]]
                
    def check_uid(self, uid, len):
        return self.VALID_CARDS.count(uid[:len])

    def print_debug(self, msg):
        if DEBUG:
            print(msg)

    # 2019-0910 added some useful text to print
    def send_sensor_data(self, name, timeout):
        while(True):
            print('Lightsensor: {}'.format(self.lt.light()))  # 2019-0715 changed
            print('Accelerometer: {}'.format(self.li.acceleration()))  # 2019-0715 changd
            time.sleep(timeout)

    def send_data():
        sensor_data = {
        "cardID": "sensor",
        "authorised": 'true',
        }
        print(sensor_data)    
        r = urequests.post('http://172.20.10.2:8080/sensor/post/', json=sensor_data)
        r.close()

    def discovery_loop(self):
        while True:
            app = AppNFC()
            nfc = app.nfc
            # Send REQA for ISO14443A card type
            self.print_debug('Sending REQA for ISO14443A card type...')
            atqa = nfc.mfrc630_iso14443a_WUPA_REQA(nfc.MFRC630_ISO14443_CMD_REQA)
            self.print_debug('Response: {}'.format(atqa))

            if (atqa != 0):
                # A card has been detected, read UID
                self.print_debug('A card has been detected, read UID...')
                uid = bytearray(10)
                uid_len = nfc.mfrc630_iso14443a_select(uid)
                self.print_debug('UID has length: {}'.format(uid_len))
                if (uid_len > 0):
                    self.print_debug('Checking if card with UID: [{:s}] is listed in VALID_CARDS...'.format(binascii.hexlify(uid[:uid_len],' ').upper()))
                    if (self.check_uid(list(uid), uid_len)) > 0:
                        self.print_debug('Card is listed, turn LED green')
                        print('Authorized access detected [{:s}]'.format(binascii.hexlify(uid[:uid_len], ' ').upper()))
                        pycom.rgbled(RGB_GREEN)
                        sensor = binascii.hexlify(uid[:uid_len], ' ').upper()
                        sensor_data = {
                        "cardID": sensor,
                        "authorised": 'true',
                        }
                        r = urequests.post('http://172.20.10.2:8080/sensor/post/', json=sensor_data)
                        r.close()
                        print("posted in database!")
                    else:
                        self.print_debug('Card is not listed, turn LED red')
                        print('Alarm!! No authorized access detected by card [{:s}]'.format(binascii.hexlify(uid[:uid_len],' ').upper()))
                        pycom.rgbled(RGB_RED)
                        sensor = binascii.hexlify(uid[:uid_len], ' ').upper()
                        sensor_data = {
                        "cardID": sensor,
                        "authorised": 'false',
                        }
                        r = urequests.post('http://172.20.10.2:8080/sensor/post/', json=sensor_data)
                        r.close()
                        print("posted in database!")

            else:
                # No card detected
                self.print_debug('Did not detect any card...')
                pycom.rgbled(RGB_BLUE)

            nfc.mfrc630_cmd_reset()
            time.sleep(2)
            nfc.mfrc630_cmd_init()