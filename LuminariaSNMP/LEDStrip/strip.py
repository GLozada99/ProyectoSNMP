import RPi.GPIO as GPIO
import time
wait_time = 5
class LED_Strip:
    def __init__(self,red,green,blue,door):
        self.blue_flag = False      
        self.red = red
        self.green = green
        self.blue = blue
        self.door = door
        self.no_error_time = 0

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        GPIO.setup(self.red, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.green, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.blue, GPIO.OUT, initial=GPIO.LOW)   
        
        GPIO.setup(self.door, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # def start_pwm(self,freq=10000):
    #     self.pwm_r = GPIO.PWM(self.red,freq)
    #     self.pwm_g = GPIO.PWM(self.green,freq)
    #     self.pwm_b = GPIO.PWM(self.blue,freq)

    #     self.pwm_r.start(0)
    #     self.pwm_g.start(0)
    #     self.pwm_b.start(0)
    
    def change_status(self,value_r,value_g,value_b):
        GPIO.output(self.red,value_r)
        GPIO.output(self.green,value_g)
        GPIO.output(self.blue,value_b)
        # self.pwm_r.ChangeDutyCycle(value_r)
        # self.pwm_g.ChangeDutyCycle(value_g)
        # self.pwm_b.ChangeDutyCycle(value_b)
    
    def error(self):
        self.change_status(1,0,0)
        # self.pwm_r.ChangeDutyCycle(100)
        # self.pwm_g.ChangeDutyCycle(0)
        # self.pwm_b.ChangeDutyCycle(0)
        self.blue_flag = True
    
    def all_good(self):
        self.change_status(0,0,0)
        # self.pwm_r.ChangeDutyCycle(0)
        # self.pwm_g.ChangeDutyCycle(0)
        # self.pwm_b.ChangeDutyCycle(0)

        if self.blue_flag:      
            self.no_error_time = time.time()
            self.blue_flag = False
        
        if time.time() - self.no_error_time > wait_time:
            self.no_error_time = 0
            not_blue = True
        else:
            GPIO.output(self.blue,1)
            #self.pwm_b.ChangeDutyCycle(100)
            not_blue = False
        
        if self.door_open() and not_blue:
            self.white()
            # self.pwm_r.ChangeDutyCycle(100)
            # self.pwm_g.ChangeDutyCycle(100)
            # self.pwm_b.ChangeDutyCycle(100)

    
    def white(self):
        self.change_status(1,1,1)
        # self.pwm_r.ChangeDutyCycle(100)
        # self.pwm_g.ChangeDutyCycle(100)
        # self.pwm_b.ChangeDutyCycle(100)
    
    def off(self):
        self.change_status(0,0,0)
        # self.pwm_r.ChangeDutyCycle(0)
        # self.pwm_g.ChangeDutyCycle(0)
        # self.pwm_b.ChangeDutyCycle(0)
    
    def door_open(self):
        return not GPIO.input(self.door)

