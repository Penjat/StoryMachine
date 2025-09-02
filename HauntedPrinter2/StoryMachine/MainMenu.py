from time import sleep
import time
import rx
from rx import operators as ops
from rx.subject import Subject
import os

class Menu:
    def __init__(self, display_output, printer_output):
        self.left_knob_input = Subject()
        self.right_knob_input = Subject()
        self.center_button_input = Subject()

        self.display_output = display_output
        self.printer_output = printer_output

        self.current_selection = 0
        # self.menu_items = ["take pic","contrast pic","Maze Maker","Tarot Reading", "print pic", "alt tarot", "LifeALife", "feed","quit", "test"]

        self.menu_items = ["quit", "camera", "contrast camera", "Maze Maker", "Bluetooth", "CellularAutomata"]

        self.left_knob_input.subscribe(lambda x: self.process_left_knob(x))
        self.right_knob_input.subscribe(lambda x: self.process_right_knob(x))
        self.center_button_input.subscribe(lambda x: self.process_press(x))
        

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
    

    