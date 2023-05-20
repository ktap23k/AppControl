from dcmotor import DCMotor       
from machine import Pin, PWM   
from time import sleep

def motor(pin1, pin2, enable):
    pin1 = Pin(pin1, Pin.OUT)    
    pin2 = Pin(pin2, Pin.OUT)      
    dc_motor = DCMotor(pin1, pin2, enable)
    dc_motor = DCMotor(pin1, pin2, enable, 350, 1023)
    return dc_motor

enable = PWM(Pin(5), 15000)
motor2 = motor(26, 27, enable)
motor1 = motor(25, 22, enable)

motor3 = motor(18, 4, enable)
motor4 = motor(19, 21, enable)

def forward(speed):
    motor1.forward(speed)
    motor2.forward(speed)
    motor3.forward(speed)
    motor4.forward(speed)

def backwards(speed):
    motor1.backwards(speed)
    motor2.backwards(speed)
    motor3.backwards(speed)
    motor4.backwards(speed)

def l_forward(speed):
    motor1.forward(speed//4)
    motor2.forward(speed//4)
    motor3.forward(speed)
    motor4.forward(speed)

def r_forward(speed):
    motor3.forward(speed//4)
    motor4.forward(speed//4)
    motor1.forward(speed)
    motor2.forward(speed)

def l_backwards(speed):
    motor1.backwards(speed//4)
    motor2.backwards(speed//4)
    motor3.backwards(speed)
    motor4.backwards(speed)
    
def r_backwards(speed):
    motor3.backwards(speed//4)
    motor4.backwards(speed//4)
    motor1.backwards(speed)
    motor2.backwards(speed)
    
def left(speed):
    motor1.stop()
    motor2.stop()
    motor3.forward(speed)
    motor4.forward(speed)

def right(speed):
    motor3.stop()
    motor4.stop()
    motor1.forward(speed)
    motor2.forward(speed)

def left_(speed):
    motor1.stop()
    motor2.stop()
    motor3.backwards(speed)
    motor4.backwards(speed)
    
def right_(speed):
    motor3.stop()
    motor4.stop()
    motor1.backwards(speed)
    motor2.backwards(speed)
    
def to_left(speed):
    pass

def to_right(speed):
    pass
