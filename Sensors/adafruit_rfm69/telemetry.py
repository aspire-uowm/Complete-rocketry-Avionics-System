import board
import busio
import digitalio
import adafruit_rfm69

import time

# Define the SPI bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Define the CS (Chip Select) and RST (Reset) pins
CS = digitalio.DigitalInOut(board.D5)  # Adjust if using a different pin
RESET = digitalio.DigitalInOut(board.D25)  # Adjust if using a different pin

# Initialize the RFM69 module
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)  # Adjust frequency as needed

# Print a confirmation message
print("RFM69 initialized successfully!")

# Send a test message
message = "Hello, world!"

while True:
    rfm69.send(bytes(message, "utf-8"))  # Encode string to bytes
    print("Sent:", message)
    time.sleep(1)
