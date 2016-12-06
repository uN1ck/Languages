from TokenScanner import scanner, token
from TokenTree import TokenTree, TokenType, node


class TokenAnalyse:
    def __init__(self):
        self.scanner = None
        self.tokens = []
        self.position = 0
        self.tree = TokenTree()

    def scanFile(self, lines):
        self.scanner = scanner(lines)
        self.tokens = self.scanner.getTokens()

    def analyseFile(self):
        try:
            self.state_root()
        except Exception as ex:
            # raise ex
            print(ex)
            return False
        return True

    def getCurrent(self):
        return self.tokens[self.position]

    def getAt(self, index):
        return self.tokens[self.position + index]

    def markError(self, element):
        # print("Exception! -> " + str(element))
        raise Exception('Exception! -> ', str(element))

    #

    def getTree(self):
        return self.tree

    #
    def state_A1(self):
        self.state_A2()
        while (self.getAt(0).tokenName == 'Tmore'
               or self.getAt(0).tokenName == 'Tequalmore'
               or self.getAt(0).tokenName == 'Tequal'
               or self.getAt(0).tokenName == 'Tequalless'
               or self.getAt(0).tokenName == 'Tless'):
            self.position += 1
            self.state_A2()

    def state_A2(self):
        self.state_A3()
        while (self.getAt(0).tokenName == 'Tplus'
               or self.getAt(0).tokenName == 'Tminus'):
            self.position += 1
            self.state_A3()

    def state_A3(self):
        self.state_A4()
        while (self.getAt(0).tokenName == 'Tmul'
               or self.getAt(0).tokenName == 'Tdiv'
               or self.getAt(0).tokenName == 'Tdivint'
               or self.getAt(0).tokenName == 'Tmod'):
            self.position += 1
            self.state_A4()

    def state_A4(self):
        self.state_A5()
        while (self.getAt(0).tokenName == 'Tor'
               or self.getAt(0).tokenName == 'Tand'
               or self.getAt(0).tokenName == 'Tnot'):
            self.position += 1
            self.state_A5()

    def state_A5(self):
        if (self.getAt(0).tokenName == 'Tconst10' or self.getAt(0).tokenName == 'Tconst16'):
            self.position += 1
        elif (self.getAt(0).tokenName == 'Tid'):
            if (self.getAt(1).tokenName == 'Topenbracket'):
                # Проверка идентификатора функции
                self.state_functionCall()
            else:
                if (not self.tree.checkNode(self.getAt(0).token, TokenType.variable, "")):
                    self.markError("Unexpected identifer: " + str(self.getAt(0)))
            self.position += 1
        elif (self.getAt(0).tokenName == 'Topenbracket'):
            self.position += 1
            self.state_A1()
            if (self.getAt(0).tokenName == 'Tclosebracket'):
                self.position += 1
            else:
                self.markError("Expected [)] got [" + str(self.getAt(0)) + "]")
        else:
            self.markError("Unexpected token [" + str(self.getAt(0)) + "]")

    def state_functionCall(self):
        if (self.getAt(0).tokenName == 'Tid'):
            name = self.getAt(0)
            if (self.getAt(1).tokenName == 'Topenbracket'):
                self.position += 2

                argCount = self.position
                args = []

                if (self.getAt(0).tokenName == 'Tid' or self.getAt(0).tokenName == 'Tconst10' or self.getAt(
                        0).tokenName == 'Tconst16'):
                    self.state_callParameters()

                while (argCount < self.position):
                    args.append(self.getAt(- self.position + argCount))
                    argCount += 2

                if (not self.tree.checkNode(name.token, TokenType.function, args)):
                    self.markError("Unexpected identifer: " + str(self.getAt(0)))

                if (self.getAt(0).tokenName == 'Tclosebracket'):
                    self.position += 1
                else:
                    return self.markError("Expected [)] got [" + str(self.getAt(0)) + "]")
            else:
                return self.markError("Expected [(] got [" + str(self.getAt(1)) + "]")
        else:
            return self.markError("Expected [Name] got [" + str(self.getAt(0)) + "]")

    def state_functionDefinition(self):
        if (self.getAt(0).tokenName == 'Tdef'):
            if (self.getAt(1).tokenName == 'Tid'):
                name = self.getAt(1)
                if (self.getAt(2).tokenName == 'Topenbracket'):
                    self.position += 3

                    argCount = self.position
                    args = []

                    if (self.getAt(0).tokenName == 'Tid'):
                        self.state_nameList()

                    if (self.getAt(0).tokenName == 'Tclosebracket'):
                        self.position += 1

                        while (argCount < self.position - 1):
                            args.append(self.getAt(- self.position + argCount))
                            argCount += 2

                        if (not self.tree.addNode(name.token, TokenType.function, args)):
                            self.markError("Unexpected identifer: " + str(name))

                        self.state_block()
                    else:
                        return self.markError("Expected [)] got [" + str(self.getAt(0)) + "]")
                else:
                    return self.markError("Expected [(] got [" + str(self.getAt(1)) + "]")
            else:
                return self.markError("Expected [Name] got [" + str(self.getAt(0)) + "]")
        else:
            return self.markError("Expected [Def] got [" + str(self.getAt(0)) + "]")

    def state_nameList(self):
        if (self.getAt(0).tokenName == 'Tid'):
            while (True):
                if (self.getAt(1).tokenName == 'Tcomma'):
                    if (self.getAt(2).tokenName == 'Tid'):
                        self.position += 2

                    else:
                        return self.markError("Expected [Name] got [" + str(self.getAt(2)) + "]")
                else:
                    self.position += 1
                    break
        else:
            return self.markError("Expected [Name] got [" + str(self.getAt(0)) + "]")

    def state_callParameters(self):
        if (self.getAt(0).tokenName == 'Tid'
            or self.getAt(0).tokenName == 'Tconst10'
            or self.getAt(0).tokenName == 'Tconst16'):

            self.state_A1()
            while (True):
                if (self.getAt(0).tokenName == 'Tcomma'):
                    self.position += 1
                    self.state_A1()
                else:
                    break
            else:
                return self.markError("Expected [,] got [" + str(self.getAt(1)) + "]")
        else:
            return self.markError("Expected [Name] got [" + str(self.getAt(0)) + "]")

    def state_while(self):
        if (self.getAt(0).tokenName == 'Twhile'):
            self.tree._addFake()

            if (self.getAt(1).tokenName == 'Topenbracket'):
                self.position += 2
                self.state_A1()
                if (self.getAt(0).tokenName == 'Tclosebracket'):
                    self.position += 1
                    self.state_block()
                else:
                    return self.markError("Expected [)] got [" + str(self.getAt(0)) + "]")
            else:
                return self.markError("Expected [(] got [" + str(self.getAt(1)) + "]")
        else:
            return self.markError("Expected [While] got [" + str(self.getAt(0)) + "]")

    def state_assignment(self):
        if (self.getAt(0).tokenName == 'Tid'):
            if (self.getAt(1).tokenName == 'Tassignment'):

                if (not self.tree.addNode(self.getAt(0).token, TokenType.variable, "")):
                    self.markError("Unexpected identifer: " + str(self.getAt(0)))

                self.position += 2
                self.state_A1()
            else:
                return self.markError("Expected [=] got [" + str(self.getAt(1)) + "]")
        else:
            return self.markError("Expected [Name] got [" + str(self.getAt(0)) + "]")

    def state_return(self):
        if (self.getAt(0).tokenName == 'Treturn'):
            self.position += 1
            self.state_A1()
        else:
            return self.markError("Expected [Return] got [" + str(self.getAt(0)) + "]")

    def state_block(self):
        if (self.getAt(0).tokenName == 'Topenblock'):
            self.position += 1
            while (self.getAt(0).tokenName != 'Tcloseblock'):
                self.state_expression()
            if (self.getAt(0).tokenName == 'Tcloseblock'):
                self.position += 1

                self.tree._stepUp()

            else:
                return self.markError("Expected [}] got [" + str(self.getAt(0)) + "]")
        else:
            return self.markError("Expected [{] got [" + str(self.getAt(0)) + "]")

    def state_root(self):
        while (self.position < len(self.tokens)):
            self.state_expression()

    def state_expression(self):
        if (self.getAt(0).tokenName == 'Tdef'):
            self.state_functionDefinition()
        else:
            self.state_operator()

    def state_operator(self):
        if (self.getAt(0).tokenName == 'Tid'):
            if (self.getAt(1).tokenName == 'Topenbracket'):
                self.state_functionCall()
            else:
                self.state_assignment()
        elif (self.getAt(0).tokenName == 'Twhile'):
            self.state_while()
        elif (self.getAt(0).tokenName == 'Topenblock'):
            self.state_block()
        elif (self.getAt(0).tokenName == 'Treturn'):
            self.state_return()
        else:
            return self.markError("Expected [Operator] got [" + str(self.getAt(0)) + "]")


TA = TokenAnalyse()
TA.scanFile(open("input.txt").readlines())
if (TA.analyseFile()):
    print("Passed!")
    TA.getTree().printTree()
else:
    print("NOT Passed!")
    #
