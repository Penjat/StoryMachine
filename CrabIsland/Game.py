
from time import sleep



locations = {
    "Town Square": {
        "connections": ["Blacksmith", "Marketplace", "Inn"]
    },
    "Blacksmith": {
        "connections": ["Town Square", "Marketplace"]
    },
    "Marketplace": {
        "connections": ["Town Square", "Blacksmith", "Harbor"]
    },
    "Inn": {
        "connections": ["Town Square", "Harbor"]
    },
    "Harbor": {
        "connections": ["Marketplace", "Inn", "Watchtower"]
    },
    "Watchtower": {
        "connections": ["Harbor"]
    }
}

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


class Game:
	def __init__(self):
		print("starting game...")
		self.is_playing = True
		self.location = "Harbor"


	def process(self, choice1, choice2):
		if choice1 == "move":
			connected_locations = locations[self.location]["connections"]
			if choice2 in connected_locations:
				self.location = choice2
				print(f"you move to {choice2}")
			else:
				print("not a connected location")

		elif choice1 == "pickup":
			location_items = items_at_location(self.location)
			if choice2 in location_items:
				items[choice2]["location"] = "picked-up"
				print(f"you move to {choice2}")
			else:
				print(f"there is no {choice2} here...")

		elif choice1 == "drop":
			inventory_items = items_at_location("picked-up")
			if choice2 in inventory_items:
				items[choice2]["location"] = self.location
				print(f"you drop the {items[choice2]["name"]} at the {self.location}")
			else:
				print(f"you do not have a {choice2}")
		

game = Game()

while game.is_playing:
	sleep(1) 
	print(f"your location is: {game.location}")
	connected_locations = locations[game.location]["connections"]

	print(f"{connected_locations}")
	print(f"{items_at_location(game.location)}")
	choice1 = input("what do you do: ")
	choice2 = input("+: ")
	game.process(choice1, choice2)
	