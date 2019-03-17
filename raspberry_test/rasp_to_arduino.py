#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import time


STOP_CODE = "3"
FORWARD_CODE = "4"
BACKWARD_CODE = "2"
RIGHT_CODE = "5"
LEFT_CODE = "6"

TOWER_LEFT_CODE = "7"
TOWER_RIGHT_CODE = "8"

ser = serial.Serial("/dev/ttyUSB0", 9600)
s = ser.readline()
time.sleep(0.5)


class AntBody(object):
    """

    """
    head = AntHead()

    STOP_CODE = "3"
    FORWARD_CODE = "4"
    BACKWARD_CODE = "2"
    RIGHT_CODE = "5"
    LEFT_CODE = "6"

    def __init__(self):
        pass

    def forward(self):
        pass

    def backward(self):
        pass

    def left(self):
        pass

    def right(self):
        pass


class AntHead(object):
    """
    Can look up and down. Left and right.
    Used with on tank with camera
    """
    TOWER_LEFT_CODE = "7"
    TOWER_RIGHT_CODE = "8"
    TOWER_UP_CODE = "9"
    TOWER_DOWN_CODE = "10"

    def up(self):
        pass

    def down(self):
        pass

    def left(self):
        pass

    def right(self):
        pass


class Ant(object):
    """
    Primary information unit in hive
    """
    body = AntBody()
    head = AntHead()

    pass


class RangerAnt(Ant):
    """
    Ranger tank ant.
    With sensors and wheels
    """
    pass


def move_tank(direction):
    ser.write(direction.encode("UTF-8"))
    time.sleep(2)
    ser.write(STOP_CODE.encode("UTF-8"))


if __name__ == '__main__':
    print("C - FORWARD 2 sec")
    print("V - BACKWARD 2 sec")
    print("Z - LEFT 2 sec")
    print("X - RIGHT 2 sec")

    print("a - TOWER LEFT 2 sec")
    print("s - TOWER RIGHT 2 sec")

    print("You can use sequence like FFLR")
    screen = curses.initscr()
    #curses.noecho()
    #screen.keypad(True)

    screen.nodelay(1)

    while True:
        char = screen.getch()
        if char != -1:
            print(char)
        if char == 113:
            curses.endwin()
            break  # q
        elif char == 120:
            move_tank(RIGHT_CODE)
        elif char == 122:
            move_tank(LEFT_CODE)
        elif char == 99:
            move_tank(FORWARD_CODE)
        elif char == 118:
            move_tank(BACKWARD_CODE)
        elif char == 115:
            move_tank(TOWER_LEFT_CODE)
        elif char == 97:
            move_tank(TOWER_RIGHT_CODE)

        else:
            pass
        time.sleep(0.1)

