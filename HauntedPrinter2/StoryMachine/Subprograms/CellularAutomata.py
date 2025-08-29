from rx import operators as ops
from rx.subject import Subject
import numpy as np
from matplotlib import pyplot


class CellularAutomataGenerator:
	def __init__(self, display_output, printer_output):
		print("init CellularAutomataGenerator")
		self.display_output = display_output
		self.printer_output = printer_output

		self.menu_items = ["main menu", "print", "depth", "rules"]
		self._current_selection = 0.0

		self.depth = 384
		self.rule = 75
		self.pixel_size = 5

	# Given an array and rules
	# return an equal size array according to the rules
	def getNextLine(self, line, rules):
		output = []
		index = 0
		for x in line:
			left_cell = 1 if line[(index - 1) % len(line)] else 0
			right_cell = 1 if line[(index + 1) % len(line)] else 0
			middle_cell = 1 if line[(index) % len(line)] else 0

			bit_index = (left_cell << 2) + (middle_cell << 1) + right_cell
			mask = (1 << bit_index)
			value = 1 if ((rules & mask) == mask) else 0

			output.append(value)
			index += 1
		return output

	def create_array(self, depth, starting_line, rules):
		array = np.zeros((depth,int(384/self.pixel_size)))
		
		for row in range(depth):
			if row == 0:
				array[0] = starting_line[:len(array[0])]
			else:		
				array[row] = self.getNextLine(array[row-1], rules)


		array = np.repeat(array, self.pixel_size, axis=1)
		array = np.repeat(array, self.pixel_size, axis=0)
		return array


	def update_display(self):
		output = ""

		self.display_output.on_next(output)

	# --------------- Input Methods -----------------

	def process_right_knob(self, event):
		if event == "up":
			self._current_selection += 0.5
		if event == "down":
			self._current_selection -= 0.5
		self.update_display()
	

	def process_left_knob(self, event):
		print(event)
		if event == "up":
			self.rule += 1
		if event == "down":
			self.rule -= 1
 
		self.update_display()

	def process_center_press(self, event):
		if event == "pressed":
			if self.selection == "main menu":
				self.printer_output.on_next(self.selection)
				return
			if self.selection == "print card":
				self.print_tarot_reading()
				
			else:
				print("did not recognize selection {self.selection}")






display_subject = Subject()
printer_subject = Subject()

display_subject.subscribe(lambda x: print(x))
printer_subject.subscribe(lambda x: print(x))

generator = CellularAutomataGenerator(display_subject, printer_subject)

first_line = np.zeros(384)
first_line[10] = 1



pyplot.imshow(generator.create_array(100, first_line, 73))

#73, 75

pyplot.show()
