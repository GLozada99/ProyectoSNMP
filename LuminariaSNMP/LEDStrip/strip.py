import RPi.GPIO as GPIO
import time
class LED_Strip:
    wait_time = 30
    def __init__(self,red,green,blue):
        self.blue_flag = False      
        self.red = red
        self.green = green
        self.blue = blue
        self.no_error_time = 0

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        GPIO.setup(self.red, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.green, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.blue, GPIO.OUT, initial=GPIO.LOW)      

    def start_pwm(self,freq):
        self.pwm_r = GPIO.PWM(self.red,freq)
        self.pwm_g = GPIO.PWM(self.green,freq)
        self.pwm_b = GPIO.PWM(self.blue,freq)

        self.pwm_r.start(0)
        self.pwm_g.start(0)
        self.pwm_b.start(0)
    
    def change_duty(self,value_r,value_g,value_b):
        self.pwm_r.ChangeDutyCycle(value_r)
        self.pwm_g.ChangeDutyCycle(value_g)
        self.pwm_b.ChangeDutyCycle(value_b)
    
    def error(self):
        self.pwm_r.ChangeDutyCycle(100)
        self.pwm_g.ChangeDutyCycle(0)
        self.pwm_b.ChangeDutyCycle(0)
        self.blue_flag = True
    
    def all_good(self):
        self.pwm_r.ChangeDutyCycle(0)
        self.pwm_g.ChangeDutyCycle(0)
        if self.blue_flag:        
            self.no_error_time = time.time()
            self.blue_flag = False
        
        if time.time() - self.no_error_time > 30:
            self.no_error_time = 0
            duty_blue = 0
        else:
            duty_blue = 100

        self.pwm_b.ChangeDutyCycle(duty_blue)
    
    def white(self):
        self.pwm_r.ChangeDutyCycle(100)
        self.pwm_g.ChangeDutyCycle(100)
        self.pwm_b.ChangeDutyCycle(100)
    
    def off(self):
        self.pwm_r.ChangeDutyCycle(0)
        self.pwm_g.ChangeDutyCycle(0)
        self.pwm_b.ChangeDutyCycle(0)

