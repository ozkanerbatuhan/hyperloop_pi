import RPi.GPIO as GPIO
import time

# GPIO setup
motor_pin = 16
close_brake_pin = 18
open_brake_pin = 23
levitation_pin = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pin, GPIO.OUT)
GPIO.setup(close_brake_pin, GPIO.OUT)
GPIO.setup(open_brake_pin, GPIO.OUT)
GPIO.setup(levitation_pin, GPIO.OUT)

# Initial states
motor_running = False
brake_closed = False
brake_opened = False

def run_motor(state):
    global motor_running, brake_closed, brake_opened
    if not brake_closed and not brake_opened:
        GPIO.output(motor_pin, GPIO.HIGH if state else GPIO.LOW)
        motor_running = state
        print(f"Motor {'running' if state else 'stopped'}")

def close_brake(state):
    global brake_closed, motor_running
    if state:
        brake_closed = True
        motor_running = False
        GPIO.output(motor_pin, GPIO.LOW)
        GPIO.output(close_brake_pin, GPIO.HIGH)
        GPIO.output(open_brake_pin, GPIO.LOW)
        print("Brake closed, motor stopped")
    else:
        brake_closed = False
        GPIO.output(close_brake_pin, GPIO.LOW)
        print("Brake already open or cannot close")

def open_brake(state):
    global brake_closed, brake_opened
    if state:
        brake_closed = False
        brake_opened = True
        GPIO.output(close_brake_pin, GPIO.LOW)
        GPIO.output(open_brake_pin, GPIO.HIGH)
        print("Brake opened")
    else:
        brake_opened = False
        GPIO.output(open_brake_pin, GPIO.LOW)
        print("Brake already closed or cannot open")

def run_levitation(state):
    GPIO.output(levitation_pin, GPIO.HIGH if state else GPIO.LOW)
    print(f"Levitation {'running' if state else 'stopped'}")
