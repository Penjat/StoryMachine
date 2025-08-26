from RPi import GPIO
from RPLCD import i2c
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

from .Util.KnobInput import *
from .Adafruit_Thermal import *

from picamera import PiCamera
import picamera

from PIL import Image, ImageOps
import numpy as np
from numpy import asarray
from StoryMachine import StoryMachine


import os

from Ref import Keys

# Set up Knobs and Buttons
GPIO.setmode(GPIO.BCM)


dtr_pin = 10
GPIO.setup(dtr_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Set up printer
# ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.64)
RX = board.RX
TX = board.TX

class ControlServicePhysical:
	def __init__(self):
		self.left_knob = Knob(23,24)
		self.right_knob = Knob(17,27)
		self.main_button = PressButton(18)

		self.main_button_subject = self.main_button.output_subject
		self.left_knob_subject = self.left_knob.output_subject
		self.right_knob_subject = self.right_knob.output_subject

	def check_input(self):
		self.right_knob.check_input()
		self.left_knob.check_input()
		self.main_button.check_input()

class PrinterServicePhysical:
	def __init__(self):
		print("init printer.")
		self.printer = Adafruit_Thermal("/dev/serial0", 9600, timeout=5)

	def convert_byte1(self, byte):
		i = 1
		val = 0
		for bit in byte:
			if bit == 1:
				val += i
			i = i*2
		return val

	def print_array(self, input_array):
		input_array = self._pad_width_to_multiple_of_8(input_array)
			
		my_array = input_array.reshape(-1,8)
		my_array = np.flip(my_array, 1)
		vectorized_convert_byte = np.vectorize(self.convert_byte1, signature='(n)->()')
		byte_array = vectorized_convert_byte(my_array)
		   
		self.printer.printBitmap(input_array.shape[1], input_array.shape[0], byte_array, True)
		

	def print_text(self, text, options=[]):
		size='S'
		justify='L'
		newLine=True
		self.printer.normal()

		if 'Right' in options:
			justify = 'R'
		if 'Center' in options:
			justify = 'C'

		if 'Upsidedown' in options:
			self.printer.upsideDownOn()

		if 'L' in options:
			size = 'L'
		if 'M' in options:
			size = 'M'

		if 'Bold' in options:
			self.printer.boldOn()

		if 'no line' in options:
			newLine = false

		if 'Underline' in options:
			self.printer.underlineOn(weight=2)

		if 'DH' in options:
			self.printer.doubleHeightOn()

		if 'DW' in options:
			self.printer.doubleWidthOn()

		wrap_limit = 16 if (size == 'L') else 32
		text = self.wrap_text(text, wrap_limit)

		self.printer.setSize(size)
		self.printer.justify(justify)
		if newLine:
			self.printer.println(text)
		else:
			self.printer.print(text)

	def wrap_text(self, text, limit):
		# print(text)
		if len(text) >= limit:
			substring = text[0:32]
			index = substring.rfind(' ')
			# print("index is ", index)
			#TODO case where is no space
			if index == -1 or index == 0:
				
				index = limit-1

			return text[0:index] + '\n' + self.wrap_text(text[index:], limit)

		return text

	def _pad_width_to_multiple_of_8(self, arr):
		current_width = arr.shape[1]
		padding_needed = (8 - current_width % 8) % 8
		
		if padding_needed > 0:
			padded_arr = np.pad(arr, pad_width=((0, 0), (0, padding_needed)), mode='constant', constant_values=0)
			return padded_arr
		else:
			return arr

	def feed(self, number_lines):
		print("feed")
		self.printer.feed(number_lines)

class CameraServicePhysical:
	def __init__(self):
		self.camera = PiCamera()

	def camera_image(self):
		stream = BytesIO()
		self.camera.start_preview()
		sleep(1)
		self.camera.capture(stream, format='jpeg')
		self.camera.stop_preview()
		# "Rewind" the stream to the beginning so we can read its content
		stream.seek(0)
		image = ImageOps.invert(Image.open(stream))
		return image.resize((384,384))

	def image_to_array(self, image):
		return np.array(asarray(image.convert('1')))

	def image_to_array2(self, image):
		array = np.array(asarray(image))
		
		array = np.mean(array, axis=2)
		array[array <= 180] = 0
		array[array > 180] = 1
		return array
		

class StoryMachinePhysical:
	def __init__(self):
		# Story Machine
		self.control_service = ControlServicePhysical()
		self.printer_service = PrinterServicePhysical()
		self.camera_service = CameraServicePhysical()
		key = Keys.openai_key
		self.story_machine = StoryMachine.StoryMachine(self.control_service, self.printer_service, self.camera_service, key)
		
		
		self.lcd = self.set_up_lcd()

		self.story_machine.display_output.subscribe(lambda x: self.update_lcd(x))

		
	def set_up_lcd(self):
		# Set up LCD
		lcdmode = 'i2c'
		cols = 16
		rows = 2
		charmap = 'A00'
		i2c_expander = 'PCF8574'
		address = 0x27
		port = 1
		return i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap, cols=cols, rows=rows)
	
	def update_lcd(self, input):
		if isinstance(input, list):
			print("The value is a list.")
			self.lcd.clear()
			self.lcd.cursor_pos = (0, 0)
			self.lcd.write_string(input[0])
			self.lcd.cursor_pos = (1, 0)
			self.lcd.write_string(input[1])
		elif isinstance(input, str):
			print("The value is a string.")
			self.lcd.clear()
			self.lcd.write_string(input)
			
		else:
			print("The value is neither a list nor a string.")
			print("update lcd")
		


	def run_app(self):
		
		# update_display()
		self.lcd.clear()
		self.lcd.write_string("...wellcome...")

		sleep(1)
		
		try:
			while self.story_machine.isRunning:
				self.control_service.check_input()
				sleep(0.001)

		finally:
			GPIO.cleanup()

	




