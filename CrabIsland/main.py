from game import Game
from rx.subject import Subject

if __name__ == "__main__":
    
    game = Game(
        character_file="data/character.json",
        items_file="data/items.json",
        locations_file="data/locations.json",
        npcs_file="data/npcs.json"
    )

    game.loop()