import serial
import time

def read_gps_data():
    # Open serial port
    ser = serial.Serial('/dev/serial0', 9600, timeout=1)
    data = None

    try:
        while data is None:
            # Read a line of data from the GPS module
            line = ser.readline().decode('ascii', errors='replace')
            if line.startswith('$GPGGA'):
                data = parse_gpgga(line)
            else:
                time.sleep(1)  # Delay before trying again
    except Exception as e:
        print(f"Error: {e}")
    finally:
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

if __name__ == "__main__":
    print("Reading GPS data...")
    gps_data = read_gps_data()
    if gps_data:
        print(gps_data)
    else:
        print("No GPS data received")
