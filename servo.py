# servo.py
# Control de servomotor 360° para ESP32 con MicroPython
from machine import Pin, PWM
import time

class Servo360:
    def __init__(self, pin, freq=50):
        self.pwm = PWM(Pin(pin), freq=freq)
        self.stop()

    def left(self, speed=80):
        # Ajusta el duty para tu servo
        self.pwm.duty(int(40 + speed))

    def right(self, speed=80):
        self.pwm.duty(int(115 - speed))

    def stop(self):
        self.pwm.duty(77)  # Neutral (ajusta según tu servo)
