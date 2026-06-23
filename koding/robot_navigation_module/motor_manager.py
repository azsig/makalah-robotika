import RPi.GPIO as GPIO

class MotorManager:
    def __init__(self, ena=13, in1=19, in2=26, enb=12, in3=16, in4=20, max_speed_limit=150, left_bias=1.0):
        # BCM Pin Configuration
        self.ENA = ena  # PWM Left
        self.IN1 = in1  # Dir 1 Left
        self.IN2 = in2  # Dir 2 Left
        
        self.ENB = enb  # PWM Right
        self.IN3 = in3  # Dir 1 Right
        self.IN4 = in4  # Dir 2 Right
        
        self.max_speed_limit = max_speed_limit
        self.left_bias = left_bias
        
        # Setup Pins
        GPIO.setmode(GPIO.BCM)
        for pin in [self.ENA, self.IN1, self.IN2, self.ENB, self.IN3, self.IN4]:
            GPIO.setup(pin, GPIO.OUT)
            
        # Setup PWM
        self.pwm_left = GPIO.PWM(self.ENA, 1000)  # 1kHz frequency
        self.pwm_right = GPIO.PWM(self.ENB, 1000)
        
        self.pwm_left.start(0)
        self.pwm_right.start(0)

    def set_motors(self, speed_left, speed_right):
        """
        Set speed for both motors. 
        speed range: -255 to 255 (negative for reverse)
        """
        # Terapkan bias untuk motor kiri
        speed_left = speed_left * self.left_bias

        # Batasi kecepatan secara proporsional agar rasio kemudi tetap terjaga
        # Gunakan max_speed_limit sebagai plafon absolut
        abs_l = abs(speed_left)
        abs_r = abs(speed_right)
        max_val = max(abs_l, abs_r)
        
        if max_val > self.max_speed_limit:
            ratio = self.max_speed_limit / max_val
            speed_left *= ratio
            speed_right *= ratio
        # --- Left Motor ---
        if speed_left >= 0:
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
        else:
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            speed_left = abs(speed_left)
            
        # Convert 0-255 to 0-100% duty cycle
        duty_left = (speed_left / 255.0) * 100
        self.pwm_left.ChangeDutyCycle(min(duty_left, 100))
        
        # --- Right Motor ---
        if speed_right >= 0:
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
        else:
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            speed_right = abs(speed_right)
            
        duty_right = (speed_right / 255.0) * 100
        self.pwm_right.ChangeDutyCycle(min(duty_right, 100))
        
        # Log duty cycle untuk debugging
        # print(f"[DEBUG Motor] Speed L: {speed_left:.1f} (Duty: {duty_left:.1f}%) | Speed R: {speed_right:.1f} (Duty: {duty_right:.1f}%)")

    def stop(self):
        self.pwm_left.ChangeDutyCycle(0)
        self.pwm_right.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def cleanup(self):
        self.stop()
        self.pwm_left.stop()
        self.pwm_right.stop()
        self.pwm_left = None
        self.pwm_right = None
