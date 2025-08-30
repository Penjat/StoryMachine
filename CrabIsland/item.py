class Item:
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def to_json(self):
        return {
            "name": self.name,
            "location": self.location
        }
        