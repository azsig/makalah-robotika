import RPi.GPIO as GPIO
import time

class L298NRobot:
    def __init__(self):
        # Motor A (Left)
        self.ENA = 12
        self.IN1 = 20
        self.IN2 = 21
        # Motor B (Right)
        self.ENB = 13
        self.IN3 = 19
        self.IN4 = 26

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        pins = [self.ENA, self.IN1, self.IN2,
                self.ENB, self.IN3, self.IN4]
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)

        self.pwm_a = GPIO.PWM(self.ENA, 1000)
        self.pwm_b = GPIO.PWM(self.ENB, 1000)
        self.pwm_a.start(0)
        self.pwm_b.start(0)

    def _set_motor_a(self, speed, forward=True):
        if forward:
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
        else:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
        self.pwm_a.ChangeDutyCycle(abs(speed))

    def _set_motor_b(self, speed, forward=True):
        if forward:
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
        else:
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_b.ChangeDutyCycle(abs(speed))

    def forward(self, speed=75):
        self._set_motor_a(speed, forward=True)
        self._set_motor_b(speed, forward=True)

    def backward(self, speed=75):
        self._set_motor_a(speed, forward=False)
        self._set_motor_b(speed, forward=False)

    def turn_left(self, speed=60):
        self._set_motor_a(speed, forward=False)  # Left motor back
        self._set_motor_b(speed, forward=True)   # Right motor forward

    def turn_right(self, speed=60):
        self._set_motor_a(speed, forward=True)
        self._set_motor_b(speed, forward=False)

    def stop(self):
        self.pwm_a.ChangeDutyCycle(0)
        self.pwm_b.ChangeDutyCycle(0)

    def cleanup(self):
        self.stop()
        self.pwm_a.stop()
        self.pwm_b.stop()
        self.pwm_a = None
        self.pwm_b = None
        GPIO.cleanup()

robot = L298NRobot()
try:
    robot.forward(speed=80)
    time.sleep(2)
    robot.turn_left(speed=65)
    time.sleep(0.8)
    robot.forward(speed=80)
    time.sleep(2)
    robot.stop()
finally:
    robot.cleanup()