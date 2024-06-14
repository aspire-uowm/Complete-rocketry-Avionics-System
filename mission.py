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
def read_bmp280_data():
    i2c = board.I2C()
    return adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

#### mpu6050 ####

def read_mpu6050_data():    
    sensor = mpu6050(0x68)
    return sensor.get_accel_data()

#### Neo-6M ####

def read_gps_data():
    # Open serial port
    ser = serial.Serial('/dev/serial0', 9600, timeout=1)
    data = None

    while True:
        try:
            # Read a line of data from the GPS module
            line = ser.readline().decode('ascii', errors='replace')
            if line.startswith('$GPGGA'):
                data = parse_gpgga(line)
                break
        except KeyboardInterrupt:
            print("Stopping GPS reading")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue
    ser.close()

    return data

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

#### RH_Rfm69 ####

def init_rfm69():
    # Define the SPI bus
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

    # Define the CS (Chip Select) and RST (Reset) pins
    CS = digitalio.DigitalInOut(board.D5)  # Adjust if using a different pin
    RESET = digitalio.DigitalInOut(board.D25)  # Adjust if using a different pin

    # Initialize the RFM69 module
    return adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)  # Adjust frequency as needed

#### Main ####

if __name__ == "__main__":
    while True:
        sensor = read_bmp280_data()
        print('Temperature: {} degrees C'.format(sensor.temperature))
        print('Pressure: {}hPa'.format(sensor.pressure))

        accelerometer_data = read_mpu6050_data()
        print(accelerometer_data);

        gps_data = read_gps_data()
        print(gps_data)

        rfm69 = init_rfm69()
        # Print a confirmation message
        print("RFM69 initialized successfully!")

        # Send a test message
        message = "Hello, world!"
        rfm69.send(bytes(message, "utf-8"))  # Encode string to bytes
        print("Sent:", message)

        # encapsulate data and transmmit
        message = str(sensor.temperature) + ", " + str(sensor.pressure)
        rfm69.send(bytes(message, "utf-8"))  # Encode string to bytes
        print("Sent:", message)

        message = str(','.join(map(str,accelerometer_data.values()))) 
        rfm69.send(bytes(message, "utf-8"))  # Encode string to bytes
        print("Sent:", message)

        #TODO: test below string for real gps data
        message = str(','.join(map(str,gps_data.values())))
        rfm69.send(bytes(message, "utf-8"))  # Encode string to bytes
        print("Sent:", message)

        #tested for all above messages combined, cant be sent in a single packet excecpt if size is reduces somehow
        #decide on packet transmittion strategy, how many packets? retransmitions, packet Sync e.t.c.
        #message = str(sensor.temperature) + ", " + str(sensor.pressure) + ", " + str(','.join(map(str,accelerometer_data.values()))) + ", " + str(','.join(map(str,gps_data.values())))
        #print(len(message))
        #rfm69.send(bytes(message, "utf-8"))  # Encode string to bytes
        #print("Sent:", message)
