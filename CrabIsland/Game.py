import json
from time import sleep
from character import Character
from item import Item
from location import Location


class Game:
	def __init__(self, character_file, items_file, locations_file, npcs_file):
		# Load JSON files
		with open(locations_file) as f:
			locations_data = json.load(f)
		with open(items_file) as f:
			items_data = json.load(f)
		with open(npcs_file) as f:
			npcs_data = json.load(f)
		with open(character_file) as f:
			character_data = json.load(f)

		# Build objects
		self.locations = {name: Location(name, **info) for name, info in locations_data.items()}
		self.items = {name: Item(**info) for name, info in items_data.items()}
		self.npcs = [Character(**info) for info in npcs_data]
		self.player = Character(**character_data)
		self.is_playing = True

		print("Game loaded!")

	# --- Properties ---
	@property
	def current_location(self):
		return self.player.location

	@property
	def is_game_won(self):
		# TODO: have multiple possible win conditions
		return self.player.location == "THE END"

	@property
	def player_items(self):
		"""Return all items that belong to the current player."""
		if not self.player:
			return []
		return [item for item in self.items.values() if item.location == self.player.name]

	# --- Helper methods ---
	def items_at_location(self, location_name):
		return [item for item in self.items.values() if item.location == location_name]

	def npcs_at_location(self, location, is_alive=None):
		npcs_here = [npc for npc in self.npcs if npc.location == location]

		if is_alive is True:
			npcs_here = [npc for npc in npcs_here if npc.health > 0]
		elif is_alive is False:
			npcs_here = [npc for npc in npcs_here if npc.health <= 0]

		return npcs_here

	def get_npc_by_name(self, name):
		return next((npc for npc in self.npcs if npc.name == name), None)

	# --- Player action processing ---


	def get_possible_actions(self):
		# title : action.name
		# {action: {"name": "", "type": "", "speed":"", "effects": [], "description":"", }
		actions = {}

		## -----------basic actions

		# Wait 
		actions["wait"] = {"action": {"name": "wait", "type": "wait", "speed": self.player.speed, "effects": [], "description": "" }, "targets": ["..."] }

		# Move
		connected_locations = self.locations[self.current_location].connections
		if connected_locations:
			actions["move"] = {"action": {"name": "walk", "type": "move", "speed": self.player.speed, "effects": [], "description": "" }, "targets": connected_locations }

		# Pickup
		items_here = self.items_at_location(self.current_location)
		if items_here:
			actions["pickup"] = {"action": {"name": "pick up", "type": "pickup", "speed": self.player.speed, "effects": [], "description": "" }, "targets": [item.name for item in items_here]}

		# Drop
		inventory_items = self.items_at_location("inventory")
		if inventory_items:
			actions["drop"] = {"action": {"name": "drop", "type": "drop", "speed": self.player.speed, "effects": [], "description": "" }, "targets": [item.name for item in inventory_items]}
		
		
		# Loot
		dead_characters = self.npcs_at_location(self.current_location, is_alive=False)
		if dead_characters:
			lootable_items = [
				item.name
				for item in self.items.values()
				if item.location in [npc.name for npc in dead_characters]
			]
			if lootable_items:
				actions["loot"] = {"action": {"name": "loot", "type": "loot", "speed": self.player.speed, "effects": {}, "description": "" }, "targets": lootable_items + ["all"]}

		## Attack
		npcs_here = self.npcs_at_location(self.current_location, is_alive=True)
		if npcs_here:
			actions["attack"] = {"action": {"name": "attack", "type": "attack", "speed": self.player.speed, "effects": {}, "description": "" }, "targets": [npc.name for npc in npcs_here]}

			for item in self.player_items:
				for use in item.uses:
					actions[use["name"]] = {"action": {"name": use["name"], "type": "attack", "speed": self.player.speed, "effects": use["effects"], "description": "" }, "targets": [npc.name for npc in npcs_here] }

		# print(f"the player has {len(self.player_items)}")
		# for item in self.player_items:
		# 	for use in item.uses:
		# 		actions[use["name"]] = {"options": [npc.name for npc in npcs_here], "item": item, "use": use}

		
		

		return actions
	def process_action(self, action, target_name):
		print(f"action is:{action}, targetName:{target_name}")
		action_type = action["type"]

		
		if action_type == "move":
			connected = self.locations[self.current_location].connections
			if target_name in connected:
				self.player.location = target_name
				print(f"You move to {target_name}.")
			else:
				print("That location is not connected.")

		elif action_type == "pickup":
			items_here = [item.name for item in self.items_at_location(self.current_location)]
			if target_name in items_here:
				self.items[target_name].location = "inventory"
				print(f"You pick up {target_name}.")
			else:
				print(f"There is no {target_name} here.")

		elif action_type == "drop":
			inventory_items = [item.name for item in self.items_at_location("inventory")]
			if target_name in inventory_items:
				self.items[target_name].location = self.current_location
				print(f"You drop the {target_name} at {self.current_location}.")
			else:
				print(f"You do not have a {target_name}.")

		elif action_type == "attack":
			npcs_here = self.npcs_at_location(self.current_location, is_alive=True)
			target = next((npc for npc in npcs_here if npc.name == target_name), None)
			attack_bonus = action["effects"].get("attack", 0)

			damage = self.player.strength + attack_bonus


			if target:
				# self.attack(self.player, target)
				target.deal_dmg(damage, self.player.name)
			else:
				print("No such NPC here to attack.")
		elif action_type == "loot":
			dead_npcs = self.npcs_at_location(self.current_location, is_alive=False)
			dead_names = [npc.name for npc in dead_npcs]

			if not dead_npcs:
				print("There are no dead NPCs to loot here.")
				return

			if target_name.lower() == "all":
				found_any = False
				for npc_name in dead_names:
					lootable_items = [item for item in self.items.values() if item.location == npc_name]
					if lootable_items:
						found_any = True
						print(f"You loot {npc_name}:")
						for item in lootable_items:
							item.location = "inventory"
							print(f" - {item.name}")
				if not found_any:
					print("There is nothing to loot from any corpses.")
			else:
				# Loot a specific item if it belongs to a dead NPC
				item = self.items.get(target_name)
				if item and item.location in dead_names:
					item.location = "inventory"
					print(f"You loot {target_name} from {item.location}.")
				else:
					print(f"You cannot loot {target_name} here.")
		


	# --- Game loop parts ---
	def take_turn(self, player_action):
		# Turn order
		participants = self.npcs_at_location(self.current_location, is_alive=True) + [self.player]
		sorted_chars = sorted(participants, key=lambda c: c.speed, reverse=True)

		for character in sorted_chars:
			if character == self.player:
				if player_action:
					self.process_action(*player_action)
			else:
				if character.isAlive and character.location == self.player.location:
					# self.attack(character, self.player)
					print("todo: npc action")

		# Check end conditions
		if not self.player.isAlive:
			print("You have died. THE END")
			self.is_playing = False

		if self.is_game_won:
			print("You have completed your quest!")
			print("THE END")
			self.is_playing = False

	def loop(self):
		while self.is_playing:
			sleep(1)
			print(f"\nLocation: {self.current_location}")

			available_actions = self.get_possible_actions()
			indexed_choices = []
			idx = 0

			# Print available actions
			for action_type, data in available_actions.items():
				action = data["action"]
				for option in data["targets"]:
					print(f"{idx} - {action_type} {option}")
					indexed_choices.append((action, option))
					idx += 1

			if not indexed_choices:
				print("No actions available!")
				self.is_playing = False
				break

			choice_idx = input("Select number: ")
			if not choice_idx.isdigit() or int(choice_idx) >= len(indexed_choices):
				print("Invalid choice.")
				continue

			player_action = indexed_choices[int(choice_idx)]
			self.take_turn(player_action)
