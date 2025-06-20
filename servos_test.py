import time
from servos import ServoControl

servo = ServoControl()

print("Posición inicial (centro):", servo.get_current_angle())

# Mover dos veces a la derecha
servo.turn_right(50)
print("Derecha 1:", servo.get_current_angle())
time.sleep(1)

servo.turn_right(50)
print("Derecha 2:", servo.get_current_angle())
time.sleep(1)

# Mover dos veces a la izquierda
servo.turn_left(50)
print("Izquierda 1:", servo.get_current_angle())
time.sleep(1)

servo.turn_left(50)
print("Izquierda 2:", servo.get_current_angle())
time.sleep(1)
servo.turn_right(50)
print("Derecha 1:", servo.get_current_angle())
time.sleep(1)

servo.turn_right(50)
print("Derecha 2:", servo.get_current_angle())
time.sleep(1)

# Mover dos veces a la izquierda
servo.turn_left(50)
print("Izquierda 1:", servo.get_current_angle())
time.sleep(1)

servo.turn_left(50)
print("Izquierda 2:", servo.get_current_angle())

servo.turn_right(50)
print("Derecha 1:", servo.get_current_angle())
time.sleep(1)

servo.turn_right(50)
print("Derecha 2:", servo.get_current_angle())
time.sleep(1)

# Mover dos veces a la izquierda
servo.turn_left(50)
print("Izquierda 1:", servo.get_current_angle())
time.sleep(1)

servo.turn_left(50)
print("Izquierda 2:", servo.get_current_angle())


print("Prueba finalizada. Ángulo actual:", servo.get_current_angle())
