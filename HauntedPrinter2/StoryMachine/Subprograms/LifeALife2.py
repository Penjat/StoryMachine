from openai import OpenAI
import json
from string import Template
from enum import Enum
from rx.subject import Subject, BehaviorSubject
import requests
from PIL import Image
from numpy import asarray
import os

class Story:
	def __init__(self, species, intro_chapter):
		self.species = species
		self.chapters= [intro_chapter]
		self.is_finished = False

	@property
	def chapter_number(self):
		return len(self.chapters)

	@property
	def current_chapter(self):
		return self.chapters[-1]

	def previous_messages(self):
		return [{"role": "assistant", "content": chapter.json_string()} for chapter in self.chapters]

class Chapter:
	user_choice = None
	def __init__(self, text, image, choices):
		self.text = text
		self.image = image
		self.choices = choices

	def json_string(self):
		dict = {}
		dict['text'] = self.text
		dict['image'] = self.image
		dict['choices'] = self.choices

		return json.dumps(dict)

class LifeALife:
	class State(Enum):
		LOADING = 0
		READY = 1
		THE_END = 2

	def __init__(self, display_output, printer_output, key):
		print("starting story machine")
		self.is_playing = True
		self.story = None
		self.state = LifeALife.State.LOADING
		self.client = OpenAI(api_key=key)

		self.display_output = display_output
		self.printer_output = printer_output

		self._current_selection = 0.0
		self._menu_selection = 0.0
		
		self.update_display()
		self._start_story()

	#-------------------Story---------------------
	@property
	def current_choice(self):
		return self.current_choices[int(self._current_selection)%len(self.current_choices)]

	@property
	def current_choices(self):
		return self.story.current_chapter.choices

	def progress_story(self):
		if self.state == LifeALife.State.THE_END or self.story == None:
			self._start_story()
			return

		self._next_chapter(self.current_choice)


	def _start_story(self):
		self.state = LifeALife.State.LOADING
		response = self.send_request(self.starting_messages())
		j = json.loads(response.choices[0].message.content)
		species = j["species"]
		self.save_species(species)
		intro_chapter = Chapter(j["text"], j["image"], j["choices"])
		
		self.print_title(species)
		self.print_chapter(j["text"])
		self._print_image(j["image"])

		self.story = Story(species, intro_chapter)
		self.state = LifeALife.State.READY
		self.update_display()

	def _next_chapter(self, choice):
		self.state = LifeALife.State.LOADING
		messages = self.starting_messages() + self.story.previous_messages() + [{"role": "user", "content": choice}]
		response = self.send_request(messages)
		j = json.loads(response.choices[0].message.content)
		choices = j.get("choices")

		if len(choices) > 0 :
			chapter = Chapter(j["text"], j["image"], choices)
			self.story.chapters.append(chapter)
			
			self.print_chapter(j["text"])
			self._print_image(j["image"])
			self.state = LifeALife.State.READY
			self.update_display()
			return

		self.print_chapter(j["text"])
		self._print_image(j["image"])
		self.printer_output.on_next(("print text", "THE END", ["L", "C", "bold"]))
		self.state = LifeALife.State.THE_END
		
		self.update_display()

	def _print_image(self, prompt):
		url = self._generate_image(prompt)
		data = self._fetch_image(url)
		self.printer_output.on_next(("print array", data))

	def print_title(self, title):
		self.printer_output.on_next(("print text", title, ["L", "C", "bold"]))

	def print_chapter(self, chapter):
		self.printer_output.on_next(("print text", chapter, []))
		self.printer_output.on_next(("feed", 1))

	def get_previous_species(self):
		# Get the directory of the current script
		script_dir = os.path.dirname(os.path.abspath(__file__))

		# Define the relative path of the file to load
		file_name = "previous_animals.txt"
		file_path = os.path.join(script_dir, file_name)
		

		# Load text from the file
		with open(file_path, "r") as file:
			loaded_text = file.read()
			return loaded_text

		return ""

	def save_species(self, species):
		# Get the directory of the current script
		script_dir = os.path.dirname(os.path.abspath(__file__))

		# Define the relative path of the file to load
		file_name = "previous_animals.txt"
		file_path = os.path.join(script_dir, file_name)

		with open(file_path, "a") as file:
			file.write(", " + species)
		

	def update_display(self):
		if self._menu_selection != 0.0:
			self.display_output.on_next("main menu")
			return

		if self.state == LifeALife.State.LOADING:
			self.display_output.on_next("loading...")
			return

		if self.state == LifeALife.State.READY:
			self.display_output.on_next(self.current_choice)
			return

		if self.state == LifeALife.State.THE_END:
			self.display_output.on_next("press to start")

	def starting_messages(self):
		return [{"role": "system", "content": self.system_prompt()},
	{"role": "system", "content": "START_STORY"},
	{"role": "assistant", "content": '{"species": "Penguine", "text": "You hatch from a small egg in the harsh cold of Antarctica. Your fluffy down keeps you warm as you huddle close to your parent. You watch as other penguin chicks waddle around, eager to explore their icy world.", "image": "A woodcut style, black and white illustration of penguin chicks in Antarctica. The chicks, some sleeping and others waddling, are depicted with detailed carvings showing their fluffy down against a stark icy background.", "choices": "["Explore", "Eat", "Swim", "Play"]"}'},
	{"role": "user", "content": "Explore"},
	{"role": "assistant", "content": '{"text": "Excited to see more of the icy expanse, you waddle away from the safety of the nest. The vast stretch of ice dazzles you as you move further from the colony. Suddenly, you notice a seal approaching with hungry eyes.", "image": "A black and white woodcut illustration of a curious penguin chick, depicted in stark contrast against a vast ice field, noticing a distant seal. The tension in the scene is captured through intricate carving details.", "choices": ["Run", "Hide", "Distract", "Fight"]}'},
	
	{"role": "user", "content": "Distract"},
	{"role": "assistant", "content": '{"text": "You flap your little flippers and make a lot of noise, trying to distract the seal from noticing you. Your efforts pay off as the seal seems momentarily confused. However, it quickly refocuses on you, ready to strike. What will you do next?", "image": "A dynamic woodcut style scene in black and white, showing a penguin chick energetically distracting a seal on icy plains. The chick’s flippers and the puzzled seal are carved in high detail.", "choices": ["Peck", "Jump", "Dive", "Wait"]}'},
	{"role": "user", "content": "Peck"},
	{"role": "assistant", "content": """{"text": "Boldly, you peck at the seal's flippers with all your tiny might. Surprised by your courage, the seal backs away, giving you a chance to waddle quickly back to the safety of the colony. The other penguins cheer for your bravery.", "image": "A black and white woodcut depiction of a penguin chick attacking a seal’s flippers. The scene is dramatic, with the backdrop of a cheering penguin colony intricately carved to show texture and movement.", "choices": ["Grow Up", "Think", "Fish Hunt", "Mate"]}"""},
	{"role": "user", "content": "Mate"},
	
	{"role": "assistant", "content": """{"text": "You have matured into a strong adult penguin with sleek feathers ready to find a mate. Amongst the colony, you catch the eye of a charming penguin with a playful demeanor. Together, you form a strong bond, ready to start a family of your own.", "image": "A romantic woodcut style, black and white portrait of two adult penguins standing close and affectionately looking into each other’s eyes, set against a detailed backdrop of their icy colony.", "choices": ["Raise Chicks", "Waddle Together", "Rest", "Dance"]}"""},
	{"role": "user", "content": "Raise Chicks"},
	{"role": "assistant", "content": """{"text": "You and your mate successfully raise several batches of chicks over the years. You see them grow and eventually waddle off to start their own families. As time passes, you live a full life surrounded by the love of your mate and the community. You die peacefully of old age, having lived a full and satisfying life.\\nThe End", "image": "A poignant, black and white woodcut scene showing an old penguin surrounded by its family and looking over a bustling colony. The intricate carvings highlight the texture of the penguins' feathers and the snowy environment.", "choices": []}"""},
	{"role": "system", "content": "START_STORY"}]


	def system_prompt(self):
		previous_species = self.get_previous_species()
		species_text = "Species will be a random choice. Do not use previously generated species: " + previous_species
		return f"""You are a game that lets the user play as any species on the planet Earth. You will respond in JSON format. When prompted by the system to START_STORY, you will respond with keys for species, text, image, and choices.
	{species_text}.
	Text will describe the scene in complete sentences, initially depicting the animal's infancy and later showing results of user choices.
	Image descriptions should detail a black and white, woodcut-style scene, including specific environmental and behavioral elements.
	Choices will present 4 possible actions relevant to the text, each in 1 to 3 words, totaling no more than 20 letters. Do not offer the same choice more than once in the same story.  
	The narrative should span 3 to 7 chapters. If reaching 7 chapters, ensure the story naturally concludes with the animal dying of old age. The game ends when the animal dies, either of old age or other causes, at which point you must immediately append "The End" to the text and return an empty array for choices.
	Always end the story clearly with "The End" to signal its conclusion. This rule is absolute, regardless of the story’s length or how it ends. An empty array for choices should accompany this ending, indicating no further actions are possible.  """

	#-------------------Network---------------------
	def _generate_image(self, prompt):
		print(prompt)
		response = self.client.images.generate(
		  model="dall-e-3",
		  prompt=prompt,
		  size="1024x1024",
		  quality="standard",
		  n=1,
		)
		print(response)
		url = response.data[0].url
		return url

	def _fetch_image(self, url):
		print(url)
		data = requests.get(url).content

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

	def send_request(self, messages):
		return self.client.chat.completions.create(
		model="gpt-3.5-turbo-0125",
		temperature=1.5,
		response_format={ "type": "json_object" },
		messages=messages)

	#-------------------Inputs---------------------

	def process_right_knob(self, event):
		self._menu_selection = 0.0
		if event == "up":
			self._current_selection += 0.5
		if event == "down":
			self._current_selection -= 0.5
		self.update_display()

	def process_left_knob(self, event):
		if event == "up":
			self._menu_selection += 0.5
		if event == "down":
			self._menu_selection -= 0.5
		self.update_display()

	def process_center_press(self, event):
		if self._menu_selection != 0:
			self.printer_output.on_next("main menu")
			return
			
		self.progress_story()

	#------------------------------------------------