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

    def getParams(self):
        return self.params

    def __str__(self):
        res = "[ Name: " + self.name + " (" + str(self.type) + ") Params:" + str(self.params) + "] -> "
        if (self.neighbour != None):
            res += self.neighbour.name
        else:
            res += "NONE"
        res += "\n└-> "
        if (self.child != None):
            res += self.child.name
        else:
            res += "NONE"
        return res

        #


class TokenTree:
    def __init__(self):
        self.root = node("root", TokenType.root, None, "")
        self.current = self.root
        self._addFake()

    # Метод добавления объекта в дерево
    def addNode(self, name, type, params):
        if (type == TokenType.variable):
            if (self._tryPutName(name, type)):
                return self._addVariable(name)
            else:
                return False
        elif (type == TokenType.function):
            return self._addFunction(name, params)

    # Метод проверки наличия объекта в дереве
    def checkNode(self, name, type, params):
        if (type == TokenType.variable):
            return self._checkVariable(name)
        elif (type == TokenType.function):
            if (self._checkFunction(name, params)):
                for var in params:
                    if (var.tokenName == "Tid"):
                        if (not self._checkVariable(var.token)):
                            return False
                return True
            else:
                return False

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
        while (current.getType() != TokenType.root):
            if (current.getName() == name and current.getType() == TokenType.variable):
                return True
            current = current.getParent()

        return False

    def _checkFunction(self, name, params):
        current = self.current
        while (current.getType() != TokenType.root):
            if (current.getName() == name and current.getType() == TokenType.function):
                return current.getParams() == len(params)
            current = current.getParent()
        return False

    # Проверка наличия имени в дереве
    def _tryPutName(self, name, type):
        current = self.current
        while (current.getType() != TokenType.root):
            if (current.getName() == name):
                return False
            current = current.getParent()
        return True

    # Метод добавления фейковой врешины
    def _addFake(self):
        if (self.current.getChild() == None):
            self.current.addChild(node("fake", TokenType.fake, self.current, ""))
            self.current = self.current.getChild()
        else:
            self.current.addNeighbour(node("neighbour fake", TokenType.fake, self.current, ""))
            self.current = self.current.getNeighbour()
            self._addFake()

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
        return True

    # Метод доабвления функции и премещения указателя на уровень функции переменной
    def _addFunction(self, name, params):
        added = node(name, TokenType.function, self.current, len(params))
        self.current.addNeighbour(added)
        self.current = added
        self._addFake()

        for current in params:
            self._addVariable(current.token)
        return True
