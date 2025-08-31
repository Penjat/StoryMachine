class Item:
    def __init__(self, name, location, uses=[]):
        self.name = name
        self.location = location
        self.uses = uses

    def to_json(self):
        return {
            "name": self.name,
            "location": self.location,
            "uses": self.uses
        }