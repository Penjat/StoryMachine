from time import sleep
import time
import rx
from rx import operators as ops
from rx.subject import Subject
import os
# from RingMenu import RingMenu

class Menu:
    def __init__(self, display_output, printer_output, menu_items):
        self.left_knob_input = Subject()
        self.right_knob_input = Subject()
        self.center_button_input = Subject()

        self.display_output = display_output
        self.printer_output = printer_output

        self.last_time = time.time()
        self.current_selection = 0

        self.menu_items = menu_items

        self.left_knob_input.subscribe(lambda x: self.process_left_knob(x))
        self.right_knob_input.subscribe(lambda x: self.process_right_knob(x))
        self.center_button_input.subscribe(lambda x: self.process_press(x))
        
    def update_display(self):
        delta_time = time.time() - self.last_time
        self.last_time = time.time()
        


    def process_right_knob(self, event):
        print("right event")
        if event == "up":
            self.current_selection += 1
        if event == "down":
            self.current_selection -= 1

        self.update_display()
        
            
    def process_left_knob(self, event):
        print("left event")
        

    def process_press(self,event):
        if event == "pressed":
            output = self.menu_items[int(self.current_selection)%len(self.menu_items)]
            self.printer_output.on_next(output)
            return
        
    def update_display(self):
        output = self.menu_items[int(self.current_selection)%len(self.menu_items)]
        self.display_output.on_next(output)
    

    