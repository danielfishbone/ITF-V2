import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
class Motor():
        def __init__(self,en,in1,in2):
                self.en  = en
                self.in1 = in1
                self.in2 = in2
                gpio.setup(self.en,gpio.OUT)
                gpio.setup(self.in1,gpio.OUT)
                gpio.setup(self.in2,gpio.OUT)
                self.pwm =gpio.PWM(self.en,100)
                self.pwm.start(0)

        def move(self,direction=0,speed=0):
                # speed *= 100
                if (direction<0):
                        gpio.output(self.in1,gpio.LOW)
                        gpio.output(self.in2,gpio.HIGH)
                elif(direction>0):
                        gpio.output(self.in1,gpio.HIGH)
                        gpio.output(self.in2,gpio.LOW)
                else:
                        gpio.output(self.in2,gpio.LOW)
                        gpio.output(self.in1,gpio.LOW)
                self.pwm.ChangeDutyCycle(speed)

class Relay():
    def __init__(self,pin):
        self.pin = pin
        gpio.setup(self.pin,gpio.OUT)
    def on(self):
        gpio.output(self.pin,gpio.HIGH)
    def off(self):
        gpio.output(self.pin,gpio.LOW)    
def main():
        motor.move(1,0.75)
        relay1.on()
        relay2.on()
        relay3.on()
        relay4.on()
        sleep(2)
        relay1.off()
        relay2.off()
        relay3.off()
        relay4.off()
        motor.move()
        sleep(1)
        relay1.on
        relay2.on
        relay3.on
        relay4.on
        motor.move(-1,0.99)
        sleep(2)
        

if __name__=='__main__':

        motor=Motor(17,27,22)
        relay1 =Relay(26)
        relay2 =Relay(19)
        relay3 =Relay(6)
        relay4 =Relay(5)
        
        main()


