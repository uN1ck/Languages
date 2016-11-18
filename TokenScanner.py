import re


class token:
    def __init__(self, tokenName, tokenID, token, tokenPosition, tokenStringIndex):
        self.tokenName = tokenName
        self.tokenID = tokenID
        self.tokenPosition = tokenPosition
        self.token = token.strip()
        self.tokenStringIndex = tokenStringIndex

    def __len__(self):
        return len(self.token)

    def __str__(self):
        return "[ Name: " + str(self.tokenName) + " ID: " + str(self.tokenID) + " Token: \"" + str(
            self.token) + "\" at: " + str(self.tokenStringIndex + 1) + "|" + str(self.tokenPosition + 1) + " ]"


class scanner:
    tokens = [('Tdef', 'def'),
              ('Twhile', 'while'),
              ('Treturn', 'return'),
              ('Tor', 'or'),
              ('Tand', 'and'),
              ('Tif', 'if'),
              ('Tconst10', '[1-9][0-9]*'),
              ('Tconst16', '0x[0-9A-F]+'),
              ('Tid', '[a-zA-Z]+'),
              ('Tequal', '=='),
              ('Tnotequal', '!='),
              ('Tequalmore', '>='),
              ('Tequalless', '<='),
              ('Tmore', '>[^=]'),
              ('Tless', '<[^=]'),
              ('Tassignment', '=[^=<>]'),
              ('Tplus', '\+'),
              ('Tminus', '\-'),
              ('Tmul', '\*'),
              ('Tdivint', '//'),
              ('Tdiv', '/'),
              ('Tmod', '%'),
              ('Tcomma', ','),
              ('Topenbracket', '\('),
              ('Tclosebracket', '\)'),
              ('Topenblock', '\{'),
              ('Tcloseblock', '\}')
              ]
    сomments = {'Tcomment': '#[^\n]*',
                'Teol': '\n',
                'Tmulticomment': '\'\'\''
                }

    def __init__(self, text):
        self.text = text
        self.tokensDetected = []

    # Метод определения одного блока, либо систем ывложенных блоков
    def _defineBlock(self, index, lines):

        currentGap = 0
        isDetected = False
        lineIndex = index

        while lineIndex < len(lines):
            line = lines[lineIndex]

            if (':' in line and not isDetected):
                lines[lineIndex] = line.replace(':', '{')
                while (currentGap + 4 < len(line) and line[currentGap:currentGap + 4] == '    '):
                    currentGap += 4
                currentGap += 4
                isDetected = True
            elif (':' in line and isDetected):
                gap = 0
                while (gap + 4 < len(line) and line[gap:gap + 4] == '    '):
                    gap += 4
                if (gap != currentGap):
                    lines[lineIndex - 1] += ' }'
                    isDetected = False
                    currentGap = 0
                lineIndex = self._defineBlock(lineIndex, lines)
            elif (isDetected):
                gap = 0
                while (gap + 4 < len(line) and line[gap:gap + 4] == '    '):
                    gap += 4
                if (gap != currentGap):
                    lines[lineIndex - 1] += ' }'
                    isDetected = False
                    currentGap = 0
                    return lineIndex

            lineIndex += 1
        return lineIndex

    # Метод определения всех блоков
    def defineBlocks(self):
        lineIndex = 0

        while (lineIndex < len(self.text)):
            lineIndex = self._defineBlock(lineIndex, self.text)
            lineIndex += 1

    # Метод извещения об ошибке
    def markError(self, element):
        print("Lexical error " + str(element))
        raise Exception('Lexical error', str(element))

    # Удаление игнорируемых символов
    def deleteComments(self):

        isComment = False
        result = []

        for current in self.text:
            for pattern in self.сomments:

                if (re.match(self.сomments[pattern], current) and pattern == 'Tmulticomment'):
                    isComment = isComment ^ True

                if (isComment and pattern == 'Tmulticomment'):
                    current = ''
                    break

                current = current.strip(' ')
                current = re.sub(self.сomments[pattern], '', current)

            if (len(current) > 0 and re.fullmatch('_+', current) == None):
                result.append(current)
        self.text = result
        if (isComment):
            self.markError(("No ending on comment"))

    # Взятие лексемы из строки по индексу символа начала лексемы
    def _nextLexem(self, line, index, stringIndex, tabIndex):
        base = index
        while (index < len(line)):
            if (line[index] == ' '):
                index += 1
            else:
                break

        for cToken in self.tokens:
            currentMatch = re.match(cToken[1], line[index:])
            if (currentMatch != None):
                return (token(cToken[0], hash(cToken[0]), currentMatch.group(), index + 4 * tabIndex, stringIndex),
                        index + len(currentMatch.group()) - base)
        self.markError("Unexpected token: \"" + str(line[index]) + "\" at: " + line)

    # Лексический разбор текста
    def lexems(self):

        stringIndex = 0
        tabIndex = 0

        for line in self.text:
            if ('{' in line): tabIndex += 1

            lineIndex = 0
            while (lineIndex < len(line)):
                current = self._nextLexem(line, lineIndex, stringIndex, tabIndex)
                lineIndex += current[1]
                self.tokensDetected.append(current[0])
            stringIndex += 1

            if ('}' in line): tabIndex -= 1

    # Обработать текст
    def getTokens(self):
        self.prepareText()
        self.lexems()
        return self.tokensDetected

    # Препроцессинг текста
    def prepareText(self):
        self.defineBlocks()
        self.deleteComments()

#
# scn = scanner(open("input.txt").readlines())
# for token in scn.getTokens():
#     print(str(token.token) + " ")
