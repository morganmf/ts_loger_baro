#90EE90#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from Adafruit_BME280 import *
import httplib,urllib
from ctypes import c_short
import smbus
import os
import io
import sys
import time
import Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
from sys import stdout
from subprocess import *
from time import sleep, strftime
from datetime import datetime

#timeout = 1.0 # one second
sensor = BMP085.BMP085(mode=BMP085.BMP085_HIGHRES)
sensor_2 = BME280(p_mode=BME280_OSAMPLE_4, t_mode=BME280_OSAMPLE_4, h_mode=BME280_OSAMPLE_1, filter=BME280_FILTER_8)
#file = open("/home/pi/log/ttloger_log.csv", "a")
version = 'v1.61.806 Beta'
sensorht = Adafruit_DHT.DHT11
pin = 13
DEVICE = 0x77
bus = smbus.SMBus(1) # Rev 2 Pi uses 1
#sensor_2.read_pressure()
#hectopascals = pascals / 100
humidity, temperature = Adafruit_DHT.read_retry(sensorht, pin)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Optionally you can override the bus number:
#sensor = BMP085.BMP085(busnum=2)

# You can also optionally change the BMP085 mode to one of BMP085_ULTRALOWPOWER,
# BMP085_STANDARD, BMP085_HIGHRES, or BMP085_ULTRAHIGHRES.  See the BMP085
# datasheet for more details on the meanings of each mode (accuracy and power
# consumption are primarily the differences).  The default mode is STANDARD.
#sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

# Raspberry Pi pin configuration:
lcd_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 24
lcd_d4        = 22
lcd_d5        = 27
lcd_d6        = 17
lcd_d7        = 4
#lcd_backlight = 4

# Define LCD column and row size for 20x4 LCD.
#lcd_columns = 4
#lcd_rows    = 20

#Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           20, 4)
# initialize GPIO
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()


#read data using pin 26
#instance = sensorht(pin = 13)
#result = instance.read()

def readBmp180Id(addr=DEVICE):
  # Register Address
  REG_ID     = 0xD0

  (chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
  return (chip_id, chip_version)

def measure_CPUtemp():
        temp = os.popen("vcgencmd measure_temp").readline()
        return (temp.replace("temp=",""))

def doMain():
        #meastime = raw_input('Wprowadz czas pomiaru w sekundach:')
        #meastimefl = float(meastime)
        #m1time = int(meastimefl)
        #m2time = int(m1time/60)
        lcd.message('TTLoger'+chr(10))
        lcd.message(version+chr(10))
        #time.sleep(0.5)
        lcd.message('blaoyne 2018 ,2019   '+chr(10))
        print('\n')
        #time.sleep(0.5)
        lcd.message('start logowania'+chr(10))
        lcd.message('barolog_test.csv'+chr(10))
        time.sleep(0.425)
        lcd.clear()
        lcd.message('Inicjalizacja...\n')
        time.sleep(0.333)
        lcd.message('Ladowanie...')
        lcd.message('.')
        time.sleep(0.33)
        lcd.message('.')
        time.sleep(0.33)
        lcd.message('.')
        lcd.message('.'+chr(10))
        lcd.message('Wysokosc {0:0.0f}m n.p.m. \n'.format(sensor.read_altitude()))
        time.sleep(0.712)
        lcd.set_cursor(9,3)
        lcd.message('OK!')
        time.sleep(0.33)
        lcd.clear()
        print('Wysokość '+ bcolors.BOLD+'{0:0.0f}m n.p.m.'.format(sensor.read_altitude())+bcolors.ENDC)
        (chip_id, chip_version) = readBmp180Id()
        meas = "pomiar co"
        meas2 = "minut(y)"
        #meastimeminute = str(int(meastime))
        print(meas,bcolors.BOLD, m2time, bcolors.ENDC, meas2)
        print( 'Parametry sensora',)
        print("Chip ID     :", bcolors.BOLD, chip_id, bcolors.ENDC)
        print("Wersja      :", bcolors.BOLD, chip_version, bcolors.ENDC)
        print("Pi temp     :",  bcolors.BOLD, measure_CPUtemp(), bcolors.ENDC)
        print('--------------------------------------------------')
	                
def endWork():
    lcd.clear()
    os.system('cls' if os.name == 'nt' else 'clear')
    lcd.message('zamykanie...\n')
    print(bcolors.BOLD+"\n"+'zamykanie')
    time.sleep(0.833)
    os.system('cls' if os.name == 'nt' else 'clear')
    lcd.message('do widzenia')
    print('do widzenia\n'+bcolors.ENDC)
    time.sleep(0.75)
    lcd.clear()
    #file.close()
    os.system('cls' if os.name == 'nt' else 'clear')
    lcd.display = False
    os._exit(1)
    pass

def fileWork():
    humidity, temperature = Adafruit_DHT.read_retry(sensorht, pin)
    #print(temperature, humidity)
    conn=httplib.HTTPConnection("api.thingspeak.com:80")
    #print("Temperature : ", sensor.read_temperature, "C")
    #print("Pressure    : ", sensor.read_sealevel_pressure, "mbar\n\n")
    headers={"Content-type":"application/x-www-form-urlencoded","Accept":"text/plain"}
    #(temperature,pressure)=readBmp180()
    params=urllib.urlencode({'field1':sensor.read_temperature(),'field2':humidity,'field3':sensor.read_sealevel_pressure()/100,'field4':sensor.read_pressure()/100,'field5':sensor_2.read_temperature(),'field6':measure_CPUtemp(),'key':'0JSYXZIYX2U9B5D4'})
    conn.request("POST","/update",params,headers)
    response=conn.getresponse()
    print(bcolors.BOLD+bcolors.OKGREEN+' >status<',response.status,response.reason)
    print(bcolors.ENDC)
    data = response.read()
    lcd.set_cursor(19, 0)
    lcd.message('@')
    time.sleep(0.13)
    lcd.set_cursor(19, 1)
    lcd.message('v')
    time.sleep(0.03)
    lcd.set_cursor(19, 2)
    lcd.message('v')
    time.sleep(0.13)
    lcd.set_cursor(19, 3)
    lcd.message('v')
    time.sleep(0.13)
    lcd.set_cursor(19, 2)
    lcd.message('v')
      
    
def doWork():
    humidity, temperature = Adafruit_DHT.read_retry(sensorht, pin)
    time.sleep(0.03)
    print(bcolors.HEADER+' odczyt wartości z sensorów...'+bcolors.ENDC)    
    {print(bcolors.BOLD+"\r"+datetime.now().strftime("\033[K %-d/%-m/%Y %-H:%M.%S  ") + '\033[K| Ciśn.QFE@61m={0:0.2f}mbar '.format(sensor.read_pressure()/100)+
           '\033[K| Ciśn.QNH={0:0.2f}mbar '.format(sensor.read_sealevel_pressure()/100)+'\033[K| T1={0:0.1f}°C'.format(sensor.read_temperature())+
           ' | T2={0:0.0f}°C | H1={1:0.0f}%'.format(temperature, humidity), end=' '+'wilg. '+bcolors.ENDC),} 
    print(bcolors.HEADER+'\n zapis do thingspeak.com...'+bcolors.ENDC)
    sys.stdout.flush()
    #time.sleep(0.5)
    
def doLCD():
    #humidity, temperature = Adafruit_DHT.read_retry(sensorht, pin)
    #lcd.clear()
    lcd.set_cursor(19, 0)
    lcd.message('X')
    time.sleep(0.33)
    lcd.set_cursor(19, 1)
    lcd.message('*')
    lcd.set_cursor(19, 0)
    lcd.message('/')
    time.sleep(0.33)
    lcd.set_cursor(19, 2)
    lcd.message('*')
    lcd.set_cursor(19, 0)
    time.sleep(0.33)
    lcd.message('-')
    time.sleep(0.33)
    lcd.set_cursor(19, 3)
    lcd.message('*')
    lcd.set_cursor(19, 0)
    lcd.message('X')
    time.sleep(0.33)
    lcd.set_cursor(19, 2)
    lcd.message('*')
    lcd.set_cursor(19, 0)
    time.sleep(0.33)
    lcd.message('|')
    lcd.set_cursor(19, 0)
    lcd.message(' ')
    time.sleep(0.33)
    lcd.set_cursor(19, 1)
    time.sleep(0.33)
    lcd.set_cursor(0, 0)
    lcd.message(datetime.now().strftime('%-d/%-m/%Y %-H:%M.%S '))
    lcd.set_cursor(0, 1)
    lcd.message('Wilg={0:0.0f}%'.format(humidity)+'  '+chr(247)+'='+measure_CPUtemp())
    lcd.set_cursor(0, 2)
    lcd.message('{0:0.1f}'.format(sensor.read_pressure()/100)+'mbar  {0:0.1f}'.format(sensor.read_temperature())+chr(223)+'C ')
    lcd.set_cursor(0, 3)
    lcd.message('{0:0.1f}mbar  '.format(sensor.read_sealevel_pressure()/100)+'{0:0.1f}'.format(temperature)+chr(223)+'C ')
    
lcd.clear()
os.system('cls' if os.name == 'nt' else 'clear')

try:
    while True:
        print(bcolors.WARNING + bcolors.BOLD +'--------------------------------------------------')
        print('|TTLoger '+version+'                          |')
        print('|BMP180/BMB280/DHT22                             |')
        print('|                                                |')
        print('|(c)tito blaoyne 2018,2019                       |')
        print('| Naciśnij Ctrl-C aby zakończyć program          |')
        print('--------------------------------------------------'+bcolors.ENDC)
        meastime = raw_input('Wprowadź czas pomiaru w sekundach:')
        meastimefl = float(meastime)
        m1time = int(meastimefl)
        m2time = int(m1time/60)
        doMain()
        while True:
          doLCD()
          doWork()
          fileWork()
          time.sleep(m1time-7)                    
except KeyboardInterrupt:
        endWork()
        pass

    





