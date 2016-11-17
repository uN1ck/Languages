from TokenScanner import scanner, token


class TokenAnalyse:
    def __init__(self, ):
        self.scanner = None
        self.tokens = []

    def scanFile(self, lines):
        self.scanner = scanner(lines)
        self.tokens = self.scanner.getTokens()

    def analyseFile(self):
        return False

    # Метод извещения об ошибке
    def markError(self, element):
        print("Unexpected token " + str(element))
        raise Exception('Unexpected token', str(element))

    # Детектор состояний
    def stateAt(self, line, index):
        if (line[index].tokenName == 'Tdef'):
            return self.state_functionDef
        elif (line[index].tokenName == 'Tif'):
            return self.state_if
        elif (line[index].tokenName == 'Twhile'):
            return self.state_while
        elif (line[index].tokenName == 'Treturn'):
            return self.state_return
        elif (line[index].token == 'Topenblock'):
            return self.state_block
        elif (line[index].token == 'Tid'):
            if (len(line[index:]) > 1):

                if (line[index + 1].tokenName == 'Tmore'
                    or line[index + 1].tokenName == 'Tequalmore'
                    or line[index + 1].tokenName == 'Tequal'
                    or line[index + 1].tokenName == 'Tequalles'
                    or line[index + 1].tokenName == 'Tless'):
                    return self.state_A2
                elif(line[index + 1].tokenName == 'Tplus'
                    or line[index + 1].tokenName == 'Tminus'):
                    return self.state_A3
                elif (line[index + 1].tokenName == 'Tmul'
                      or line[index + 1].tokenName == 'Tdiv'
                      or line[index + 1].tokenName == 'Tdivint'
                      or line[index + 1].tokenName == 'Tmod'):
                    return self.state_A4
                elif (line[index + 1].tokenName == 'Topenbracket'
                      or line[index + 1].tokenName == 'Tclosebracket'
                      or line[index + 1].tokenName == 'T'
                      or line[index + 1].tokenName == 'Tdiv'

    # Состояния класса

    def state_A2(self, line, index):
        if (len(line[index:]) > 1):
            if (line[index + 1].token == '>'
                or line[index + 1].token == '>='
                or line[index + 1].token == '=='
                or line[index + 1].token == '<='
                or line[index + 1].token == '<'):
                return self.state_A2(line, index + 1)
            else:
                return self.state_A3(line, index + 1)
        self.markError("No next token after -> " + line[index])

    def state_A3(self, line, index):
        if (len(line[index:]) > 1):
            if (line[index + 1].token == '+'
                or line[index + 1].token == '-'):
                return self.state_A3(line, index + 1)
            else:
                return self.state_A4(line, index + 1)
        self.markError("No next token after -> " + line[index])

    def state_A4(self, line, index):
        if (len(line[index:]) > 1):
            if (line[index + 1].token == '*'
                or line[index + 1].token == '/'
                or line[index + 1].token == '//'
                or line[index + 1].token == '%'):
                return self.state_A4(line, index + 1)
            else:
                return self.state_A5(line, index + 1)
        self.markError("No next token after -> " + line[index])

    def state_A5(self, line, index):
        # if (len(line[index:]) > 1):

        self.markError("No next token after -> " + line[index])

    def _state_while(self)):

    def state_while(self, line, index):
        position = index
        current = line[index:]
        if (current[0].tokenName == 'Twhile'):
            if (current[1].tokenName == 'Topenbracket'):
                gap = self.state_nameList(current,2)
                if (current[gap].tokenName == 'Tclosebracket'):



    def state_if(self, line, index):
        return 1

    def state_block(self, line, index):
        return 1

    def state_return(self, line, index):
        return 1

    def state_assignment(self, line, index):
        return 1

    def state_invoke(self, line, index):
        return 1

    def state_operator(self, line, index):
        if (line[index].token == 'while'):
            self.state_while(line, index)
        elif (line[index].tokenName == 'Topenblock'):
            self.state_block(line, index)
        elif (line[index].token == 'return'):
            self.state_return(line, index)
        elif (line[index].token == 'if'):
            self.state_block(line, index)
        elif (line[index].tokenName == 'Tid'):
            if (line[index + 1].tokenName == 'Tassignment'):
                self.state_assignment(line, index)
            else:
                self.state_invoke(line, index)
        else:
            self.markError("Unexpected lexem: \"" + str(line[index]) + "\" at " + line)

    def _state_functionDef(self, line, index):
        position = index
        while (position + 1 < len(line[index:])):
            if (line[index + position].tokenName == 'Tid' and line[index + position].tokenName == 'Tcomma'):
                position += 2
        if (line[index + position].tokenName == 'Tclosebracket' and line[
                    index + position + 1].tokenName == 'Topenblock'):
            return True
        return False

    def state_functionDef(self, line, index):
        current = line[index:]
        if (current[0].token == 'def'
            and current[1].tokenName == 'Tid'
            and current[2].tokenName == 'Topenbracket'):
            return self._state_functionDef(line, index + 3)
        self.markError("Unexpected lexem at: " + line[index:])
