import serial
import json

def read_serial_data(port='/dev/serial0', baudrate=9600, timeout=1):
    # Seri portu aç
    ser = serial.Serial(port, baudrate, timeout=timeout)
    ser.flush()

    while True:
        if ser.in_waiting > 0:
            try:
                # Veriyi oku
                line = ser.readline().decode('utf-8').rstrip()
                # Veriyi JSON olarak parse et
                data = json.loads(line)
                validated_data = {}
                for key, value in data.items():
                    if isinstance(key, str) and isinstance(value, (int, float, str)):
                        validated_data[key] = value
                    else:
                        validated_data[key] = ""

                # Dogrulanmis veriyi yazdir
                print(validated_data)

            except (json.JSONDecodeError, ValueError) as e:
                # JSON parse hatasi veya baska bir hata durumunda
                print(f"Veri hatasi: {e}")
                continue
        else:
            return 


