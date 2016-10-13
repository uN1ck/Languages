import re

fin = open("input.txt", "r")
fout = open("output.txt", "w")

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

LexemIndices = {'Tconst10': 1000,
                'Tconst16': 1001,
                'Tid': 1010,
                'Topenbracket': 1000,
                'Tclosebracket': 1000,
                'Ttabblock': 1500,
                'Tassignment': 2007,
                'Tequal': 2107,
                'Tnotequal': 2207,
                'Tmore': 2307,
                'Tless': 2407,
                'Tequalmore': 2507,
                'Tequalless': 2607,
                'Tplus': 2707,
                'Tminus': 2807,
                'Tmul': 2907,
                'Tdiv': 3007,
                'Tdivint': 3107,
                'Tmod': 3207,
                'Tcomma': 3307,
                'Topenblock': 3407
                }

Comments = {'Tcomment': '#[^\n]*',
            'Teol': '\n',
            'Tmulticomment': '\'\'\''}

Ignores = {'Tspace': ' ',
           'Tdotcomma': ';'
           }


# Класс сканера
class lexical_scanner:
    def __init__(self):
        self.text = [];
        self.preparedText = [];
        self.lexemsAnalysed = [];

    # Метод удаления всех комментариев
    def deleteComments(self):

        isComment = False;
        result = []

        for current in self.text:
            for pattern in Comments:

                if (re.match(Comments[pattern], current) and pattern == 'Tmulticomment'):
                    isComment = isComment ^ True;

                if (isComment and pattern == 'Tmulticomment'):
                    current = ''
                    break

                current = current.strip(' ')
                current = re.sub(Comments[pattern], '', current)

            if (len(current) > 0 and re.fullmatch('_+', current) == None):
                # print(current)
                result.append(current)
        self.preparedText = result;
        if (isComment):
            self.markError(("No ending on comment"));

    # Метод извещения об ошибке
    def markError(self, element):
        print("Lexical error at " + str(element));
        fout.write("Lexical error at " + str(element) + "\n");

    # Метод чтения следующей лексемы
    # Возврщаемый тип (Имя лексемы, обозначение, индекс в строке, длина, индекс лексемы)
    def nextLexem(self, line, start):

        index = start + 1

        if (line[start] == ','):
            return ('Tcomma', line[start:index], start, 1, 1001)

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
        if (line[start] == ':'):
            return ('Topenblock', line[start:index], start, 1, 3212)
        if (line[start] == '{'):
            return ('Ttabblock', line[start:index], start, 1, 3313)

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
        for line in self.preparedText:
            lexemLine = []
            index = 0

            while len(line) > index:
                if (re.match(' |;', line[index]) != None):
                    index += 1
                    continue

                currentLexem = self.nextLexem(line, index)
                #if (currentLexem[0] == 'Terror'):
                    # fout.write(str(currentLexem))
                    # return False

                lexemLine.append(currentLexem)
                index += currentLexem[3]
            self.lexemsAnalysed.append(lexemLine)
        return True  # self.correctLexemTiming()

    # Метод вывода лексем
    def showLexems(self):
        for current in self.lexemsAnalysed:
            fout.write(str(current) + "\n")

    def correctLexemTiming(self):
        for lexem in self.lexemsAnalysed:
            prev = ()
            for lexem2 in lexem:
                if (prev != () and lexem2[4] % 100 == prev[4] % 100 and lexem2[4] % 100 == 1):
                    self.markError(("Incorrect lexem order on", (prev, lexem2)))
                    return False
                prev = lexem2
        return True


scanner = lexical_scanner()
try:
    scanner.text = fin.readlines()
except Exception:
    print(str(Exception))
finally:
    scanner.deleteComments()
    if (scanner.scanAllLexems()):
        scanner.showLexems()



fout.close()
