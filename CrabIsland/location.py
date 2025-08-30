class Location:
    def __init__(self, name, connections, description, features):
        self.name = name
        self.connections = connections
        self.description = description
        self.features = features

    def to_json(self):
        return {
            "connections": self.connections,
            "description": self.description,
            "features": self.features
        }