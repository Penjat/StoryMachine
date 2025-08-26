import os
from time import sleep
import openai
import json
import requests
from PIL import Image, ImageOps
from numpy import asarray 


class AltTarot:
    def __init__(self, display_output, printer_output, key):
        self.display_output = display_output
        self.printer_output = printer_output
        self.menu_items = ["main menu", "print card", "reading"]
        self.print_reading = False
        self._current_selection = 0.0
        openai.api_key = key

    @property
    def selection(self):
        return self.menu_items[int(self._current_selection)%len(self.menu_items)]


    def tarot_reading(self):
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt="Gigi is an alternat tarot card generator and reader.  It generats an alternate origional tarot card and provides a reading as well as providing a desription of the image on the card.\n\nCard: The Knight of Sneakers\nDescription: A knight wearing sneakers.\nReading: This card suggests that you are ready to take a risk and make a bold move. The Knight of Sneakers indicates that you have the courage and strength to follow your own path, and to take action that is unconventional and daring. You are well-prepared to take on any challenge that comes your way and to make a lasting impact on your life and the lives of those around you. Do not be afraid to take risks, even if it means going against the grain. The Knight of Sneakers is a reminder that success comes from taking risks and having faith in your own abilities.\n\nCard:",
          temperature=0.92,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )

        split_txt = response["choices"][0]["text"].split('Description:')
        split_txt2 = split_txt[1].split('Reading:')

        card_name = split_txt[0]
        reading = split_txt2[1]

        description = split_txt2[0]
  
        img_response = openai.Image.create(
          prompt=f'Black and white image. A Tarot card with the image of {description}',
          n=1,
          size="512x512"
        )

        data = requests.get(img_response["data"][0]["url"]).content

        # Opening a new file named img with extension .jpg
        # This file would store the data of the image file
        f = open('img.jpg','wb')
     
        # Storing the image data inside the data variable to the file
        f.write(data)
        f.close()

        # Opening the saved image and displaying it
        img = Image.open('img.jpg').convert('1').resize((384,384))

        img_data = asarray(img)
        inverter = lambda x: 1-x
        img_data = inverter(img_data)

        return (card_name.upper(), reading, img_data)


    def print_tarot_reading(self):
        data = self.tarot_reading()
        self.printer_output.on_next(("print text", data[0], ["L", "C", "bold"]))
        self.printer_output.on_next(("feed", 1))
        self.printer_output.on_next(("print array", data[2]))

        if self.print_reading:
            self.printer_output.on_next(("print text", data[1], ["S"]))

        print(data)

    def update_display(self):
        if self.selection == "reading":
            self.display_output.on_next(f"reading: {self.print_reading}")
            return

        self.display_output.on_next(self.selection)


# --------------- Input Methods -----------------

    def process_right_knob(self, event):
        if event == "up":
            self._current_selection += 0.5
        if event == "down":
            self._current_selection -= 0.5
        self.update_display()
    

    def process_left_knob(self, event):
        print(event)
        if self.selection == "reading":
            self.print_reading = (event == "down")
            
 
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