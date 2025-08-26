import os, random
from PIL import Image
import json
import rx
from rx import operators as ops
from rx.subject import Subject

from RPi import GPIO
from time import sleep
import time
import copy
from io import BytesIO

from random import randint

import board
import busio
import serial

import math
from KnobInput import *
from story_maker import *
from RPLCD import i2c
from Adafruit_Thermal import *
import adafruit_thermal_printer

from picamera import PiCamera
import picamera

from PIL import Image, ImageOps
import numpy as np
from numpy import asarray

# Set up Knobs and Buttons
GPIO.setmode(GPIO.BCM)
left_knob = Knob(23,24)
right_knob = Knob(17,27)
main_button = PressButton(18)

# Set up printer
ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.64)
RX = board.RX
TX = board.TX
# uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
# 
# printer = ThermalPrinter(uart, auto_warm_up=False)

printer = Adafruit_Thermal("/dev/serial0", 9600, timeout=5)
# printer.warm_up()

# Set up LCD
lcdmode = 'i2c'
cols = 16
rows = 2
charmap = 'A00'
i2c_expander = 'PCF8574'
address = 0x27
port = 1
lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap, cols=cols, rows=rows)

camera = PiCamera()

# Set up Menu
#menu = Menu()
#menu.display_output.subscribe(lambda x: process_display_output(x))
#menu.printer_output.subscribe(lambda x: process_printer_output(x))

current_choice_index = 0.0



def process_story_output(output):
#     print(output)
   
    if output["type"] == "printText":
         print_text(output["data"])
         
    if output["type"] == "printImage":
        print("printing image...")
        print(output["data"])

    
def process_left_knob(input):
    print(input)
#     menu.left_knob_input.on_next(input)

def process_right_knob(event):
    global current_choice_index
    if event == "up":
        current_choice_index += 0.5
    if event == "down":
        current_choice_index -= 0.5
    update_display()

def process_center_press(event):
    if event == "pressed":
        global current_choice_index
        global story_maker
        choice = story_maker.choices[int(current_choice_index)%len(story_maker.choices)]
        story_maker.select_choice(choice)

def update_display():
    global current_choice_index
    global story_maker
    if len(story_maker.choices) == 0:
        lcd.clear()
        return
    output = story_maker.choices[int(current_choice_index)%len(story_maker.choices)]["text"]
    lcd.clear()
    lcd.write_string(output)
    
        
def print_text(input_text):
    lines = wrap_for_printing(input_text)
    for line in lines:
        printer.println(line)
        
def wrap_for_printing(input_string):
    length_limit = 32
    lines = []
    
    words = input_string.split()
    line = ""
    for word in words:
        if len(line) + len(word) + 1 < length_limit:
            line += " "
            line += word
        else:
            lines.append(line)
            line = word

    lines.append(line)
    return lines


main_button.output_subject.subscribe(lambda x: process_center_press(x))
left_knob.output_subject.subscribe(lambda x: process_left_knob(x))
right_knob.output_subject.subscribe(lambda x: process_right_knob(x))


story_maker = StoryMaker("crab_island_images.txt")

story_maker.output_subject.subscribe(lambda x: process_story_output(x))
#story_maker.choices

story_maker.goto_story_node("00000000-0000-0000-0000-000000000000")
lcd.write_string("Story start")





try:
    while story_maker.is_running:
        right_knob.check_input()
        left_knob.check_input()
        main_button.check_input()
        sleep(0.001)

finally:
    GPIO.cleanup()
