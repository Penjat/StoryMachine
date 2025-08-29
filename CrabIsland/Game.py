
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


class Game:
	def __init__(self):
		print("starting game...")
		self.is_playing = True
		self.location = "Harbor"

	def process(self, choice):
		connected_locations = locations[self.location]["connections"]
		if choice in connected_locations:
			self.location = choice
			print(f"you move to {choice}")
		else:
			print("not a connected location")
		

game = Game()

while game.is_playing:
	sleep(1) 
	print(f"your location is: {game.location}")
	connected_locations = locations[game.location]["connections"]
	print(f"{connected_locations}")
	choice = input("Where do you go: ")
	game.process(choice)
	