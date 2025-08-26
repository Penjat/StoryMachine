from RPi import GPIO
from time import sleep
import time

import board
import busio
import serial

from MainMenu import *
from KnobInput import *
from RPLCD import i2c
import adafruit_thermal_printer

# Set up Knobs and Buttons
GPIO.setmode(GPIO.BCM)
left_knob = Knob(23,24)
right_knob = Knob(17,27)
main_button = PressButton(18)

# Set up printer
ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.64)
RX = board.RX
TX = board.TX
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
printer = ThermalPrinter(uart, auto_warm_up=False)
printer.warm_up()

# Set up LCD
lcdmode = 'i2c'
cols = 16
rows = 2
charmap = 'A00'
i2c_expander = 'PCF8574'
address = 0x27
port = 1
lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap, cols=cols, rows=rows)

# Set up Menu
menu = Menu()
menu.display_output.subscribe(lambda x: process_display_output(x))
menu.printer_output.subscribe(lambda x: process_printer_output(x))

main_button.output_subject.subscribe(lambda x: process_center_press(x))
left_knob.output_subject.subscribe(lambda x: process_left_knob(x))
right_knob.output_subject.subscribe(lambda x: process_right_knob(x))

def process_display_output(output):
    lcd.clear()
    lcd.write_string(output)

def process_printer_output(output):
    print(output)
    printer.print(output)

def process_left_knob(input):
    menu.left_knob_input.on_next(input)

def process_right_knob(input):
    menu.right_knob_input.on_next(input)

def process_center_press(input):
    # menu.center_button_input.on_next(input)
    printer.print("hi")

running = True

try:
    while running:
        right_knob.check_input()
        left_knob.check_input()
        main_button.check_input()
        sleep(0.001)

finally:
    GPIO.cleanup()
    
