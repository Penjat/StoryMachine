import os
from PIL import Image, ImageOps
import numpy as np
from numpy import asarray
from random import randint
import random



class TarotReader:
    def __init__(self, display_output, printer_output):
        self.display_output = display_output
        self.printer_output = printer_output
        self.menu_items = ["main menu", "B&W", "print card"]
        self.inversion_options = ["normal", "inverted", "random"]
        self._current_selection = 0.0


    @property
    def selection(self):
        return self.menu_items[int(self._current_selection)%len(self.menu_items)]

    def tarot_reading(self):
        file_name = random.choice(os.listdir("/home/pi/Documents/PNG"))
        load_img_rz = Image.open("/home/pi/Documents/PNG/%s" %file_name).convert('1').resize((384,726))
        data = asarray(load_img_rz)
        inverter = lambda x: 1-x
        data = inverter(data)

        return data
        
    def print_tarot_reading(self):
        data = self.tarot_reading()
        self.printer_output.on_next(("print array", data))

    def update_display(self):
        self.display_output.on_next(self.selection)

# --------------- Input Methods -----------------

    def process_right_knob(self, event):
        global current_selection
        if event == "up":
            self._current_selection += 0.5
        if event == "down":
            self._current_selection -= 0.5
        self.update_display()
    

    def process_left_knob(self, event):
        print("MazeMaker recieving right input")

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