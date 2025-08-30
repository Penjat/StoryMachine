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
        self.character = Character(**character_data)
        self.is_playing = True

        print("Game loaded!")

    @property
    def current_location(self):
        return self.character.location

    # --- Converted helper functions into methods ---
    def items_at_location(self, location_name):
        return [item.name for item in self.items.values() if item.location == location_name]

    def npcs_at_location(self, location):
        return [npc for npc in self.npcs if npc.location == location]

    def get_npc_by_name(self, name):
        for npc in self.npcs:
            if npc.name == name:
                return npc
        return None

    # --- Player action processing ---
    def process(self, choice1, choice2):
        if choice1 == "move":
            connected_locations = self.locations[self.current_location].connections
            if choice2 in connected_locations:
                self.character.location = choice2
                print(f"you move to {choice2}")
            else:
                print("not a connected location")

        elif choice1 == "pickup":
            location_items = self.items_at_location(self.current_location)
            if choice2 in location_items:
                self.items[choice2].location = "picked-up"
                print(f"you pick up {choice2}")
            else:
                print(f"there is no {choice2} here...")

        elif choice1 == "drop":
            inventory_items = self.items_at_location("picked-up")
            if choice2 in inventory_items:
                self.items[choice2].location = self.current_location
                print(f"you drop the {choice2} at the {self.current_location}")
            else:
                print(f"you do not have a {choice2}")

        elif choice1 == "attack":
            npcs_here = self.npcs_at_location(self.current_location)
            target = next((npc for npc in npcs_here if npc.name == choice2), None)

            if target:
                self.attack(self.character, target)
                
            else:
                print("No such NPC at this location")

    def attack(self, attacker, target):
    	damage = attacker.strength # TODO: more modifieres here
    	target.health -= damage
    	print(f"{attacker.name} deals {damage} damage to {target.name}. {target.name} has {target.health} HP left.")

    def take_turn(self, choice1, choice2):
        characters = self.npcs_at_location(self.current_location) + [self.character]
        sorted_chars = sorted(characters, key=lambda c: c.speed, reverse=True)

        for character in sorted_chars:
            if character == self.character:
                self.process(choice1, choice2)
            else:
            	# decide NPC action
            	if self.character.location == character.location:
            		self.attack(character, self.character)
            	
            	
                


    def loop(self):
        while self.is_playing:
            sleep(1)
            print(f"\nLocation: {self.current_location}")
            print(f"Connected: {self.locations[self.current_location].connections}")
            print(f"Items here: {self.items_at_location(self.current_location)}")
            print(f"NPCs here: {[npc.name for npc in self.npcs_at_location(self.current_location)]}")

            choice1 = input("Action (move/pickup/drop/attack): ")
            choice2 = input("Target/Location: ")
            self.take_turn(choice1, choice2)