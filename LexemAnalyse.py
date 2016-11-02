from LexemScanner import LexemScanner


class lexeical_scanner:
    def __init__(self, fileName):
        self.scanner = LexemScanner(fileName)
        self.lexems = [];

    def scanlexems(self):
        self.lexems = self.scanner.buildLexems()

    def doLexicalAnalyse(self):
        index = 0
        try:
            while (index < len(self.lexems)):
                detectedLexem = self.state_root(index)
                index = detectedLexem(index)
        except Exception as ex:
            print(str(ex))
            return False
        return True

    def state_root(self, index):
        if (self.lexems[index][0] == 'Tkeyword'):
            if (self.lexems[index][1] == 'def'):
                return self.state_functionDefinition
            elif (self.lexems[index][1] == 'if'):
                return self.state_if
            elif (self.lexems[index][1] == 'while'):
                return self.state_while
            elif (self.lexems[index][1] == 'return'):
                return self.state_return
            else:
                return self.state_operator
        elif (self.lexems[index][0] == 'Topenblock'):
            return self.state_block

    # States

    def state_functionDefinition(self, index):
        if (self.lexems[index][1] == 'def'):
            if (self.lexems[index + 1][0] == 'Tid'):
                if (self.lexems[index + 2][0] == 'Topenbracket'):
                    index = self.state_nameList(index + 3)
                    if (self.lexems[index][0] == 'Tclosebracket'):
                        if (self.lexems[index + 1][0] == 'Topenblock'):
                            index = self.state_block(index + 1)
                            return index
        raise Exception("Unexpected lexem at: " + str(index))

    def state_if(self, index):
        if (self.lexems[index][1] == 'if'):
            if (self.lexems[index + 1][0] == 'Topenbracket'):
                index = self.state_A1(index + 2)
                if (self.lexems[index][0] == 'Tclosebracket'):
                    if (self.lexems[index + 1][0] == 'Topenblock'):
                        index = self.state_operator(index + 2)
                        if (self.lexems[index][1] == 'else'):
                            index = self.state_operator(index + 1)
                            return index + 1
        raise Exception("Unexpected lexem at: " + str(index))

    def state_while(self, index):
        if (self.lexems[index][1] == 'while'):
            if (self.lexems[index + 1][0] == 'Topenbracket'):
                index = self.state_A1(index + 2)
                if (self.lexems[index][0] == 'Tclosebracket'):
                    if (self.lexems[index + 1][0] == 'Topenblock'):
                        index = self.state_operator(index + 2)
                        return index + 1
        raise Exception("Unexpected lexem at: " + str(index))

    def state_return(self, index):
        if (self.lexems[index][1] == 'return'):
            index = self.state_block(index + 1)
            return index
        raise Exception("Unexpected lexem at: " + str(index))

    def state_block(self, index):
        if (self.lexems[index][0] == 'Topenbracket'):
            index = self.state_root(index + 1)(index + 1)
            if (self.lexems[index][0] == 'Tclosebracket'):
                return index + 1
        raise Exception("Unexpected lexem at: " + str(index))

    def state_nameList(self, index):
        if (self.lexems[index][0] == 'Tid'):
            index += 1
            while (self.lexems[index][0] == 'Tcomma' and self.lexems[index + 1][0] == 'Tid'):
                index += 1
            return index
        raise Exception("Unexpected lexem at: " + str(index))

    def state_A1(self, index):
        if (self.lexems[index][0] == 'Tid' or self.lexems[index][0] == 'Tconst10' or self.lexems[index][
            0] == 'Tconst16'):
            if ((self.lexems[index][0] == 'Tmore'
                 or self.lexems[index][0] == 'Tequalmore'
                 or self.lexems[index][0] == 'Tequal'
                 or self.lexems[index][0] == 'Tequalless'
                 or self.lexems[index][0] == 'Tequal')
                and self.lexems[index + 1][0] == 'Tid'):

                index += 1
                while ((self.lexems[index][0] == 'Tmore'
                        or self.lexems[index][0] == 'Tequalmore'
                        or self.lexems[index][0] == 'Tequal'
                        or self.lexems[index][0] == 'Tequalless'
                        or self.lexems[index][0] == 'Tequal')
                       and self.lexems[index + 1][0] == 'Tid'):
                    index += 1
            return self.state_A2(index)
        raise Exception("Unexpected lexem at: " + str(index))

    def state_A2(self, index):
        if (self.lexems[index][0] == 'Tid' or self.lexems[index][0] == 'Tconst10' or self.lexems[index][
            0] == 'Tconst16'):
            if ((self.lexems[index][0] == 'Tplus'
                 or self.lexems[index][0] == 'Tminus')
                and self.lexems[index + 1][0] == 'Tid'):
                index += 1
                while ((self.lexems[index][0] == 'Tplus'
                        or self.lexems[index][0] == 'Tminus')
                       and self.lexems[index + 1][0] == 'Tid'):
                    index += 1
            return self.state_A3(index)
        raise Exception("Unexpected lexem at: " + str(index))

    def state_A3(self, index):
        if (self.lexems[index][0] == 'Tid' or self.lexems[index][0] == 'Tconst10' or self.lexems[index][
            0] == 'Tconst16'):
            if ((self.lexems[index][0] == 'Tmul'
                 or self.lexems[index][0] == 'Tdiv'
                 or self.lexems[index][0] == 'Tmod'
                 or self.lexems[index][0] == 'Tdivint')
                and self.lexems[index + 1][0] == 'Tid'):
                index += 1
                while ((self.lexems[index][0] == 'Tmul'
                        or self.lexems[index][0] == 'Tdiv'
                        or self.lexems[index][0] == 'Tmod'
                        or self.lexems[index][0] == 'Tminus')
                       and self.lexems[index + 1][0] == 'Tid'):
                    index += 1
            return self.state_A4(index)
        raise Exception("Unexpected lexem at: " + str(index))

    def state_A4(self, index):
        if (self.lexems[index][0] == 'Tid' or self.lexems[index][0] == 'Tconst10' or self.lexems[index][
            0] == 'Tconst16'):
            if ((self.lexems[index][0] == 'or' or self.lexems[index][0] == 'not' or self.lexems[index][0] == 'and') and
                        self.lexems[index + 1][0] == 'Tid'):
                index += 1
                while ((self.lexems[index][0] == 'or' or self.lexems[index][0] == 'not' or self.lexems[index][
                    0] == 'Tminus') and
                               self.lexems[index + 1][0] == 'Tid'):
                    index += 1
            return self.state_A5(index)
        raise Exception("Unexpected lexem at: " + str(index))

    def state_A5(self, index):
        if (self.lexems[index][0] == 'Tconst10'
            or self.lexems[index][0] == 'Tconst16'
            or self.lexems[index][0] == 'Tid'
            or self.lexems[index][0] == 'Topenbracket'
            or self.lexems[index][0] == 'Tclosebracket'):
            return index + 1
        raise Exception("Unexpected lexem at: " + str(index))

    def state_operatorSet(self, index):
        if (self.lexems[index][0] == 'Tkeyword' and self.lexems[index + 1][0] == 'Tassignment'):
            return self.state_A1(index + 2)

    def state_operator(self, index):
        if (self.lexems[index][0] == 'Tkeyword'):
            if (self.lexems[index][1] == 'if'):
                return self.state_if
            elif (self.lexems[index][1] == 'while'):
                return self.state_while
            elif (self.lexems[index][1] == 'return'):
                return self.state_return
            elif (self.lexems[index][1] == 'Tassignment'):
                return self.state_operatorSet
        elif (self.lexems[index][0] == 'Topenblock'):
            return self.state_block
        raise Exception("Unexpected lexem at: " + str(index))


ls = lexeical_scanner("input.txt")
print(ls.doLexicalAnalyse())
