#coding: utf-8
# eInk - ePaper doshboard connected to Jeedom, Open Source Home Automation server
# Waveshare 2,7inch SPI ePaper display
# Full tutorial 
# English version https://diyprojects.io/weather-station-epaper-displaydashboard-jeedom-raspberry-pi-via-json-rpc-api/#.WqjWOJPOU_U
# French version https://projetsdiy.fr/station-meteo-affichage-epaper-eink-dashboard-jeedom-raspberrypi-jsonrpc/
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import requests
import json
import math
import time
from datetime import datetime 
from datetime import timedelta 
import locale
locale.setlocale(locale.LC_TIME,'')

darksky_api_key = "0c364b329eaaaf21879e82272fbb2cba"
darksky_forecast_url = "https://api.darksky.net/forecast/"
latLon = "/35.970,-78.893"
url = darksky_forecast_url + darksky_api_key + latLon

imageFolder = "/img"

H_condition = 100
W_condition = 100
H_Big = 15
H_icone = 25
W_icone = 25
Bord = 5
Col1 = 66
Col2 = 132
Col3 = 198
LiBaCd = 140
DiamPastille = 10
modeTest = False
prevision = {}

if modeTest:
  EPD_WIDTH       = 176
  EPD_HEIGHT      = 264
else:
  print 'mode epd2in7'
  import RPi.GPIO as GPIO
  import epd2in7
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

#Load Images and fonts
fontSmall = ImageFont.truetype(folder_img + 'FreeMonoBold.ttf', 9)
fontMedium = ImageFont.truetype(folder_img + 'FreeMonoBold.ttf', 12)
fontBig = ImageFont.truetype(folder_img + 'FreeMonoBold.ttf', H_Big)
temperature = Image.open(folder_img + 'temperature.png')
humidity = Image.open(folder_img + 'humidity.png')
pressure = Image.open(folder_img + 'pressure.png')
direction = Image.open(folder_img + 'direction.png')
lever = Image.open(folder_img + 'lever.png')
coucher = Image.open(folder_img + 'coucher.png')

#Resize pictures
temperature = temperature.resize((H_icone,W_icone))
humidity = humidity.resize((H_icone,W_icone))
pressure = pressure.resize((H_icone,W_icone))
direction = direction.resize((H_icone,W_icone))
lever = lever.resize((H_icone ,W_icone ))
coucher = coucher.resize((H_icone ,W_icone ))
#w,h = condition.size

def updateParameter(id, method):
  # Jeedom JSON RPC API documentation
  # https://jeedom.github.io/core/fr_FR/jsonrpc_api#tocAnchor-1-30-2
  parameters = {                                                                
    "jsonrpc" : "2.0",                                                    
    "method" : method,                                                                                                              
    "params": {                                                           
        "apikey": Api_key,
        "id" : id                                      
        }                                                                 
  }  
  return parameters

def getDirWind(WindDir):
  #https://www.campbellsci.com/blog/convert-wind-directions
  Direction = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW","N"]
  CompassDir = int(round((math.fmod(WindDir,360))/ 22.5,0)+1)
  return Direction[CompassDir]

def findIcone(condition_id):
  # All weather conditions returned by Jeedom
  # Toutes les conditions renvoyees par le plugin météo de Jeedom https://github.com/jeedom/plugin-weather/blob/beta/core/class/weather.class.php
  # Prevision d apres le code openweathermap.org
  # Icones Open Source https://github.com/kickstandapps/WeatherIcons
  # Icones température, humidité, pression atmosphérique récupérées sur https://icones8.fr
  if condition_id >= 200 and condition_id <= 299:
    return 'Storm'  
  if condition_id >= 300 and condition_id <= 399:
    return 'Haze'  
  if condition_id >= 500 and condition_id <= 510:
    return 'PartlySunny'  
  if condition_id >= 520 and condition_id <= 599:
    return 'Rain'  
  if condition_id >= 600 and condition_id <= 699 or condition_id == 511:
    return 'Snow' 
  if condition_id >= 700 and condition_id <= 799:
    return 'wind'
  if condition_id >= 800 and condition_id <= 899:
    return 'Cloud'  
  if condition_id == 800:
    return 'Sun'  

conditions = {
  "clear-day": "Clear",
  "clear-night": "Clear",
  "rain": "Rainy",
  "snow": "Snowy",
  "sleet": "Sleet",
  "wind": "Windy",
  "fog": "Foggy",
  "cloudy": "Cloudy",
  "partly-cloudy-day": "Partly cloudy",
  "partly-cloudy-night": "Partly cloudy"
}

def parseDaily(daily):
  dailyIcon = daily["icon"]
  dailySummary = daily["summary"]
  dailyData = daily["data"]

def parseHourly(hourly):  
  hourlyIcon = hourly["icon"]
  hourlySummary = hourly["summary"]
  hourlyData = hourly["data"]

def parseMinutely(minutely):      
  minutelySummary = minutely["summary"]
  minutelyIcon = minutely["icon"]
  minutelyData = minutely["data"]

def getDataFromDarkySky():
  response = requests.get(url)
  jsonResponse = json.loads(response.text)
  currently = jsonResponse["currently"]
  currentSummary = currentSummary["summary"]
  minutely = jsonResponse["minutely"]
  hourly = jsonResponse["hourly"]
  daily = jsonResponse["daily"]

  flags = jsonResponse["flags"]
  windDir = getDirWind(currently["windBearing"])
  windSpeed = currently["windSpeed"]

  data = {}
  data["currently"] = currently
  data["minutely"] = minutely
  data["hourly"] = hourly
  data["daily"] = daily


def updateFrame1():
  mask = Image.new('1', (EPD_HEIGHT,EPD_WIDTH), 255)       
  draw = ImageDraw.Draw(mask)

  morningCondition = "Morning condition"
  eveningCondition = "Evening condition"
  sunrise = "daily[0][sunriseTime]"
  sunset = "daily[0][sunsetTime]"

  data = getDataFromDarkySky()
  currentSummary = data["currently"]["summary"]

  # condition = Image.open(folder_img + prevision['condition'] + '.png')
  # condition = condition.resize((H_condition,W_condition))
  mask.paste(condition, (0,0), condition)
  mask.paste(lever, (W_condition + Bord,70), lever)
  mask.paste(coucher, (W_condition + 90,70), coucher)
  date = unicode(time.strftime("%a %d %B") + "  " + time.strftime("%H:%M"),'UTF-8')
  draw.text((W_condition + Bord,5), date, font = fontMedium, fill = 0)

  draw.text((W_condition + Bord,25), condGauche, font = fontBig, fill = 0)
  draw.text((W_condition + Bord,45), condDroite, font = fontBig, fill = 0)
  draw.text((W_condition + 45,75), getSunTime(str(prevision['leverSoleil']['value'])), font = fontSmall, fill = 0)
  draw.text((W_condition + 125,75), getSunTime(str(prevision['coucherSoleil']['value'])), font = fontSmall, fill = 0)

  #Prévision du jour en détail - Today weather forecast
  #Tourne la bousole dans la direction du vent - Wind direction
  direction.rotate(float(prevision['dirVent']['value']))
  mask.paste(temperature, (Bord,110), temperature)
  mask.paste(humidity, (Col1,110), humidity)
  mask.paste(pressure, (Col2,110), pressure)
  mask.paste(direction, (Col3,110), direction)
  draw.text((Bord,LiBaCd), str(prevision['tempMax']['value']) + '%C', font = fontMedium, fill = 0)
  draw.text((Col1,LiBaCd), str(prevision['humidite']['value'])+'%', font = fontMedium, fill = 0)
  draw.text((Col2,LiBaCd), str(prevision['pa']['value'])+str(prevision['pa']['unit']), font = fontMedium, fill = 0)
  draw.text((Col3 + 35,110), getDirWind(float(prevision['dirVent']['value'])), font = fontMedium, fill = 0)
  draw.text((Col3,LiBaCd), str(prevision['vitVent']['value'])+str(prevision['vitVent']['unit']),font = fontMedium, fill = 0)

  #Lignes - draw lines
  draw.line((0,H_condition,EPD_HEIGHT,H_condition), fill=0)
  draw.line((0,LiBaCd + 20,EPD_HEIGHT,LiBaCd + 20), fill=0)
  draw.line((W_condition,0,W_condition,H_condition), fill=0)

  #Bas de page - draw bottom of the page
  draw.text((Bord,EPD_WIDTH - 18), str(prevision['city']),font = fontMedium, fill = 0)
  draw.text((180,EPD_WIDTH - 17), "projetsdiy.fr",font = fontSmall, fill = 0)
  draw.ellipse((97,EPD_WIDTH - DiamPastille - 2,107,EPD_WIDTH - 2), fill=0, outline=0)
  draw.ellipse((117,EPD_WIDTH - DiamPastille - 2,127,EPD_WIDTH - 2), fill=255, outline=0)
  draw.ellipse((137,EPD_WIDTH - DiamPastille - 2,147,EPD_WIDTH - 2), fill=255, outline=0)
  draw.ellipse((157,EPD_WIDTH - DiamPastille - 2,167,EPD_WIDTH - 2), fill=255, outline=0)  



  out = mask.rotate(90)
  out.save('frame1.bmp',"bmp")

  if modeTest == False:
    epd.display_frame(epd.get_frame_buffer(out))

#Prévisions des 4 prochains jours - 4-days forecast
def updateFrame2():
    mask = Image.new('1', (EPD_HEIGHT,EPD_WIDTH), 255)   
    date = datetime.now()
    draw = ImageDraw.Draw(mask)
    pasHoriz = 16
    #Format date heure en Python https://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/
    #Entete
    draw.text((Bord,0), unicode("Prévisions à 4 jours",'utf-8'), font = fontBig, fill = 0)
    draw.line((0,2*Bord + H_Big,EPD_HEIGHT,2*Bord + H_Big), fill=0)
    draw.line((Col1, 2*Bord + H_Big, Col1, EPD_WIDTH - 15), fill=0)
    draw.line((Col2, 2*Bord + H_Big, Col2, EPD_WIDTH - 20), fill=0)
    draw.line((Col3, 2*Bord + H_Big, Col3, EPD_WIDTH - 20), fill=0)
    draw.line((0,EPD_WIDTH - 15,EPD_HEIGHT,EPD_WIDTH - 15), fill=0)

    #J+1 - day + 1
    date = datetime.now() + timedelta(days=1)  
    draw.text((Bord, 3*Bord + H_Big), unicode(date.strftime("%A"),'utf-8'), font = fontMedium, fill = 0)
    c1 = Image.open(folder_img + prevision['conditionJ1'] + '.png')
    c1 = c1.resize((H_icone * 2,W_icone * 2))
    mask.paste(c1, (Bord, 5*Bord + H_Big), c1)    
    prev1 = prevision['condJ1Txt']['value'][0:12]
    prev2 = prevision['condJ1Txt']['value'][12:24]
    print prev2
    draw.text((Bord, 5 * pasHoriz), prev1, font = fontSmall, fill = 0)
    draw.text((Bord, 6 * pasHoriz), prev2, font = fontSmall, fill = 0)
    draw.text((Bord, 7 * pasHoriz), unicode(str(prevision['tempMinJ1']['value'])+'°C','utf-8'), font = fontMedium, fill = 0)
    draw.text((Bord, 8 * pasHoriz), unicode(str(prevision['tempMaxJ1']['value'])+'°C','utf-8'), font = fontMedium, fill = 0)
    
    #J+2 - Day + 2
    date = datetime.now() + timedelta(days=2)  
    draw.text((Bord + Col1, 3*Bord + H_Big), unicode(date.strftime("%A"),'utf-8'), font = fontMedium, fill = 0)
    c1 = Image.open(folder_img + prevision['conditionJ2'] + '.png')
    c1 = c1.resize((H_icone * 2,W_icone * 2))
    mask.paste(c1, (Bord + Col1, 5*Bord + H_Big), c1)
    prev1 = prevision['condJ2Txt']['value'][0:12]
    prev2 = prevision['condJ2Txt']['value'][12:24]
    draw.text((Bord + Col1, 5 * pasHoriz), prev1, font = fontSmall, fill = 0)
    draw.text((Bord + Col1, 6 * pasHoriz), prev2, font = fontSmall, fill = 0)
    draw.text((Bord + Col1, 7 * pasHoriz), unicode(str(prevision['tempMinJ2']['value'])+'°C','utf-8'), font = fontMedium, fill = 0)
    draw.text((Bord + Col1, 8 * pasHoriz), unicode(str(prevision['tempMaxJ2']['value'])+'°C','utf-8'), font = fontMedium, fill = 0)

    #J+3
    date = datetime.now() + timedelta(days=3)  
    draw.text((Bord + Col2, 3*Bord + H_Big), unicode(date.strftime("%A"),'utf-8'), font = fontMedium, fill = 0)
    c1 = Image.open(folder_img + prevision['conditionJ3'] + '.png')
    c1 = c1.resize((H_icone * 2,W_icone * 2))
    mask.paste(c1, (Bord + Col2, 5*Bord + H_Big), c1)
    prev1 = prevision['condJ3Txt']['value'][0:12]
    prev2 = prevision['condJ3Txt']['value'][12:24]
    draw.text((Bord + Col2, 5 * pasHoriz), prev1, font = fontSmall, fill = 0)
    draw.text((Bord + Col2, 6 * pasHoriz), prev2, font = fontSmall, fill = 0)
    draw.text((Bord + Col2, 7 * pasHoriz), unicode(str(prevision['tempMinJ3']['value'])+'°C','utf-8'), font = fontMedium, fill = 0)
    draw.text((Bord + Col2, 8 * pasHoriz), unicode(str(prevision['tempMaxJ3']['value'])+'°C','utf-8'), font = fontMedium, fill = 0)    

    #J+4
    date = datetime.now() + timedelta(days=4)  
    draw.text((Bord + Col3, 3*Bord + H_Big), unicode(date.strftime("%A"),'utf-8'), font = fontMedium, fill = 0)
    c1 = Image.open(folder_img + prevision['conditionJ4'] + '.png')
    c1 = c1.resize((H_icone * 2,W_icone * 2))
    mask.paste(c1, (Bord + Col3, 5*Bord + H_Big), c1)
    prev1 = prevision['condJ4Txt']['value'][0:12]
    prev2 = prevision['condJ4Txt']['value'][12:24]
    draw.text((Bord + Col3, 5 * pasHoriz), prev1, font = fontSmall, fill = 0)
    draw.text((Bord + Col3, 6 * pasHoriz), prev2, font = fontSmall, fill = 0)
    #draw.text((Bord + Col1, 6 * pasHoriz), str(prevision['condJ4Txt']['value'][0:10]), font = fontSmall, fill = 0)
    draw.text((Bord + Col3, 7 * pasHoriz), unicode(str(prevision['tempMinJ4']['value'])+'°C','utf-8'), font = fontMedium, fill = 0)
    draw.text((Bord + Col3, 8 * pasHoriz), unicode(str(prevision['tempMaxJ4']['value'])+'°C','utf-8'), font = fontMedium, fill = 0)

    #Bas de page - Page footer
    draw.text((Bord,EPD_WIDTH - 18), str(prevision['city']),font = fontMedium, fill = 0)
    draw.text((180,EPD_WIDTH - 17), "projetsdiy.fr",font = fontSmall, fill = 0)
    draw.ellipse((97,EPD_WIDTH - DiamPastille - 2,107,EPD_WIDTH - 2), fill=255, outline=0)
    draw.ellipse((117,EPD_WIDTH - DiamPastille - 2,127,EPD_WIDTH - 2), fill=0, outline=0)
    draw.ellipse((137,EPD_WIDTH - DiamPastille - 2,147,EPD_WIDTH - 2), fill=255, outline=0)
    draw.ellipse((157,EPD_WIDTH - DiamPastille - 2,167,EPD_WIDTH - 2), fill=255, outline=0) 
    
    out = mask.rotate(90)
    out.save('frame2.bmp',"bmp")

    if modeTest==False:
      epd.display_frame(epd.get_frame_buffer(out))

def main():
    if modeTest:
      getDataFromJeedom()  
      updateFrame1()
      #updateFrame2()
    else:
      while True:
        key1state = GPIO.input(key1)
        key2state = GPIO.input(key2)
        key3state = GPIO.input(key3)
        key4state = GPIO.input(key4)
    
        if key1state == False:
            print('Update frame 1')
            getDataFromJeedom()  
            updateFrame1()
            time.sleep(0.5)
        if key2state == False:
            print('Update frame 2')
            getDataFromJeedom()  
            updateFrame1()
            time.sleep(0.5)
        if key3state == False:
            print('Key3 Pressed')
            time.sleep(0.2)
        if key4state == False:
            print('Key4 Pressed')
 
if __name__ == "__main__":
    #Met à jour l'écran au démarrage
    getDataFromJeedom()  
    #updateFrame2()
    updateFrame1() 
    
    # Then wait you press key1 to key4 to update screen (only on Raspberry Pi 3)
    # puis attend un événement sur les touches Key1 à Key4 (sur un Raspberry Pi uniquement)
    main()
