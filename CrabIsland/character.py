class Character:
    def __init__(self, name, strength, health, location, speed):
        self.name = name
        
        self.location = location

        
        # - Stats
        self.speed = speed
        self.strength = strength
        # self.vitality
        # self.dextarity
        # self.constituion
        # self.intellengce
        # self.wisdom
        # self.charisma
        # self.luck

        # - State
        self.health = health
        # self.mood
        

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

    def get_action(self, npcs, items):
        npcs_here = [npc for npc in self.npcs if npc.location == location]


        # Violence Adversion
        # 10 true pacifist, won't attack
        # -10 Pycotic, attacks everyone regaurdless

        # Courage
        # 10 not afraid of anything, will charge into certain death
        # -10 fraidy cat, runs away from everything

        # Forgivness
        # 10 turn the other cheek
        # -10 once harmed, cannot be undone

        


