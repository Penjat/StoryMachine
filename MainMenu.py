from time import sleep
import time
import rx
from rx import operators as ops
from rx.subject import Subject
import os

class Menu:
    def __init__(self):
        self.left_knob_input = Subject()
        self.right_knob_input = Subject()
        self.center_button_input = Subject()

        self.display_output = Subject()
        self.printer_output = Subject()

        self.current_selection = 0.0
        self.menu_items = ["selfie", "sample text","story"]

        self.left_knob_input.subscribe(lambda x: self.process_left_knob(x))
        self.right_knob_input.subscribe(lambda x: self.process_right_knob(x))
        self.center_button_input.subscribe(lambda x: self.process_press(x))

    def process_left_knob(self, event):
        global current_selection
        if event == "up":
            self.current_selection += 1
        if event == "down":
            self.current_selection -= 1
        self.update_display()
            
    def process_right_knob(self, event):
        if event == "up":
            print("right up")
        if event == "down":
            print("right down")

    def process_press(self,event):
        if event == "pressed":
            output = self.menu_items[int(self.current_selection)%len(self.menu_items)]
            self.printer_output.on_next(output)
            return
        
    def update_display(self):
        output = self.menu_items[int(self.current_selection)%len(self.menu_items)]
        self.display_output.on_next(output)
    

    