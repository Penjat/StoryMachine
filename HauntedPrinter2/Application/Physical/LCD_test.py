
from RPLCD import i2c
import time
from time import sleep
import string
import random
import math



class MenuAnimator:
	def __init__(self):

class LCDService:
	def __init__(self):

		self.title = ""
		self.new_title = None
		self.last_time = time.time()

		self.configuration = {"center_title": True }

		self.animation_frame = 16

		# Set up LCD
		lcdmode = 'i2c'
		cols = 16
		rows = 2
		charmap = 'A00'
		i2c_expander = 'PCF8574'
		address = 0x27
		port = 1
		self.lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap, cols=cols, rows=rows)

	def set_title(self, title):

		self.title = title
		self.lcd.clear()
		if self.configuration["center_title"] == True:
			cursor_offset = math.floor((16 - len(title))/2)
			self.lcd.cursor_pos = (0, cursor_offset)

		
		self.lcd.write_string(title)

	def update_display(self):

		# updating display
		delta_time = time.time() - self.last_time
		self.last_time = time.time()
		


lcd_service = LCDService()

lcd_service.set_title("hello")

while True:
	lcd_service.update_display()
	sleep(0.001)

# Each tuple is 8 rows, each row = 5 bits (LSB right).
# Use 0bxxxxx where x=1 is pixel on, 0 is off.

sword = (
	0b00100,
	0b00100,
	0b00100,
	0b00100,
	0b01110,
	0b11111,
	0b01110,
	0b00100,
)

shield = (
	0b11111,
	0b10001,
	0b10101,
	0b10101,
	0b10101,
	0b10001,
	0b11111,
	0b00000,
)

fire = (
	0b00100,
	0b01110,
	0b00101,
	0b01111,
	0b11110,
	0b01100,
	0b00100,
	0b00000,
)

coin = (
	0b01110,
	0b10001,
	0b10111,
	0b10101,
	0b11101,
	0b10001,
	0b01110,
	0b00000,
)

heart = (
	0b01010,
	0b11111,
	0b11111,
	0b11111,
	0b01110,
	0b00100,
	0b00000,
	0b00000,
)

skull = (
	0b01110,
	0b10101,
	0b11111,
	0b11111,
	0b01110,
	0b01110,
	0b00000,
	0b00000,
)

arrow = (
	0b00100,
	0b00110,
	0b11111,
	0b11111,
	0b00110,
	0b00100,
	0b00000,
	0b00000,
)

smiley = (
	0b00000,
	0b01010,
	0b00000,
	0b00000,
	0b10001,
	0b01110,
	0b00000,
	0b00000,
)

# icons = [sword, shield, fire, coin, heart, skull, arrow, smiley]

# for i, icon in enumerate(icons):
#     lcd.create_char(i, icon)



# How big is the lcd? 16/2?
# Make a letter go across the screen
# for i in range(32):
# 	text = "oooooooooooooooooooooooooooooooo" 
# 	text = text[:i] + "x" + text[i+1:]
	
# 	lcd.write_string(text)
# 	sleep(0.01)

icon_ref = ["\x00","\x01","\x02","\x03","\x04","\x05","\x06","\x07"]

# Make a letter explosion
# for i in range(32):
	
	 
# output_array = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]   




# Everything flashing random

# output_array = []#[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]
# chars = string.printable[:-5]
# 	# # for i in range(32):
# 	# # 	output_array.append(random.choice(chars))
# 	# lcd.cursor_pos = (idy, idx)
# 	# lcd.write_string("hello")
#     on_switch = false
# while True:
# 	# output_array = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]
	
# 	idx = random.randrange(16)
# 	idy = random.randrange(2)
# 	lcd.cursor_pos = (idy, idx)
# 	lcd.write_string(random.choice(chars))

#     lcd.cursor_pos = (0, 2)
#     my_string = 
#     lcd.write_string(hello)


# 	sleep(0.001)













# Usage: write special chars with \x00 ... \x07
# lcd.write_string("\x00\x01\x02\x03\x04\x05\x06\x07")



