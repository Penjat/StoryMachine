import os
import curses
from rx.subject import Subject
from matplotlib import pyplot

from rich.live import Live

from rich.prompt import Prompt
# from rich import print
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

import keyboard

# Services
from .Service.PrinterServiceTerminal import *
from .Service.ControlServiceTerminal import *
from .Service.CameraServiceTerminal import *
from StoryMachine import StoryMachine

from Ref.Keys import openai_key

from time import sleep

# ------------------------------------Functions-------------------------------

class StoryMachineTerminal:
	def __init__(self):
		# Story Machine
		self.control_service = ControlServiceTerminal()
		self.printer_service = PrinterServiceTerminal()
		self.story_machine = StoryMachine.StoryMachine(self.control_service, self.printer_service, CameraServiceTerminal(), openai_key)

		# UX
		self.story_machine.display_output.subscribe(lambda x: self.process_display_output(x))
		self.printer_service.print_history_subject.subscribe(lambda x: self.process_printer_output(x))
		self.clear_screen()

		# Init
		self.printer_output_history = ["start"]
		self.printer_menu_display = "hello"
	def run_app(self):
		try:	
			with Live(self.show_layout(), refresh_per_second=4, screen=True) as live:
				while self.story_machine.running:
					self.check_key_press()	
					sleep(0.4)
					live.update(self.show_layout())
			
		finally:
			print("done")

	def clear_screen(self):
		os.system('cls' if os.name == 'nt' else 'clear')

	def check_key_press(self):

		if keyboard.is_pressed('x'):
			self.control_service.main_button_subject.on_next("pressed")
			sleep(0.1)

		if keyboard.is_pressed('a'):
			self.control_service.left_knob_subject.on_next("up")
			sleep(0.1)

		if keyboard.is_pressed('d'):
			self.control_service.left_knob_subject.on_next("down")
			sleep(0.1)

		if keyboard.is_pressed('q'):
			self.control_service.right_knob_subject.on_next("up")
			sleep(0.1)

		if keyboard.is_pressed('e'):
			self.control_service.right_knob_subject.on_next("down")
			sleep(0.1)


	# Update Display

	def process_display_output(self, output):
		print(output)
		self.printer_output_history.append(output)
		self.show_layout()


	def process_printer_output(self, output):
		self.printer_menu_display = output
		self.show_layout()

	def show_layout(self):
		self.clear_screen()
		layout = Layout()
		layout.split_column(
		    Layout(name="upper"),
		    Layout(name="lower")
		)

		layout["upper"].update(Layout(Panel("nothing yet...",title="history", title_align="center", padding=1)))

		layout["lower"].size = 5


		grid = Table.grid(expand=True)
		grid.add_column(justify="center", ratio=1)

		grid.add_row(self.printer_menu_display)
		layout["lower"].update(Layout(Panel(grid,title="actions", title_align="center", padding=1)))

		return layout




