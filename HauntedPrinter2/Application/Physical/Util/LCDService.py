from RPLCD import i2c

class LCDService:
	def __init__(self):
		# Set up LCD
		lcdmode = 'i2c'
		cols = 16
		rows = 2
		charmap = 'A00'
		i2c_expander = 'PCF8574'
		address = 0x27
		port = 1
		self.lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap, cols=cols, rows=rows)
		self.previous_input = ""

	
	def update_display(self, input):
        self.lcd.clear()
        self.lcd.write_string(input)
        self.previous_input = input