import os, random
from PIL import Image
from numpy import asarray
from matplotlib import pyplot
import json
import rx
from rx import operators as ops
from rx.subject import Subject

class StoryMaker():
	
	def __init__(self, file_name):
		self.story_state = []
		self.is_running = True
		f = open(file_name)
		data = json.load(f)
		self.nodes = data['nodes']
		f.close()

		self.current_node = Subject()
		self.choices = []
		self.current_node.subscribe(lambda x: self.process_change_node(x))
	
	def goto_story_node(self, node_id):
		if node_id == "END":
			return
		self.current_node.on_next(next(i for i in self.nodes if i["id"] == node_id))

	def process_change_node(self, new_node):
		for event in new_node["events"]:

			# Check event conditions
			# for condition in event["conditions"]:
			# 	print(condition)
			self.process_results(event["results"])
			self.process_new_choices(new_node["choices"])
		
		
	def process_new_choices(self, choices):
		self.choices = choices
		# Show Choices
		i = 0
		for choice in choices:
			# TODO: Check choices conditions
			print("(" + str(i) + ") " + choice["text"])
			i += 1


	def process_results(self, results):
		# Process the results
		for result in results:

			if result["type"] == "printText":
				print(result["data"])

			if result["type"] == "history":
				self.story_state.append(result["data"])


	def select_choice(self, choice):
		# Process choice results
		self.process_results(choice["results"])

		# goto destination
		self.goto_story_node(choice["destination"])
		
	def process_choice(self, user_input):
		i = int(user_input)
		self.select_choice(self.choices[i])


story_maker = StoryMaker("crab_island.txt")

story_maker.goto_story_node("00000000-0000-0000-0000-000000000000")
is_running = True
while story_maker.is_running:
	user_choice = input("")
	story_maker.process_choice(user_choice)
