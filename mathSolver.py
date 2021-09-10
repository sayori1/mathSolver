symtable = {'x': 10, 'y': 10}


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return self.type + " " + self.value


class StateMachine:

    def __init__(self, iterable):
        self.c = 0
        self.iterable = iterable

    def get(self):
        if(self.c < len(self.iterable)):
            return self.iterable[self.c]
        else:
            return None

    def advance(self):
        self.c += 1


class Lexer(StateMachine):

    operators = ['+', '-', '*', '/', '(', ')', '^', '=', ':']

    def __init__(self, raw):
        super().__init__(raw)

    def parse(self):
        tokens = []
        while(self.get() != None):
            if(self.get() in Lexer.operators):
                tokens.append(Token('operator', self.get()))
                self.advance()
            elif(self.get() == ' '):
                self.advance()
            else:
                buf = ''
                if(self.get() and self.get().isdigit() or self.get() == '.'):
                    while(self.get() and self.get().isdigit() or self.get() == '.'):
                        buf += self.get()
                        self.advance()
                    tokens.append(Token('number', buf))

                elif(self.get() and self.get().isalpha()):
                    while(self.get() and self.get().isalpha()):
                        buf += self.get()
                        self.advance()
                    tokens.append(Token('variable', buf))


        return tokens


## PARSER ##

funcs = []

class Operation:

    def __init__(self, left, right, op):
        self.left=left
        self.right=right
        self.op=op

    def eval(self):
        if(self.op == '+'):
            return self.left.eval() + self.right.eval()
        elif(self.op == '-'):
            return self.left.eval() - self.right.eval()
        elif(self.op == '*'):
            return self.left.eval() * self.right.eval()
        elif(self.op == '/'):
            return self.left.eval() / self.right.eval()
        elif(self.op == '^'):
            return self.left.eval() ** self.right.eval()

class Number:
    def __init__(self, value):
        self.value=value

    def eval(self):
        return self.value

class Variable:
    def __init__(self, name):
        self.name=name

    def eval(self):
        if(self.name == ''):
            return 1.0
        return symtable[self.name]

class Function:
    def __init__(self, variable, operation):
        self.variable = variable
        self.operation = operation
    def eval(self):
        return self.operation.eval()

class Parser(StateMachine):
    def __init__(self, tokens):
        super().__init__(tokens)

    def check(self,type,value = ''):
        if(type == self.get().type):
            if(self.get() != '' and self.get().value != value):
                print('unexpected token')
                return None
            else:
                t = self.get().value
                self.advance()
                return t
        else:
            print('unexpected token')
            return None

        
    def factor(self):
        if(self.get().type == 'number'):
            n = self.get().value
            self.advance()

            if(self.get() and self.get().type == 'variable'): #for polynomials
                return Operation(Number(float(n)), self.factor(), '*')
            return Number(float(n))
        if(self.get().type == 'variable'):
            name = self.get().value
            self.advance()
            return Variable(name)
        if(self.get().type == 'operator' and self.get().value == '('):
            self.advance()
            n = self.subAdd()
            self.advance()
            return n
        
    def mulDiv(self):
        left=self.factor()
        if(self.get() and self.get().type == 'operator' and self.get().value in ['*', '/', '^']):
            op=self.get().value
            self.advance()
            return Operation(left, self.mulDiv(), op)
        else:
            return left

    def subAdd(self):
        left=self.mulDiv()
        if(self.get() and self.get().type == 'operator' and self.get().value in ['+', '-']):
            op=self.get().value
            self.advance()
            return Operation(left, self.subAdd(), op)
        else:
            return left

    def build():
        pass


def test():
    lexer=Lexer("123*123*43*2x+ 100x^2 +(12 + 523) ")
    tokens=lexer.parse()
    parser=Parser(tokens)
    print(parser.subAdd().eval())


test()
