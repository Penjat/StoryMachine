from MainMenu import *
import pygame
import rx
from rx import operators as ops

from colorama import init as colorama_init
from colorama import Fore, Back, Style

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    KEYUP,
    QUIT,
)

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

menu = Menu()
menu.display_output.subscribe(lambda x: process_display_output(x))
menu.printer_output.subscribe(lambda x: process_printer_output(x))

total_printer_output = []
display_output = ""
os.system('clear')

def process_display_output(output):
	global display_output
	display_output = output
	os.system('clear')
	print_total_output()
	show_controls()


def process_printer_output(output):
	os.system('clear')
	global total_printer_output
	total_printer_output.append(output)
	print_total_output()
	show_controls()
	
def show_controls():
	global display_output
	print(Back.BLUE + Fore.WHITE + display_output)
	print(Style.RESET_ALL)

def print_total_output():
	global total_printer_output
	for line in total_printer_output:
		print(line)

print("starting virtual story machine...")

running = True

try:
	while running:
    	# def check_inputs(self):
        # self.controls.right_knob.check_input()
        # self.controls.left_knob.check_input()
        # self.controls.main_button.check_input()

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
				elif event.key == K_UP:
					menu.left_knob_input.on_next("up")
				elif event.key == K_DOWN:
					menu.left_knob_input.on_next("down")
				elif event.key == K_RIGHT:
					menu.right_knob_input.on_next("up")
				elif event.key == K_LEFT:
					menu.right_knob_input.on_next("down")
				elif event.key == K_SPACE:
					menu.center_button_input.on_next("pressed")
			if event.type == KEYUP:
				if event.key == K_SPACE:
					menu.center_button_input.on_next("released")
			elif event.type == QUIT:
				running = False
        
		sleep(0.001)
finally:
	print("done")
#     GPIO.cleanup()