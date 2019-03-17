# -*- coding: utf-8 -*-

"""
Модуль под общие методы,
которые могут использоваться где угодно.
Методы не связаны друг с другом.

"""
import os


def modprobe_w1_gpio():
    """
    Выполняет в консоли modprobe для GPIO
    (для raspberry pi)
    :return:
    """
    os.system('modprobe w1-gpio')  # Turns on the GPIO module
    os.system('modprobe w1-therm')  # Turns on the Temperature module
