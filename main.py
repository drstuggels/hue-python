# pylint: disable=no-value-for-parameter

import threading
import time
from os import getenv

from dotenv import load_dotenv
from phue import Bridge

b = Bridge(getenv("IP"))
light = b.lights[0]


def map_num(n, start1, stop1, start2, stop2, mode: str = "int"):
    mapped = (n-start1)/(stop1-start1)*(stop2-start2)+start2
    if mode == "int":
        return int(mapped)
    elif mode == "float":
        return float(mapped)
    elif mode == "round":
        return round((n-start1)/(stop1-start1)*(stop2-start2)+start2, 1)


def toggle():
    light.on = not(light.on)


def hue(percent: float):
    max_hue = 65535
    light.hue = map_num(percent, 0, 100, 0, max_hue)


def brightness(percent: float):
    max_brightness = 255
    light.brightness = map_num(percent, 0, 100, 0, max_brightness)


cont = True
thread = ""


def circle(sleep: float, increment: int):
    h = 0
    while cont:
        hue(h % 101)
        time.sleep(sleep)
        h += increment


def wild(sleep: float, increment: int):
    global thread
    global cont
    if thread != "":
        return
    else:
        cont = True
        thread = threading.Thread(target=circle, args=(sleep, increment,))
        thread.start()


def stop_wild():
    global cont
    global thread
    if thread == "":
        return
    else:
        cont = False
        thread.join()
        thread = ""


def warmth(percent: float):
    min_temp = 154
    max_temp = 500
    light.colortemp = map_num(percent, 0, 100, min_temp, max_temp)
