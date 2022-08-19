import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_pcd8544
import time
import requests
from random import randint
from module import Motor,Relay
import serial
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

url = "http://itfiot.hub.ubeac.io/ITFV2"
uid ="POT"
timeout =2 #seconds

line1 = "Welcome"
line2 ="Line 2"
line3 = "Line 3"

i2c = busio.I2C(board.SCL, board.SDA)
adc = ADS.ADS1015(i2c)

motor=Motor(17,27,22) 

A = Relay(26)
B = Relay(19)
C = Relay(6)
D = Relay(5)

spi = busio.SPI(board.SCK, MOSI=board.MOSI)
dc = digitalio.DigitalInOut(board.D23)  # data/command
cs = digitalio.DigitalInOut(board.CE0)  # Chip select
reset = digitalio.DigitalInOut(board.D24)  # reset
display = adafruit_pcd8544.PCD8544(spi, dc, cs, reset)
fontSize = 15

# Contrast and Brightness Settings
display.bias = 4
display.contrast = 60

# Turn on the Backlight LED
backlight = digitalio.DigitalInOut(board.D18)  # backlight
backlight.switch_to_output()
backlight.value = True

# Clear display.
display.fill(0)
display.show()
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontSize)
potentiometer = 0

def readAnalog():
    maxVal = 32767
    GAIN=1
    chan = AnalogIn(adc, ADS.P0)
    newdata = chan.value
    # newdata = adc.read_adc(0, gain=GAIN)
    val = int(newdata)
    mapped =(100 * val)/( maxVal )
    return mapped

def readAnalog1():
    maxVal =1023
    port = "/dev/serial0" 
    ser=serial.Serial(port,baudrate=9600,timeout =3)
    newdata=ser.readline()
    newdata =str(newdata)
    a= newdata.find("{") 
    b = newdata.find("}")
    newdata =newdata[a+1:b]
    try:
        val = int(newdata)
        mapped =(100 * val)/( maxVal )
        return mapped
    except :
        print('Error')
        return -1


def post(potentiometer):
    try:
    
#        potentiometer = randint(0,100) 
        data = {
                "id": uid,
                "sensors":[{
                  'id': 'ptentiometer',
                  'data': potentiometer
                }]
            }

        r = requests.post(url, verify=False, json=data)
       # print(r.status_code) 
    except KeyboardInterrupt:
        pass
lastTime = time.time()
direction = True
while True:
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.

    val = readAnalog()
    line1 = "POT is "+str(int(val))+"%"

    if val <=15:
        motor.move(-1,100)
        A.on()
        B.off()
        C.off()
        D.off()
        line2 = "Motor: Turns Left"
        line3 = "Relay: A is ON"
    elif val >15 and val <= 30:
        motor.move(1,100)
        A.off()
        B.on()
        C.off()
        D.off()
        line2 = "Motor: Turns Right"
        line3 = "Relay: B is ON"
    elif val >30 and val <=45:
        motor.move(-1,50)
        A.off()
        B.off()
        C.on()
        D.off()
        line2 = "Motor: Turns Left"
        line3 = "Relay: C is ON"
    elif val >45 and val <=60:
        motor.move(1,50)
        A.off()
        B.off()
        C.off()
        D.on()
        line2 = "Motor: Turns Right"
        line3 = "Relay: D is ON"
    elif val >60 and val <=80:
        if (time.time() - lastTime) >= timeout:
            direction = not direction
            if direction:
                motor.move(1,75)
                B.on()
                A.off()
                line2 = "Motor: Turns Right"
                line3 = "Relay: B is ON"

            else:
                motor.move(-1,75)
                A.on()
                B.off()
                line2 = "Motor: Turns Left"
                line3 = "Relay: A is ON"
            lastTime = time.time()

    elif val >80 and val <=100:
        motor.move()
        A.on()
        B.on()
        C.on()
        D.on()
        line2 = "Motor: Stopped"
        line3 = "Relay: All are ON"
    if val != -1:
        post(val)

    image = Image.new("1", (display.width, display.height))

# Get drawing object to draw on image
    draw = ImageDraw.Draw(image)

# Draw Some Text

    (font_width, font_height) = font.getsize(line1)
    draw.text(
        (0,0),
        line1,
        font=font,
        fill=255,
        
    )
    (font_width, font_height) = font.getsize(line2)
    draw.text(
        (0,10),
        line2,
        font=font,
        fill=255,
    )
    (font_width, font_height) = font.getsize(line3)
    draw.text(
        (0,20),
        line3,
        font=font,
        fill=255,
    )


# Display image
    display.image(image)
    display.show()
