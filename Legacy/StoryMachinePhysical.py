from RPi import GPIO
from time import sleep
import time
import copy
from io import BytesIO
import sys

from random import randint

import board
import busio
import serial

import math
from MainMenu import *
from MazeMake import *
from KnobInput import *

from RPLCD import i2c
from Adafruit_Thermal import *
import adafruit_thermal_printer

from picamera import PiCamera
import picamera

from PIL import Image, ImageOps
import numpy as np
from numpy import asarray

import os

# Keys
import Keys

# Sub Programs
from MazeMaker import *
from TarotReader import *
from AltTarot import *
from LiveALive import *


# Set up Knobs and Buttons
GPIO.setmode(GPIO.BCM)
left_knob = Knob(23,24)
right_knob = Knob(17,27)
main_button = PressButton(18)

dtr_pin = 10
GPIO.setup(dtr_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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

display_output = Subject()
printer_output = Subject()
display_output.subscribe(lambda x: process_display_output(x))
printer_output.subscribe(lambda x: process_printer_output(x))

# Set up Menu
menu = Menu(display_output, printer_output)

main_button.output_subject.subscribe(lambda x: process_center_press(x))
left_knob.output_subject.subscribe(lambda x: process_left_knob(x))
right_knob.output_subject.subscribe(lambda x: process_right_knob(x))


def camera_image():
    stream = BytesIO()
    camera.start_preview()
    sleep(1)
    camera.capture(stream, format='jpeg')
    camera.stop_preview()
    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)
    image = ImageOps.invert(Image.open(stream))
    return image.resize((384,384))

def image_to_array(image):
    return np.array(asarray(image.convert('1')))

def image_to_array2(image):
    array = np.array(asarray(image))
    
    array = np.mean(array, axis=2)
    array[array <= 180] = 0
    array[array > 180] = 1
    return array

def print_array(input_array):
    print(input_array)
    width_padding = (math.ceil(input_array.shape[0]/8) * 8) - input_array.shape[0]
    input_array = np.pad(input_array, [(0,width_padding), (0, 0)], mode='constant')
    width = input_array.shape[1]
    height = input_array.shape[0]
        
    my_array = input_array.reshape(-1,8)
    byte_array = []
    for byte in my_array:
        byte_array.append(convert_byte(byte))
       
    print("starting print")
    printer.printBitmap(width,height, byte_array)
    print("done")

def convert_byte(byte):
    i = 1
    val = 0
    for bit in np.flip(byte):
        if bit == 1:
            val += i
        i = i*2
    return val
   
def process_display_output(output):
    lcd.clear()
    lcd.write_string(output)

def process_cmd(output):
    cmd_type = output[0]

    if cmd_type == "print array":
        print("should print an array")
        print_array(output[1])
        return

    if cmd_type == "print text":
        format_options = output[2]
        text_size = "S"

        if "L" in format_options:
            text_size = "L"
        if "M" in format_options:
            text_size = "M"
        if "bold" in format_options:
            printer.boldOn()
        
        if "C" in format_options:
            printer.justify("C")
        if "R" in format_options:
            printer.justify("R")

        print_text_size(output[1], text_size)
        printer.setDefault()
        return
    if cmd_type == "feed":
        printer.feed(output[1])
        return
    else:
        print(f"command not recognized {cmd_type}")
    

def process_printer_output(output):
    global sub_program
    global display_output
    global printer_output

    print(output)

    if isinstance(output, tuple):
        print("it is a tuple")
        process_cmd(output)

    if output == "main menu":
        sub_program = 0
        menu.update_display()

    if output == "Maze Maker":
        print("starting maze maker...")
        sub_program = MazeMaker(display_output, printer_output)

    if output == "LiveALive":
        print("starting LiveALive...")
        sub_program = LiveALive(display_output, printer_output)

    if output == "take pic":
        my_array = image_to_array(camera_image())
        print_array(my_array)
        
    if output == "contrast pic":
        my_array = image_to_array2(camera_image())
        print_array(my_array)
        
    if output == "test":
        printer.boldOn()
        printer.setSize('L')
        printer.justify('C')
        print_text("INBOX")
        printer.feed(4)
        print_text("OUTBOX")
        
    
    # if output == "bible qoute":
    #     printer.justify('L')
    #     printer.setSize('S')
    #     print("random bible quote")
    #     file1 = open('bible.txt', 'r')
    #     lines = file1.readlines()
          
    #     count = 0
    #     line = random.choice(lines)
    #     print("{}".format(line.strip()))
    #     print_text("{}".format(line.strip()))

    if output == "Tarot Reading":
        print("starting Tarot Reader...")
        sub_program = TarotReader(display_output, printer_output)
        
    if output == "print pic":
        load_img_rz = Image.open("/home/pi/Documents/whale3.png").convert('1').resize((384,726))
        data = asarray(load_img_rz)
        inverter = lambda x: 1-x
        data = inverter(data)
        print_array(data)



    if output == "alt tarot":
        sub_program = AltTarot(display_output, printer_output)

    if output == "feed":
        printer.feed(1)

    if output == "quit":
        lcd.clear()
        lcd.write_string("goodbye")
        sys.exit()
        
def print_text_size(input_text, size):
    print("print text size " + size)
    printer.setSize(size)
    
    lines = wrap_for_printing(input_text, size)
    for line in lines:
        printer.println(line)
    printer.setSize('S')
   
        
def print_text(input_text):
    lines = wrap_for_printing(input_text)
    for line in lines:
        printer.println(line)
        
def wrap_for_printing(input_string, text_size = 'S'):
    print(text_size)
    if text_size == 'L':
        length_limit = 15
    else:
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


def process_left_knob(input):
    global sub_program
    if sub_program != 0:
        sub_program.process_left_knob(input)
    else:
        menu.left_knob_input.on_next(input)
    

def process_right_knob(input):
    global sub_program
    if sub_program != 0:
        sub_program.process_right_knob(input)
    
    else:
        menu.right_knob_input.on_next(input)

def process_center_press(input):
    global sub_program
    if input != "pressed":
        return

    if sub_program != 0:
        sub_program.process_center_press(input)
    else:
        menu.center_button_input.on_next(input)
    
    
running = True
sub_program = 0
# update_display()
lcd.write_string("...welcome...")

try:
    while running:
        right_knob.check_input()
        left_knob.check_input()
        main_button.check_input()
        sleep(0.001)

finally:
    GPIO.cleanup()
    
