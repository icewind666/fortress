#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модуль используется при прямом подключении датчика температуры к
Raspberry pi (gpio)

Читает температуру с датчика, показывает на lcd экране
А также отправляет GET-запросом на серверную часть.
(http://192.168.0.104:9999/temp?t={})
"""

import glob
import os
import time

import RPi.GPIO as GPIO
import requests
import serial

from raspberry_test.lcd_iic import LCDDisplay

GPIO.setmode(GPIO.BCM)

# Initialize the GPIO Pins
os.system('modprobe w1-gpio')  # Turns on the GPIO module
os.system('modprobe w1-therm')  # Turns on the Temperature module

# Finds the correct device file that holds the temperature data
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

lcd = LCDDisplay()
lcd.init()
last_value = 0  # last temperature read


# A function that reads the sensors data
def read_temp_raw():
    f = open(device_file, 'r')  # Opens the temperature device file
    lines = f.readlines()  # Returns the text
    f.close()
    return lines


# Convert the value of the sensor into a temperature
def read_temp():
    lines = read_temp_raw()  # Read the temperature 'device file'

    # While the first line does not contain 'YES', wait for 0.2s
    # and then read the device file again.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
    lines = read_temp_raw()

    # Look for the position of the '=' in the second line of the
    # device file.
    equals_pos = lines[1].find('t=')

    # If the '=' is found, convert the rest of the line after the
    # '=' into degrees Celsius, then degrees Fahrenheit
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    else:
        return "ERR"


def lcd_write_temp(t):
    lcd.print_line1("Temperature")
    lcd.print_line2("{} C".format(t))
    # lcd.lcd_byte(0x01, lcd.LCD_CMD)


# Print out the temperature until the program is stopped.
ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
    try:
        current_temp = read_temp()
        print('Read t=', current_temp)
        if abs(float(current_temp) - last_value) > 1:
            print('delta = ', abs(float(current_temp) - last_value))
            ser.write('10')
            time.sleep(.3)
            ser.write('100')
            time.sleep(.3)
            # ser.write('10')
            # time.sleep(.)
            last_value = float(current_temp)
        r = requests.get("http://192.168.0.104:9999/temp?t={}".format(current_temp))
        lcd_write_temp(current_temp)
        time.sleep(3)
    except KeyboardInterrupt:
        break
