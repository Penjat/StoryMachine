class Character:
    def __init__(self, name, strength, health, location, speed):
        self.name = name
        self.strength = strength
        self.health = health
        self.location = location
        self.speed = speed

    @property
    def isAlive(self):
        return self.health > 0

    def to_json(self):
        return {
            "name": self.name,
            "strength": self.strength,
            "health": self.health,
            "location": self.location,
            "speed": self.speed
        }

    def deal_dmg(self, dmg, source_name):
        self.health -= dmg

        print(f"{source_name} deals {dmg} damage to {self.name}!")
        if self.isAlive == False:
            print(f"{self.name} was killed by {source_name}")

