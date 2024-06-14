# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Wiring Check, Pi Radio w/RFM69

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
#Import the RFM69 radio module.
import adafruit_rfm69

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Configure RFM69 LoRa Radio
CS = DigitalInOut(board.D5)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

while True:
    rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 433.0)
    print("f")
