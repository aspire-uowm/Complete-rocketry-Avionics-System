# main source 

import board

import adafruit_bmp280
from mpu6050 import mpu6050
from Sensors.Neo_6m.Gps import read_gps_data
from Sensors.adafruit_rfm69.rfm69 import init_rfm69_spi

if __name__ == "__main__":
    i2c = board.I2C()
    mpu = mpu6050(0x68)

    while True:
        bmp_data = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        print('Temperature: {} degrees C'.format(bmp_data.temperature))
        print('Pressure: {}hPa'.format(bmp_data.pressure))

        accelerometer_data = mpu.get_accel_data()
        print(accelerometer_data);

        gps_data = read_gps_data()
        print(gps_data)

        rfm69 = init_rfm69_spi()
        # Print a confirmation message
        print("RFM69 initialized successfully!")

        # Send a test message
        message = "Hello, world!"
        rfm69.send(bytes(message, "utf-8"))  # Encode string to bytes
        print("Sent:", message)

        # encapsulate data and transmmit
        message = str(bmp_data.temperature) + ", " + str(bmp_data.pressure)
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
        #message = str(bmp_data.temperature) + ", " + str(bmp_data.pressure) + ", " + str(','.join(map(str,accelerometer_data.values()))) + ", " + str(','.join(map(str,gps_data.values())))
        #print(len(message))
        #rfm69.send(bytes(message, "utf-8"))  # Encode string to bytes
        #print("Sent:", message)
