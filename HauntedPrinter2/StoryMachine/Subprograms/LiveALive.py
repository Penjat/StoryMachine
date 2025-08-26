import os
from time import sleep
import openai
import json
import requests
from PIL import Image, ImageOps
from numpy import asarray 
import re

class LiveALive:
    PROMPT = "Live-a-Life is a game where the player starts as an infant of any species and lives an entire life. The player makes choices along the way that guide a series of events. The player could start as a spider, a bird, a whale, a bacterium, a tree, or anything else. Each chapter represents approximately 1/6 of the creature's lifetime. For every chapter, a description of an image is generated. The game ends at the natural end of the creature's life. Each story consists of six chapters, and each chapter is between 50 and 150 words long. The chapter labels should not contain spaces (e.g., Chapter1 instead of Chapter 1).\n\nSpecies: Mallard Duck\nChapter1: You have just hatched from your shell, and it seems you are a duck... Nice! You see and hear your siblings around you, chirping for food.\nImage: A nest of newly hatched Mallard ducks.\nChoices: lead, follow, leave, find humans\nPlayer: lead\nChapter2: You have been determined to be the leader of the group of hatchlings. Someone has to be in charge, right? You lead your flock on adventures, scouting out food sources and finding excellent swimming spots.\nImage: A large Mallard Duck pointing with its wing, while several other ducks look in that direction.\nChoices: find food, find mate, explore, meditate\nPlayer: find mate\nChapter3: You have split from your flock to find a mate. You stop at a pond and lay eyes on the most beautiful duck you have ever seen!\nImage: A male Mallard duck with its mouth wide open, looking at a very attractive female duck who is staring back seductively.\nChoices: quack, swim, dance, fly away\nPlayer: dance\nChapter4: You decide to impress her with your amazing dance moves, and it works! The two of you fall in love.\nImage: A Mallard duck dancing wildly while another duck watches.\nChoices: build nest, explore, return to family, leave mate\nPlayer: build nest\nChapter5: You and your mate have successfully built a nest and started a family. You take turns searching for food and defending the nest while the other watches over the eggs. You are now the parent of several ducklings!\nImage: Two ducks staring at several newly hatched ducklings.\nChoices: teach foraging, teach fighting, teach dancing, leave family\nPlayer: teach dancing\nChapter6: You teach your children to dance, hoping it will work the same magic for them as it did for you. You watch your children grow up. Some stay with you, while others fly off for new adventures. One day, you pass away peacefully, surrounded by your family.\nImage: A deceased duck looking peaceful, with several other ducks looking sad.\nTHE END\n\nSpecies:"
    def __init__(self, display_output, printer_output, key):
        self.display_output = display_output
        self.printer_output = printer_output

        self.menu_items = ["main menu", "play game", "main menu", "play game"]
        self._current_selection = 0.0
        self.current_chapter = 0

        self.debug_mode = False
        self.print_calls = False

        self.GPT_error = False
        self.species = ""
        self.text_so_far = ""
        self.current_choices = []

        self.is_playing = False
        self.is_loading = False


        openai.api_key = key

        self.update_display()

    @property
    def selection(self):
        return self.menu_items[int(self._current_selection)%len(self.menu_items)]

    @property
    def current_choice(self):
        return self.current_choices[int(self._current_selection)%len(self.current_choices)]
    

    def update_display(self):
        if self.GPT_error == True:
            self.display_output.on_next("Error")
            return

        if self.is_loading:
            self.display_output.on_next("please wait")
            return

        if self.is_playing:
            self.display_output.on_next(self.current_choice)
            return

        self.display_output.on_next(self.selection)



    def fetch_response(self, prompt):
        print("==========================")
        print("fetch Prompt: ", prompt)
        response = openai.Completion.create(
          model="gpt-4",
          prompt= prompt,
          temperature=1.08,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0.2,
          presence_penalty=0,
          stop=["Player:", "THE END"]
        )
        print("RESPONSE:", response)
        print("==========================")
        return response

    def parse_response(self, response):
        text = response["choices"][0]["text"]

        chapter_match = re.search(r"Chapter\d+:(.+?)\n", text)
        image_match = re.search(r"Image:(.+?)\n", text)
        choices_match = re.search(r"Choices:(.+?)\n", text)

        # Get the extracted parts
        chapter = chapter_match.group(1).strip() if chapter_match else None
        image = image_match.group(1).strip() if image_match else None
        choices = choices_match.group(1).strip() if choices_match else None

        return chapter, image, choices

    def add_response_to_text(self, chapter, image, choices):
        self.text_so_far += f"\nChapter{self.current_chapter}: {chapter}\nImage: {image}\nChoices: {choices}"

    def start_story(self):
        print("starting story...")
        self.current_chapter = 1
        self.text_so_far = ""

        self.is_loading = True
        self.update_display()


        response = self.fetch_response(self.PROMPT)

        self.species = response["choices"][0]["text"].split('\n', 1)[0]
        chapter, image, choices = self.parse_response(response)

        
        self.print_title(self.species)
        self.text_so_far += self.species
        # print("Species:", self.species)
        img_data = self.fetch_image(image)
        self.printer_output.on_next(("print array", img_data))

        self.print_chapter(chapter)
        # print("Image:", image)

        if choices == None:
            # This shouldn't happen
            self.print_title("THE END")
            self.is_playing = False
        else:
            self.current_choices = choices.split(', ')
            print("Choices:", choices)
            self.add_response_to_text(chapter, image, choices)

        self.is_loading = False
        self.update_display()

    def process_choice(self, input):
        self.is_loading = True
        self.update_display()

        self.current_chapter += 1
        self.text_so_far += f"\nPlayer: {input}"
        response = self.fetch_response(self.PROMPT + self.text_so_far)

        chapter, image, choices = self.parse_response(response)
        if chapter == None:
            self.GPT_error = True
            self.update_display()
            return

        self.show_response(chapter, image, choices)
        
    def show_response(self, chapter, image, choices):
        img_data = self.fetch_image(image)
        self.printer_output.on_next(("print array", img_data))
        self.print_chapter(chapter)
        # print("Chapter:", chapter)
        # print("Image:", image)

        if choices == None:
            self.print_title("THE END")
            self.is_playing = False
        else:
            self.current_choices = choices.split(', ')
            # print("Choices:", choices)
            self.add_response_to_text(chapter, image, choices)

        self.is_loading = False
        self.update_display()

    def print_title(self, title):
        if self.debug_mode:
            print(title)
            return
        else:
            self.printer_output.on_next(("print text", title, ["L", "C", "bold"]))

    def print_chapter(self, chapter):
        if self.debug_mode:
            print(chapter)
            return
        else:
            self.printer_output.on_next(("print text", chapter, []))
            self.printer_output.on_next(("feed", 1))

    def fetch_image(self, image_description):
        img_response = openai.Image.create(
          prompt=f'Black and white woodcut style image of {image_description}',
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

        return img_data
    def retry(self):
        self.GPT_error = False
        self.is_loading = True
        self.update_display()

        response = self.fetch_response(self.PROMPT + self.text_so_far)
        chapter, image, choices = self.parse_response(response)
        if chapter == None:
            self.GPT_error = True
            self.update_display()
            return
        self.show_response(chapter, image, choices)

# --------------- Input Methods -----------------

    def process_right_knob(self, event):
        if event == "up":
            self._current_selection += 0.5
        if event == "down":
            self._current_selection -= 0.5
        self.update_display()
    

    def process_left_knob(self, event):
        return

    def process_center_press(self, event):
        if event == "pressed":
            if self.GPT_error == True:
                self.retry()
                return
            if self.is_loading == True:
                # print("stil loading...")
                return

            if self.is_playing == True:
                # print(self.current_choice)
                self.process_choice(self.current_choice)
                return



            if self.selection == "play game":
                # is_loading = True

                self.is_playing = True
                self.start_story()
                return
            if self.selection == "main menu":
                self.printer_output.on_next(self.selection)
                return
                
            else:
                print("did not recognize selection {self.selection}")
 




