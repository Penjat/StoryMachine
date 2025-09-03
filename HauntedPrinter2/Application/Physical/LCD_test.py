

# import time
# from time import sleep
# import string
# import random
# import math



# class RingMenu:
# 	def __init__(self, menu_items, index=0):
#         self.menu_items = menu_items
#         self.index = index

#     def update_display(self):

#         # updating display
#         delta_time = time.time() - self.last_time
#         self.last_time = time.time()

#     def add_index(self, amt):
#         self.index += amt




# lcd_service = LCDService()

# lcd_service.set_title("hello")

# while True:
# 	lcd_service.update_display()
# 	sleep(0.001)

# # Each tuple is 8 rows, each row = 5 bits (LSB right).
# # Use 0bxxxxx where x=1 is pixel on, 0 is off.

# sword = (
# 	0b00100,
# 	0b00100,
# 	0b00100,
# 	0b00100,
# 	0b01110,
# 	0b11111,
# 	0b01110,
# 	0b00100,
# )

# shield = (
# 	0b11111,
# 	0b10001,
# 	0b10101,
# 	0b10101,
# 	0b10101,
# 	0b10001,
# 	0b11111,
# 	0b00000,
# )

# fire = (
# 	0b00100,
# 	0b01110,
# 	0b00101,
# 	0b01111,
# 	0b11110,
# 	0b01100,
# 	0b00100,
# 	0b00000,
# )

# coin = (
# 	0b01110,
# 	0b10001,
# 	0b10111,
# 	0b10101,
# 	0b11101,
# 	0b10001,
# 	0b01110,
# 	0b00000,
# )

# heart = (
# 	0b01010,
# 	0b11111,
# 	0b11111,
# 	0b11111,
# 	0b01110,
# 	0b00100,
# 	0b00000,
# 	0b00000,
# )

# skull = (
# 	0b01110,
# 	0b10101,
# 	0b11111,
# 	0b11111,
# 	0b01110,
# 	0b01110,
# 	0b00000,
# 	0b00000,
# )

# arrow = (
# 	0b00100,
# 	0b00110,
# 	0b11111,
# 	0b11111,
# 	0b00110,
# 	0b00100,
# 	0b00000,
# 	0b00000,
# )

# smiley = (
# 	0b00000,
# 	0b01010,
# 	0b00000,
# 	0b00000,
# 	0b10001,
# 	0b01110,
# 	0b00000,
# 	0b00000,
# )

# # icons = [sword, shield, fire, coin, heart, skull, arrow, smiley]

# # for i, icon in enumerate(icons):
# #     lcd.create_char(i, icon)



# # How big is the lcd? 16/2?
# # Make a letter go across the screen
# # for i in range(32):
# # 	text = "oooooooooooooooooooooooooooooooo" 
# # 	text = text[:i] + "x" + text[i+1:]
	
# # 	lcd.write_string(text)
# # 	sleep(0.01)

# icon_ref = ["\x00","\x01","\x02","\x03","\x04","\x05","\x06","\x07"]

# # Make a letter explosion
# # for i in range(32):
	
	 
# # output_array = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]   




# # Everything flashing random

# # output_array = []#[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]
# # chars = string.printable[:-5]
# # 	# # for i in range(32):
# # 	# # 	output_array.append(random.choice(chars))
# # 	# lcd.cursor_pos = (idy, idx)
# # 	# lcd.write_string("hello")
# #     on_switch = false
# # while True:
# # 	# output_array = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]
	
# # 	idx = random.randrange(16)
# # 	idy = random.randrange(2)
# # 	lcd.cursor_pos = (idy, idx)
# # 	lcd.write_string(random.choice(chars))

# #     lcd.cursor_pos = (0, 2)
# #     my_string = 
# #     lcd.write_string(hello)


# # 	sleep(0.001)













# # Usage: write special chars with \x00 ... \x07
# # lcd.write_string("\x00\x01\x02\x03\x04\x05\x06\x07")



