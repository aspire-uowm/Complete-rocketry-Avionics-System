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
import digitalio
import board
#Import the RFM69 radio module.
import adafruit_rfm69

def init_rfm69_i2c():
    # Create the I2C interface.
    i2c = busio.I2C(board.SCL, board.SDA)

    # Define the CS (Chip Select) and RST (Reset) pins
    CS = digitalio.DigitalInOut(board.D5)  # Adjust if using a different pin
    RESET = digitalio.DigitalInOut(board.D25)  # Adjust if using a different pin

    # Initialize the RFM69 module
    return adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)  # Adjust frequency as needed

def init_rfm69_spi():
    # Define the SPI bus
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

    # Define the CS (Chip Select) and RST (Reset) pins
    CS = digitalio.DigitalInOut(board.D5)  # Adjust if using a different pin
    RESET = digitalio.DigitalInOut(board.D25)  # Adjust if using a different pin

    # Initialize the RFM69 module
    return adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)  # Adjust frequency as needed
