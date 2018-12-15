#Import libraries
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import RPi.GPIO as GPIO
import epd2in7
import Image
import ImageFont
import ImageDraw
import time


epd = epd2in7.EPD()
epd.init()
EPD_WIDTH       = epd2in7.EPD_WIDTH
EPD_HEIGHT      = epd2in7.EPD_HEIGHT
GPIO.setmode(GPIO.BCM)
key1 = 5
key2 = 6
key3 = 13
key4 = 19
GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
image = Image.new('1', (epd2in7.EPD_WIDTH, epd2in7.EPD_HEIGHT), 255)
   

def updateDisplay(string):

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)

    draw.text((20, 50), string, font = font, fill = 0)
    #draw.rectangle((epd2in7.EPD_WIDTH/2-10, epd2in7.EPD_HEIGHT/2-10, epd2in7.EPD_WIDTH/2+10, epd2in7.EPD_HEIGHT/2+10), fill = 0)
    print('update display')
    epd.display_frame(epd.get_frame_buffer(image))

def makeImage():
    #Image Size
    EPD_WIDTH       = 176
    EPD_HEIGHT      = 264
    # Create a white mask 
    mask = Image.new('1', (EPD_HEIGHT,EPD_WIDTH), 255)   
    #Create a Draw object than allows to add elements (line, text, circle...) 
    draw = ImageDraw.Draw(mask)
    #Some Text
    draw.text((EPD_HEIGHT/4,EPD_WIDTH/2), 'Demo Python PILL', fill = 0)
    #Horizontal line
    draw.line((0,EPD_WIDTH/2 + 12, EPD_HEIGHT, EPD_WIDTH/2 + 12), fill = 0)
    #Save the picture on disk
    mask.save('demopill.bmp',"bmp")
    

updateDisplay("Hello")
