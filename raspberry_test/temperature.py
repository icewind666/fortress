# -*- coding: utf-8 -*-
import json
import time
import sqlite3
import datetime


class Sensor(object):
    """
    Base sensor class.
    Sensor is values (time, value)
    """
    value = ""
    id = ""
    units = "шт."
    db_table = "default"


    """
    Saves to db
    """
    def save(self):

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


class Temperature(Sensor):
    """
    Temperature sensor class.
    """

    """
    Inits temp sensor.
    """
    def init(self):
        pass
