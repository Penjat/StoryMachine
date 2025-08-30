
from time import sleep
from enum import Enum, auto



locations = {
	"Sandy Cove": {
		"connections": ["Rocky Outcrop", "Palm Beach"],
		"description": "A quiet cove where waves lap gently at the shore.",
		"features": ["soft sand", "driftwood", "shells"]
	},
	"Rocky Outcrop": {
		"connections": ["Sandy Cove", "Seabird Cliffs"],
		"description": "Jagged rocks jut out into the sea, dangerous for ships.",
		"features": ["tide pools", "crabs", "sharp rocks"]
	},
	"Seabird Cliffs": {
		"connections": ["Rocky Outcrop", "Hidden Cave"],
		"description": "Towering cliffs where seabirds circle and nest.",
		"features": ["bird nests", "guano", "steep drop"]
	},
	"Hidden Cave": {
		"connections": ["Seabird Cliffs", "Driftwood Beach"],
		"description": "A dark cave carved into the rock, often flooded at high tide.",
		"features": ["echoes", "moss", "salt spray"]
	},
	"Driftwood Beach": {
		"connections": ["Hidden Cave", "Sheltered Bay"],
		"description": "A wide stretch of beach covered in tangled driftwood.",
		"features": ["logs", "seaweed", "footprints"]
	},
	"Sheltered Bay": {
		"connections": ["Driftwood Beach", "Old Wreck"],
		"description": "A calm bay, well hidden from the open sea.",
		"features": ["calm waters", "fishing boats", "coral"]
	},
	"Old Wreck": {
		"connections": ["Sheltered Bay", "Shattered Reef"],
		"description": "The splintered remains of a once-mighty ship, now rotting.",
		"features": ["broken mast", "cargo crates", "barnacles"]
	},
	"Shattered Reef": {
		"connections": ["Old Wreck", "Black Sand Beach"],
		"description": "Sharp coral reefs break the waves with deadly force.",
		"features": ["coral shards", "colorful fish", "wreckage"]
	},
	"Black Sand Beach": {
		"connections": ["Shattered Reef", "Jagged Rocks"],
		"description": "Dark volcanic sand crunches underfoot.",
		"features": ["obsidian shards", "warm sand", "strange markings"]
	},
	"Jagged Rocks": {
		"connections": ["Black Sand Beach", "Whispering Cliffs"],
		"description": "Rocks rise like teeth from the shore, slippery and dangerous.",
		"features": ["spray", "oysters", "slick stone"]
	},
	"Whispering Cliffs": {
		"connections": ["Jagged Rocks", "Moonlit Strand"],
		"description": "Wind whistles through cracks in the cliffs, sounding like voices.",
		"features": ["howling wind", "gulls", "carved faces in stone"]
	},
	"Moonlit Strand": {
		"connections": ["Whispering Cliffs", "Coral Beach"],
		"description": "A silver sand beach that glows in the moonlight.",
		"features": ["bioluminescence", "smooth stones", "quiet waves"]
	},
	"Coral Beach": {
		"connections": ["Moonlit Strand", "Stormwatch Point"],
		"description": "Shallow water reveals bright coral close to shore.",
		"features": ["starfish", "tide pools", "broken coral"]
	},
	"Stormwatch Point": {
		"connections": ["Coral Beach", "High Bluff"],
		"description": "A windswept point where storms are often first spotted.",
		"features": ["storm clouds", "lightning marks", "signal fire remains"]
	},
	"High Bluff": {
		"connections": ["Stormwatch Point", "Palm Beach"],
		"description": "A sheer cliff rising above the sea, offering a wide view.",
		"features": ["eagles", "grass tufts", "rock ledges"]
	},
	"Palm Beach": {
		"connections": ["High Bluff", "Sandy Cove"],
		"description": "Tall palms sway over soft golden sand.",
		"features": ["coconuts", "shade", "parrots"]
	}
}

npcs = [
	{
	"name": "Jorjo",
	"strength": 6,
	"health": 18,
	"location": "High Bluff",
	"speed": 4
	}
]



items = {
	"Sword of Dawn": {
		"name": "Sword of Dawn",
		"location": "Blacksmith"
	},
	"Healing Potion": {
		"name": "Healing Potion",
		"location": "Inn"
	},
	"Treasure Map": {
		"name": "Treasure Map",
		"location": "Harbor"
	},
	"Magic Lantern": {
		"name": "Magic Lantern",
		"location": "Watchtower"
	},
	"Bag of Gold": {
		"name": "Bag of Gold",
		"location": "Marketplace"
	},
	"Ancient Scroll": {
		"name": "Ancient Scroll",
		"location": "Town Square"
	}
}

def items_at_location(location_name):
	return [info["name"] for info in items.values() if info["location"] == location_name]

def get_npcs_at_location(location):
	"""Return a list of NPC names at the given location."""
	return [npc["name"] for npc in npcs if npc["location"] == location]


class Game:
	def __init__(self, character):
		print("starting game...")
		self.character_name = "Jill"
		self.is_playing = True
		self.character = character

	@property
	def current_location(self):
		return self.character["location"]

	def set_location(self, location):
		self.character["location"] = location


	def process(self, choice1, choice2):
		if choice1 == "move":
			connected_locations = locations[self.current_location]["connections"]
			if choice2 in connected_locations:
				self.set_location(choice2)
				print(f"you move to {choice2}")
			else:
				print("not a connected location")

		elif choice1 == "pickup":
			location_items = items_at_location(current_location)
			if choice2 in location_items:
				items[choice2]["location"] = "picked-up"
				print(f"you move to {choice2}")
			else:
				print(f"there is no {choice2} here...")

		elif choice1 == "drop":
			inventory_items = items_at_location("picked-up")
			if choice2 in inventory_items:
				items[choice2]["location"] = self.current_location
				item = items[choice2]["name"]
				print(f"you drop the {item} at the {self.current_location}")
			else:
				print(f"you do not have a {choice2}")

	def take_turn(self, choice1, choice2):
		characters = npcs + [self.character]
		sorted_chars = sorted(characters, key=lambda c: c["speed"], reverse=True)

		for character in sorted_chars:
			print(character["name"])


character = {
	"name": "Spencer",
	"strength": 22,
	"health": 100,
	"location": "High Bluff",
	"speed": 9
}		

game = Game(character)

while game.is_playing:
	sleep(1) 
	print(f"your location is: {game.current_location}")
	connected_locations = locations[game.current_location]["connections"]

	print(f"{connected_locations}")
	print(f"{items_at_location(game.current_location)}")
	print(f"{get_npcs_at_location(game.current_location)}")

	choice1 = input("what do you do: ")
	choice2 = input("+: ")

	game.take_turn(choice1, choice2)
	