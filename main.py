import socketio
import RPi.GPIO as GPIO
import time
import json
import gpio_control
from mpu6050_sensor import read_mpu6050_data
from serial_data import read_serial_data

# Create a Socket.IO client
sio = socketio.Client(reconnection=True, reconnection_attempts=0, reconnection_delay=1, reconnection_delay_max=5)

@sio.event
def connect():
    print("Connection established")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.event
def connected(data):
    sio.emit("train", data)

@sio.event
def ready(data):
    print("ready", data)
    gpio_control.run_levitation(data)

@sio.event
def start(data):
    print("start", data)
    gpio_control.run_motor(data)

@sio.event
def stop(data):
    print("stop", data)
    if data:
        gpio_control.run_motor(False)
        gpio_control.close_brake(True)
    else:
        gpio_control.close_brake(False)

@sio.event
def break_event(data):
    if data:
        gpio_control.close_brake(True)
        time.sleep(5)
        gpio_control.close_brake(False)
        gpio_control.open_brake(True)
        time.sleep(1)
    else:
        gpio_control.close_brake(False)
        gpio_control.open_brake(False)

@sio.event
def emergency(data):
    print("emergency", data)
    if data:
        gpio_control.run_motor(False)
        gpio_control.close_brake(True)
    else:
        print("Emergency cancel")

@sio.event
def connect_error(err):
    print("Connection error:", err)

def try_connect(url):
    try:
        print(f"Attempting to connect to {url}")
        sio.connect(url, wait_timeout=5)
        return True
    except Exception as e:
        print(f"Failed to connect to {url}: {e}")
        return False

def continuous_connect():
    urls = [
        'http://192.168.1.89:3030',
        'http://192.168.178.207:3030',
        'http://192.168.1.67:3030',
        'http://127.0.0.1:3030'
    ]
    while True:
        for url in urls:
            if try_connect(url):
                return
        print("Couldn't connect to any URL. Trying again in 2 seconds...")
        time.sleep(2)

def getAllData():
    while True:
        if sio.connected:
            accelerometer_data, gyroscope_data, temperature = read_mpu6050_data()
            sensorsData = (accelerometer_data, gyroscope_data, temperature)
            if sensorsData:
                print(accelerometer_data, gyroscope_data, temperature)
                data_to_send = {
                    "accelerometer": accelerometer_data,
                    "gyroscope": gyroscope_data,
                    "temperature": temperature
                }
                json_data = json.dumps(data_to_send)
                sio.emit("acceleration", json_data)
            else:
                print("Failed to read accelerometer data.")
            
            serialData = read_serial_data()
        time.sleep(0.5)

def main():
    while True:
        try:
            continuous_connect()
            sio.start_background_task(getAllData)
            sio.wait()
        except socketio.exceptions.ConnectionError as e:
            print(f"Connection lost: {e}. Attempting to reconnect...")
            time.sleep(5)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted by user")
    finally:
        sio.disconnect()
        GPIO.cleanup()
