# -*- coding: utf-8 -*-
import json
import time
import sqlite3
import datetime
from utils.util_lib import modprobe_w1_gpio
from storage import Storage


class TemperatureSensor(object):
    """
    Base sensor class.
    Sensor is values (time, value)
    """
    value = ""

    def __init__(self):
        modprobe_w1_gpio()

    def save(self, dtime, value):
        """
        Saves to db
        """
        
        pass

    """
    Reads last 'count' values.
    Default count is 1 last value.
    """
    def read_last(self, count=1):

        pass

    """
    Reads values in date range
    """
    def read_range(self, datetime_from, datetime_to):
        pass
