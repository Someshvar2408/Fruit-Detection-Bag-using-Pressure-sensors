import serial
import csv
import time

SERIAL_PORT = 'COM13'  # Change this to your Arduino's serial port
BAUD_RATE = 9600
OUTPUT_FILE = 'apple2.csv'

HEADERS = ["Timestamp", "ContactCount"] + \
          [f"Sensor{i+1}" for i in range(6)] + \
          ["WeightSensorAvg", "Weight"]



def parse_data(raw):
    parts = raw.split(',')
    data = {}
    current_key = None
    sensor_values = []

    for part in parts:
        if ':' in part:
            key, value = part.split(':', 1)
            key = key.strip()
            value = value.strip()
            if key == "Sensors":
                current_key = "Sensors"
                sensor_values = [value]  # Start collecting sensor values
            else:
                data[key] = value
                current_key = None
        else:
            if current_key == "Sensors":
                sensor_values.append(part.strip())

    if sensor_values:
        data["Sensors"] = sensor_values

    try:
        row = [time.strftime("%Y-%m-%d %H:%M:%S")]
        row.append(int(data.get("Contacts", -1)))
        row.extend(int(val) for val in data.get("Sensors", []))
        row.append(float(data.get("WeightSensor", 0.0)))
        row.append(float(data.get("Weight", 0.0)))
        return row
    except Exception as e:
        print("Parse error:", e)
        return None

def main():
    with open(OUTPUT_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)

    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
        time.sleep(2)  # Give time for Arduino reset
        while True:
            try:
                line = ser.readline().decode().strip()
                if line:
                    print("Received:", line)
                    row = parse_data(line)
                    if row:
                        with open(OUTPUT_FILE, mode='a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(row)
            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    main()
