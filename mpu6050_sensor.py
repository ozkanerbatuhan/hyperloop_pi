from mpu6050 import mpu6050
import time

def read_mpu6050_data(sensor_address=0x68, retries=5, delay=0.5):
    try:
        sensor = mpu6050(sensor_address)
    except Exception as e:
        print(f"Error initializing MPU6050: {e}")
        return None

    for attempt in range(retries):
        try:
            accelerometer_data = sensor.get_accel_data()
            gyroscope_data = sensor.get_gyro_data()
            temperature = sensor.get_temp()
            return accelerometer_data, gyroscope_data, temperature
        except OSError as e:
            print(f"I/O error on attempt {attempt + 1}: {e}")
        except Exception as e:
            print(f"Unexpected error on attempt {attempt + 1}: {e}")
        time.sleep(delay)

    print("Failed to read from MPU6050 after multiple attempts.")
    return None
