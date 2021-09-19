class StateMachine:
    def __init__(self, arr):
        self.arr = arr
        self.c = 0

    def advance(self):
        r = self.current()
        self.c += 1
        return r

    def current(self):
        if(self.c < len(self.arr)):
            return self.arr[self.c]
        else:
            return None

    def eat(self, value):
        if(self.c == value):
            return self.current()
        else:
            print("unexpected token ", value )

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __str__(self):
        return str(self.type) + " " + str(self.value)

## LEXER

class Lexer(StateMachine):
    operators = ['+', '-', '*', '/', '(', ')', '=', ','] 

    def __init__(self, raw):
        super().__init__(raw)
    
    def parse(self):
        tokens = []
        while(self.current() != None):
            if(self.current() in Lexer.operators):
                tokens.append(Token("operator", self.advance() ) )
            elif(self.current().isdigit()):
                buf = ""
                while(self.current() and self.current().isdigit() or self.current() == '.'):
                    buf += self.advance()
                tokens.append(Token("number", buf ))
            elif(self.current().isalpha()):
                buf = ""
                while(self.current() and self.current().isalpha()):
                    buf += self.advance()
                tokens.append(Token("string", buf ))
            elif(self.current() == ' '):
                self.advance()
        return tokens

## AST OBJECTS

class Number:
    def __init__(self, value):
        self.value = float(value)

    def calc(self):
        return self.value

class Operation:
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def calc(self):
        if(self.op == '+'):
            return self.left.calc() + self.right.calc()
        elif(self.op == '-'):
            return self.left.calc() - self.right.calc()
        elif(self.op == '*'):
            return self.left.calc() * self.right.calc()
        elif(self.op == '/'):
            return self.left.calc() / self.right.calc()
        elif(self.op == '^'):
            return self.left.calc() ** self.right.calc()

class Variable:
    table = {'x':1}
    def __init__(self, name, value = None):
        self.name = name
        if(value != None):
            Variable.table[name] = value
    def calc(self):
        return Variable.table[self.name]

class Function: #f(x) = x + 1
    table = {}

    def __init__(self, name, operation, enumeration):
        self.name = name
        Function.table[name] = operation

    def calc(self):
        return Function.table[self.name].calc()

class FunctionCall: #f(x)
    def __init__(self, name, enumeration):
        self.name = name
    
    def calc(self):
        pass

class Enumeration:
    def __init__(self, arr):
        self.arr = arr

## PARSER

class Parser(StateMachine):
    def __init__(self, tokens):
        super().__init__(tokens)

    def check(self, type, values = []):
        if(self.current() and self.current().type == type):
            if(values == []):
                return True
            else:
                return self.current().value in values
        return False

    def advanceIf(self, type, values = []):
        if(self.check(type, values)):
            return self.advance()
        else:
            print("unexpected token: expected ", type, values, " but got ", self.current().type, self.current().value)

    def factor(self):

        if(self.check('number')):
            return Number(self.advance().value)

        if(self.check('operator', ['('])):
            self.advance()
            expression = self.mulDiv()

            self.check('operator', [')'])
            self.advance()

            return expression

        if(self.check('string')):
            print(self.current().value)
            return Variable(self.advance().value)

    def mulDiv(self):
        left = self.factor()
        if(self.check('operator',['*', '/'] ) ):
            op = self.advance().value
            return Operation(left, self.mulDiv(), op)
        else:
            return left
    
    def subAdd(self):
        left = self.mulDiv()
        if(self.check("operator", ['+', '-'])):
            op = self.advance().value
            return Operation(left, self.subAdd(), op)
        else:
            return left

    def enumeration(self):
        self.advanceIf("operator", ['('])
        enum = []
        while(not self.check('operator', [')'])):
            enum.append(self.factor())
            self.advanceIf("operator", [','])
        self.advance()
        return Enumeration(enum)

    def func(self):
        name = self.advanceIf("string", [])
        enum = self.enumeration()
        self.advanceIf("operator", ["="])
        operation = self.subAdd()
        return Function(name, operation, enum)


lexer = Lexer("f(x)=1+x")
parser = Parser(lexer.parse())
print(parser.func().calc() )