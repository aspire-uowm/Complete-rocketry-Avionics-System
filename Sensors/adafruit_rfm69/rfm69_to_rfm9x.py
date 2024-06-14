import time
import busio
import digitalio
import board
import adafruit_rfm69

# Create the I2C interface.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Configure RFM69HCW CS and reset pins
cs = digitalio.DigitalInOut(board.D5)
reset = digitalio.DigitalInOut(board.D6)

# Initialize RFM69 radio
rfm69 = adafruit_rfm69.RFM69(spi, cs, reset, 433.0)  # 915 MHz frequency

# Send data
while True:
    rfm69.send(bytes("Hello from RFM69!", "utf-8"))
    print("Sent data!")
    time.sleep(2)
