# main source 

import serial
import time

import board
import busio
import digitalio

import adafruit_bmp280
import adafruit_rfm69
from mpu6050 import mpu6050


####  bmp280  ####
def init_bmp280():
    i2c = board.I2C()
    sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

    print('Temperature: {} degrees C'.format(sensor.temperature))
    print('Pressure: {}hPa'.format(sensor.pressure))


#### RH_Rfm69 ####

def init_rfm69():
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

    #while True:
    rfm69.send(bytes(message, "utf-8"))  # Encode string to bytes
    print("Sent:", message)


#### mpu6050 ####

def init_mpu6050():    
    sensor = mpu6050(0x68)

    accelerometer_data = sensor.get_accel_data()

    print(accelerometer_data);


#### Neo-6M ####

def read_gps_data():
    # Open serial port
    ser = serial.Serial('/dev/serial0', 9600, timeout=1)

    while True:
        try:
            # Read a line of data from the GPS module
            line = ser.readline().decode('ascii', errors='replace')
            if line.startswith('$GPGGA'):
                print(parse_gpgga(line))
        except KeyboardInterrupt:
            print("Stopping GPS reading")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue
    ser.close()

def parse_gpgga(data):
    parts = data.split(',')
    if len(parts) < 15:
        return "Incomplete GPGGA data"

    time_utc = parts[1]
    latitude = convert_to_degrees(parts[2])
    lat_direction = parts[3]
    longitude = convert_to_degrees(parts[4])
    lon_direction = parts[5]
    fix_quality = parts[6]
    num_satellites = parts[7]
    altitude = parts[9]

    return {
        "Time (UTC)": time_utc,
        "Latitude": f"{latitude} {lat_direction}",
        "Longitude": f"{longitude} {lon_direction}",
        "Fix Quality": fix_quality,
        "Number of Satellites": num_satellites,
        "Altitude": f"{altitude} M"
    }

def convert_to_degrees(raw_value):
    if raw_value == "":
        return None
    try:
        # Convert raw value to float
        raw_value = float(raw_value)
        # Extract degrees and minutes
        degrees = int(raw_value / 100)
        minutes = raw_value - (degrees * 100)
        return degrees + (minutes / 60)
    except ValueError:
        return None

#### Main ####

if __name__ == "__main__":
    init_bmp280()
    init_rfm69()
    init_mpu6050()
    read_gps_data()
