# -*- coding: utf-8 -*-
import os

def modprobe_w1_gpio():
    """
    Initialize the GPIO Pins
    :return:
    """
    os.system('modprobe w1-gpio')  # Turns on the GPIO module
    os.system('modprobe w1-therm')  # Turns on the Temperature module
