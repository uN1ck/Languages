import re

from TokenScanner import scanner

nonTerminalTokens = {"program", "expression", "function_def", "operator", "operation", "name_list_tail", "name_list",
                     "block", "A1", "A2", "A3", "A4", "A5", "A1R", "A2R", "A3R", "A4R", "function_call", "assignment",
                     "while_cycle", "return_op", "parameters_list", "parameters_list_tail", ""}

terminalTokens = {">", ">=", "==", "<=", "<", "!=", "+", "-", "/", "//", "", "%", "*", "=", "name", "while", "integer",
                  "(", ")", "{", "}", "def", "or", "not", "return", "#"}

LL1Table = {
    "program"             : {
        "name"   : ["program", "expression"],
        "while"  : ["program", "expression"],
        "integer": ["program", "expression"],
        "("      : ["program", "expression"],
        "{"      : ["program", "expression"],
        "def"    : ["program", "expression"],
        "return" : ["expression"],
        "}"      : ["E"],
        ")"      : ["E"],
        "#"      : ["E"]
    },
    "expression"          : {
        "name"   : ["operator", "operation"],  # Чекнуть оператор или операция
        "while"  : ["operator"],
        "integer": ["operation"],
        "{"      : ["operator"],
        "("      : ["operation"],
        "def"    : ["function_def"],
        "return" : ["operator"]
    },
    "function_def"        : {
        "def": [")", "name_list", "(", "name", "def"]
    },
    "operator"            : {
        "name"  : ["assignment"],
        "while" : ["while_cycle"],
        "{"     : ["block"],
        "return": ["return_op"]
    },
    "operation"           : {
        "name"   : ["A1"],
        "integer": ["A1"],
        "("      : ["A1"],
        "any"    : ["E"],
    },
    "name_list_tail"      : {
        "name": ["name_list"],
        "any" : ["E"]
    },
    "name_list"           : {
        "name": ["name_list_tail", "name"],
    },
    "block"               : {
        "{": ["}", "program", "{"]
    },
    "A1"                  : {
        "name"   : ["A1R", "A2"],
        "integer": ["A1R", "A2"],
        "("      : ["A1R", "A2"],

    },
    "A2"                  : {
        "name"   : ["A2R", "A3"],
        "integer": ["A2R", "A3"],
        "("      : ["A2R", "A3"],

    },
    "A3"                  : {
        "name"   : ["A3R", "A4"],
        "integer": ["A3R", "A4"],
        "("      : ["A3R", "A4"],

    },
    "A4"                  : {
        "name"   : ["A4R", "A5"],
        "integer": ["A4R", "A5"],
        "("      : ["A4R", "A5"],

    },
    "A5"                  : {
        "name"   : ["name"],
        "integer": ["integer"],
        "("      : [")", "operation", "("],

    },
    "A1R"                 : {
        ">"  : ["A1", ">"],
        ">=" : ["A1", ">="],
        "==" : ["A1", "=="],
        "!=" : ["A1", "!="],
        "<=" : ["A1", "<="],
        "<"  : ["A1", "<"],
        "any": ["E"],
    },
    "A2R"                 : {
        "+"  : ["A2", "+"],
        "-"  : ["A2", "-"],
        "any": ["E"],
    },
    "A3R"                 : {
        "/"  : ["A3", "/"],
        "//" : ["A3", "//"],
        "%"  : ["A3", "%"],
        "*"  : ["A3", "*"],
        "any": ["E"],
    },
    "A4R"                 : {
        "and": ["A4", "and"],
        "or" : ["A4", "or"],
        "not": ["A4", "not"],
        "any": ["E"]
    },
    "function_call"       : {
        "name": [")", "parameters_list", "(", "name"]
    },
    "assignment"          : {
        "name": ["operation", "=", "name"]
    },
    "while_cycle"         : {
        "while": [")", "operation", "(", "while"]
    },
    "return_op"           : {
        "return": ["expression", "return"]
    },
    "parameters_list"     : {
        "name"     : ["parameters_list_tail", "name"],
        "operation": ["parameters_list_tail", "operation"],

    },
    "parameters_list_tail": {
        "name"     : ["parameters_list"],  # Чекнуть нуль не нуль
        "operation": ["parameters_list"],
        "any"      : ["E"]
    },
    "E"                   : {

    }
}


class LLOne:
    def __init__(self, token_list, table):
        self.stack = ["#", "program"]
        self.tokenList = token_list
        self.tokenListPosition = 0
        self.table = table

    def _next_token(self):
        self.tokenListPosition += 1
        return self.tokenList[self.tokenListPosition] is not None

    def _current_token(self):
        return self.tokenList[self.tokenListPosition]

    def _peek(self):
        return self.stack[len(self.stack) - 1]

    def _pop(self):
        res = self.stack[len(self.stack) - 1]
        self.stack.pop(len(self.stack) - 1)
        return res

    def _put(self, value):
        self.stack.append(value)

    @staticmethod
    def mark_error(message):
        print(message)
        raise Exception('Exception! -> ', message)

    def do_analyse(self):
        while True:
            if self._peek() in terminalTokens:
                if self._peek() == self._current_token().tokenName:
                    if self._current_token().tokenName == "#":
                        return True
                    else:
                        self._next_token()
                        self.stack.pop()
                        continue
                else:
                    self.mark_error("Unexpected token: " + str(self._current_token()))
            else:
                if self._current_token().tokenName in self.table[self._peek()]:
                    buffer = self._pop()

                    # Разрешение конфликта в выражении
                    if self._current_token().tokenName == "name" and buffer == "expression":
                        if re.match("<|<=|==|>=|>|!=|\*|/|//|%|\+|-|and|or|not|\(", self.tokenList[self.tokenListPosition + 1].tokenName):
                            self._put("operation")
                        else:
                            self._put("operator")
                    # Разрешение конфликта в A5б когда мы снова не знаем, функцияэто или имя
                    elif self._current_token().tokenName == "name" and buffer == "A5":
                        if self.tokenList[self.tokenListPosition + 1].tokenName == "(":
                            self._put("function_call")
                        else:
                            self._put("name")
                    else:
                        for current in self.table[buffer][self._current_token().tokenName]:
                            self._put(current)
                else:
                    if "any" in self.table[self._peek()]:
                        buffer = self._pop()
                        for current in self.table[buffer]["any"]:
                            self._put(current)
                        continue
                    if self._peek() == "E":
                        self._pop()
                        continue
                    self.mark_error("Unexpected token: " + str(self._current_token()))


scn = scanner(open("input.txt").readlines())
res = scn.getTokens()
TA = LLOne(res, LL1Table)
try:
    if TA.do_analyse():
        print("Passed!")
    else:
        print("NOT Passed!")
except Exception as e:
    print("NOT Passed!")