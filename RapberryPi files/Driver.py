import RPi.GPIO as GPIO
from time import sleep

class Driver(object):
    def __init__(self):
        
        self.in1 = 23
        self.in2 = 24
        self.ena = 27
        self.in3 = 6
        self.in4 = 5
        self.enb = 26
        self.standby = 22
        self.servo = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.ena, GPIO.OUT)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)
        GPIO.setup(self.enb, GPIO.OUT)
        GPIO.setup(self.standby, GPIO.OUT)
        GPIO.setup(self.servo, GPIO.OUT)
        self.p1 = GPIO.PWM(self.ena, 1000)
        self.p2 = GPIO.PWM(self.enb, 1000)
        self.steer = GPIO.PWM(self.servo, 50)
        self.p1.start(25)
        self.p2.start(25)
        self.steer.start(90)
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)
    def drive(self, throttle, speed, angle):
        print("Angle:", angle)
        if throttle == 1:
            GPIO.output(self.standby, GPIO.HIGH)
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)
            GPIO.output(self.in3, GPIO.HIGH)
            GPIO.output(self.in4, GPIO.LOW)
            print("Forward")
            
        elif throttle == 2:
            GPIO.output(self.standby, GPIO.HIGH)
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.HIGH)
            GPIO.output(self.in3, GPIO.LOW)
            GPIO.output(self.in4, GPIO.HIGH)
        
        elif throttle == 0:
            GPIO.output(self.standby, GPIO.LOW)
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.LOW)
            GPIO.output(self.in3, GPIO.LOW)
            GPIO.output(self.in4, GPIO.LOW)
        
        self.p1.ChangeDutyCycle(speed)
        self.p2.ChangeDutyCycle(speed)
        if angle <= 60:
            angle = 60
        elif angle >= 130:
            angle = 130
        angle = 2+(angle/18)
        self.steer.ChangeDutyCycle(angle)
    
    def clean(self):
        GPIO.cleanup()
        

        