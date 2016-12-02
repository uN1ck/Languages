from enum import Enum


class TokenType(Enum):
    variable = 1
    function = 2
    fake = 3
    root = 4


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

    def getParent(self):
        return self.parent

    def getChild(self):
        return self.child

    def getNeighbour(self):
        return self.neighbour

    def getType(self):
        return self.type

    def getName(self):
        return self.name

    def __str__(self):
        return "[" + str(self.type) + " " + self.name + " " + str(len(self.params)) + "]"

        #


class TokenTree:
    def __init__(self):
        self.root = node("root", TokenType.root, None, "")
        self.current = self.root

    # Метод добавления объекта в дерево
    def addNode(self, name, type, params):
        if (type == TokenType.variable):
            return self._addVariable(name)
        elif (type == TokenType.function):
            return self._addFunction(name, params)

    # Метод проверки наличия объекта в дереве
    def checkNode(self, name, type, params):
        if (type == TokenType.variable):
            return self._checkVariable(name)
        elif (type == TokenType.variable):
            return self._checkFunction(name, params)

    def printTree(self):
        self._printTree(self.root)

    def _printTree(self, current):
        print(str(current))
        if (current.getNeighbour() != None):
            self._printTree(current.getNeighbour())

        if (current.getChild() != None):
            print('\n')
            self._printTree(current.getChild())

    #
    # Приватные методы работы с деревом
    #

    def _checkVariable(self, name):
        current = self.current
        while (current.getName() != name):
            current = current.getParent()
            if (current.getType() == TokenType.root):
                return False
        return True

    def _checkFunction(self, name, params):
        while (self.current.getName() != name):
            self.current = self.current.getParent()
            if (self.current.getType() == TokenType.root):
                return False
        return True

    # Метод добавления фейковой врешины
    def _addFake(self):
        self.current.addChild(node("fake", TokenType.fake, self.current, ""))
        self.current = self.current.getChild()

    # Метод смещения текущего указателя дерева выше на один уровень
    def _stepUp(self):
        while (self.current.getType() != TokenType.fake):
            self.current = self.current.getParent()
        self.current = self.current.getParent()
        while (self.current.getNeighbour() != None):
            self.current = self.current.getNeighbour()

    # Метод доабвления переменной
    def _addVariable(self, name):
        added = node(name, TokenType.variable, self.current, "")
        self.current.addNeighbour(added)
        self.current = self.current.getNeighbour()

    # Метод доабвления функции и премещения указателя на уровень функции переменной
    def _addFunction(self, name, params):
        added = node(name, TokenType.function, self.current, params)
        self.current.addNeighbour(added)
        self.current = added
        self._addFake()

        for current in params:
            self._addVariable(current.token)
