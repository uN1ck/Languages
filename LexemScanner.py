import re

Lexems = {'Tconst10': '[1-9][0-9]*',
          'Tconst16': '0x[0-9A-F]+',
          'Tid': '[a-zA-Z]+',
          'Tassignment': '=',
          'Tequal': '==',
          'Tnotequal': '!=',
          'Tmore': '>[^=]',
          'Tless': '<[^=]',
          'Tequalmore': '>=',
          'Tequalless': '<=',
          'Tplus': '\+',
          'Tminus': '\-',
          'Tmul': '\*',
          'Tdiv': '/',
          'Tdivint': '//',
          'Tmod': '%',
          'Tcomma': ',',
          'Topenbracket': '\(',
          'Tclosebracket': '\)',
          'Ttabblock': '\{',
          'Topenblock': ':'
          }

keyWords = {'def', 'while', 'return', 'or', 'and', 'if'}
keyWordsId = {'def': '6114', 'while': '6214', 'return': '6314', 'or': '6414', 'and': '6514', 'if': '6614'}
Comments = {'Tcomment': '#[^\n]*',
            'Teol': '\n',
            'Tmulticomment': '\'\'\''}


# Класс сканера
class lexical_scanner:
    def __init__(self):
        self.text = []
        self.lexemsAnalysed = []

    def initialize(self, text):
        self.text = text

    def setBlocks(self):
        current = self.text[0]
        prev = current
        tabGap = 0

        for line in self.text:
            currentTabGap = 0
            for current in range(len(line)):
                if line[current] == ':':
                    line[current] = '{'

            while (line[currentTabGap] == ' '): currentTabGap += 1

            if (currentTabGap != tabGap):
                line += " }"
                tabGap = currentTabGap

    # Метод удаления всех комментариев
    def deleteComments(self):

        isComment = False
        result = []

        for current in self.text:
            for pattern in Comments:

                if (re.match(Comments[pattern], current) and pattern == 'Tmulticomment'):
                    isComment = isComment ^ True

                if (isComment and pattern == 'Tmulticomment'):
                    current = ''
                    break

                current = current.strip(' ')
                current = re.sub(Comments[pattern], '', current)

            if (len(current) > 0 and re.fullmatch('_+', current) == None):
                # print(current)
                result.append(current)
        self.text = result
        if (isComment):
            self.markError(("No ending on comment"))

    # Метод извещения об ошибке
    def markError(self, element):
        print("Lexical error at " + str(element))
        raise Exception('Lexical error', str(element))

    # Метод чтения следующей лексемы
    # Возврщаемый тип (Имя лексемы, обозначение, индекс в строке, длина, индекс лексемы)
    def nextLexem(self, line, start):

        index = start + 1

        if (line[start] == ','):
            return ('Tcomma', line[start:index], start, 1, 1001)
        if (line[start] == '{'):
            return ('Topenblock', line[start:index], start, 1, 9001)
        if (line[start] == '}'):
            return ('Tcloseblock', line[start:index], start, 1, 9002)

        if (line[start] == '+'):
            return ('Tplus', line[start:index], start, 1, 2001)
        if (line[start] == '-'):
            return ('Tminus', line[start:index], start, 1, 2101)
        if (line[start] == '/'):
            if (len(line) > start + 1):
                if (line[start + 1] == '/'):
                    return ('Tdivint', line[start:index + 1], start, 2, 2201)
            return ('Tdiv', line[start:index], start, 1, 2301)
        if (line[start] == '*'):
            return ('Tmul', line[start:index], start, 1, 2401)
        if (line[start] == '%'):
            return ('Tmod', line[start:index], start, 1, 2501)

        if (line[start] == '('):
            return ('Topenbracket', line[start:index], start, 1, 3010)
        if (line[start] == ')'):
            return ('Tclosebracket', line[start:index], start, 1, 3111)

        if (line[start] == '='):
            if (len(line) > index + 1):
                if (line[start + 1] == '='):
                    return ('Tequal', line[start:index + 1], start, 2, 4001)
            return ('Tassignment', line[start:index], start, 1, 4101)
        if (line[start] == '!'):
            if (len(line) > start + 1):
                if (line[start + 1] == '='):
                    return ('Tequal', line[start:index + 1], start, 2, 4201)
        if (line[start] == '>'):
            if (len(line) > start + 1):
                if (line[start + 1] == '='):
                    return ('Tequalmore', line[start:index + 1], start, 2, 4301)
            return ('Tmore', line[start:index], start, 1, 4401)
        if (line[start] == '<'):
            if (len(line) > start + 1):
                if (line[start + 1] == '='):
                    return ('Tequalless', line[start:index + 1], start, 2, 4501)
            return ('Tless', line[start:index], start, 1, 4601)

        if (re.match('[a-zA-Z]', line[start]) != None):
            while (len(line) > index) and (re.match('[a-zA-Z]', line[index]) != None):
                index += 1
            if (line[start:index] in keyWords):
                return ('Tkeyword', line[start:index], start, index - start, keyWordsId[line[start:index]])
            else:
                return ('Tid', line[start:index], start, index - start, 6014)

        if (re.match('[1-9]', line[start]) != None):
            while (len(line) > index) and (re.match('[0-9]', line[index]) != None):
                index += 1
            return ('Tconst10', line[start:index], start, index - start, 7015)

        if (start + 2 < len(line)):
            if (line[start:start + 2] == '0x'):
                while (len(line) > index) and (re.match('[0-9A-F]', line[index]) != None):
                    index += 1
                return ('Tconst16', line[start:index], start, index - start, 7116)

        return ('Terror', line[start], 1, 1, 0000)

    # Метод вывода найденных лексем
    def scanAllLexems(self):
        self.deleteComments()
        self.setBlocks()

        for line in self.text:
            lexemLine = []
            index = 0

            while len(line) > index:
                if (re.match(' ', line[index]) != None):
                    index += 1
                    continue
                currentLexem = self.nextLexem(line, index)

                if (currentLexem[0] == "Terror"):
                    self.markError(currentLexem)

                lexemLine.append(currentLexem)
                index += currentLexem[3]
            self.lexemsAnalysed.append(lexemLine)
        return True


class LexemScanner:
    lexems = []
    ls = lexical_scanner()

    def __init__(self, textName):
        lexical_scanner.text = open(textName, "r")

    def buildLexems(self):
        lexical_scanner.scanAllLexems()
        for lexemLine in lexical_scanner.lexemsAnalysed:
            for lexem in lexemLine:
                self.lexems.append((lexem[0], lexem[1], lexem[4]))
