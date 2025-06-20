from machine import Pin, PWM

class ServoControl:
    def __init__(self, pin_number=22):
        """
        Initialize servo control on specified pin
        :param pin_number: GPIO pin number (default: 22)
        """
        self.servo = PWM(Pin(pin_number))
        self.servo.freq(50)  # Standard 50Hz frequency for servos
        self._current_angle = 90  # Start at middle position
        self.set_angle(90)  # Initialize at middle position
        
    def _map_angle_to_duty(self, angle):
        """
        Convert angle (0-180) to duty cycle (20-120)
        MG996R typically needs pulse width between 0.5ms - 2.5ms
        At 50Hz, that's about 2.5% - 12.5% duty cycle
        """
        # Ensure angle is within bounds
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
            
        # Map 0-180 degrees to duty cycle (20-120)
        # 20 (~0.5ms) for 0 degrees
        # 120 (~2.5ms) for 180 degrees
        return int(((angle / 180) * 100) + 20)
    
    def set_angle(self, angle):
        """
        Set servo to specified angle
        :param angle: Angle in degrees (0-180)
        """
        duty = self._map_angle_to_duty(angle)
        self.servo.duty(duty)
        self._current_angle = angle
        
    def get_current_angle(self):
        """
        Get current servo angle
        :return: Current angle in degrees
        """
        return self._current_angle
    
    def center(self):
        """
        Move servo to center position (90 degrees)
        """
        self.set_angle(90)
        
    def min_position(self):
        """
        Move servo to minimum position (0 degrees)
        """
        self.set_angle(0)
        
    def max_position(self):
        """
        Move servo to maximum position (180 degrees)
        """
        self.set_angle(180)
        
    def turn_left(self, degrees=10):
        """
        Gira el servo a la izquierda (reduce el ángulo) la cantidad de grados especificada.
        Si no se especifica, usa 10 grados.
        """
        new_angle = self._current_angle - degrees
        if new_angle < 0:
            new_angle = 0
        self.set_angle(new_angle)

    def turn_right(self, degrees=10):
        """
        Gira el servo a la derecha (aumenta el ángulo) la cantidad de grados especificada.
        Si no se especifica, usa 10 grados.
        """
        new_angle = self._current_angle + degrees
        if new_angle > 180:
            new_angle = 180
        self.set_angle(new_angle)