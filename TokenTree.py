class node:
    def __init__(self, name, type, parent, params):
        self.name = name
        self.type = type
        self.params = params
        self.child = None
        self.neighbour = None
        self.parent = parent

    def addChild(self, value):
        self.child = value

    def addNeighbour(self, value):
        self.neighbour = value
