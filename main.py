from decimal import Decimal
from lark import Lark, Transformer
from dataclasses import dataclass
from time import perf_counter as pf

# SYmbolic expression nodes

class Expr:
    def __add__(self, other):
        return Add(self, to_expr(other))

    def __radd__(self, other):
        return Add(to_expr(other), self)

    def __sub__(self, other):
        return Sub(self, to_expr(other))

    def __rsub__(self, other):
        return Sub(to_expr(other), self)

    def __mul__(self, other):
        return Mul(self, to_expr(other))

    def __rmul__(self, other):
        return Mul(to_expr(other), self)

    def __truediv__(self, other):
        return Div(self, to_expr(other))

    def __rtruediv__(self, other):
        return Div(to_expr(other), self)

    def __pow__(self, other):
        return Pow(self, to_expr(other))

    def __neg__(self):
        return Neg(self)


@dataclass(frozen=True)
class Equation:
    left: Expr
    right: Expr

    def __str__(self):
        return f"%s = %s" % (self.left, self.right)
    
@dataclass(frozen=True)
class Symbol(Expr):
    name: str

    def __str__(self):
        return self.name

@dataclass(frozen=True)
class Number(Expr):
    value :float

    def __str__(self):
        return str(int(self.value)) if self.value.is_integer() else str(self.value)

@dataclass(frozen=True)
class Add(Expr):
    left: Expr
    right: Expr

    def __str__(self):
        return f"({self.left}) + ({self.right})"
    
@dataclass(frozen=True)
class Sub(Expr):
    left: Expr
    right: Expr

    def __str__(self):
        return f"({self.left}) - ({self.right})"
    
@dataclass(frozen=True)
class Mul(Expr):
    left: Expr
    right: Expr

    def __str__(self):
        return f"({self.left}) * ({self.right})"

    
@dataclass(frozen=True)
class Div(Expr):
    left: Expr
    right: Expr

    def __str__(self):
        return f"({self.left}) / ({self.right})"
    
@dataclass(frozen=True)
class Pow(Expr):
    left: Expr
    right: Expr

    def __str__(self):
        return f"({self.left}) ^ ({self.right})"

@dataclass(frozen=True)
class Neg(Expr):
    value: Expr

    def __str__(self):
        return f"(-{self.value})"

def to_expr(value):
    if isinstance(value, Expr):
        return value
    if isinstance(value, (int, float)):
        return Number(float(value))
    raise TypeError(f"Cannot convert {value!r} to and expression")


grammar = r"""
    ?start: equation

    ?equation: expression "=" expression -> equation
             | expression

    ?expression: expression "+" expression -> add
               | expression "-" expression -> subtract
               | term
    ?term: term "*" unary -> multiply
         | term "/" unary -> divide
         | unary
    ?unary: "-" unary -> negate
          | "+" unary -> posate
          | power
    ?power: atom "^" unary -> power
          | atom
    ?atom: NUMBER -> number
         | NAME -> variable
         | NUMBER NAME -> variable
         | "(" expression ")"
    
         %import common.NUMBER
         %import common.CNAME -> NAME
         %import common.WS
         %ignore WS
"""
class BuildAST(Transformer):
    def equation(self, items):
        return Equation(to_expr(items[0]), to_expr(items[1]))
    def number(self, items):
        return Number(float(items[0]))

    def variable(self, items):
        return Symbol(str(items[0])) if len(items) == 1 else Mul(items[0],Symbol(str(items[1])))

    def add(self, items):
        return Add(items[0], items[1])

    def subtract(self, items):
        return Sub(items[0], items[1])

    def multiply(self, items):
        return Mul(items[0], items[1])

    def divide(self, items):
        return Div(items[0], items[1])

    def power(self, items):
        return Pow(items[0], items[1])

    def negate(self, items):
        return Neg(items[0])

    def posate(self, items):
        return items[0]


parser = Lark(grammar, parser = "lalr")

builder = BuildAST()

def parse(source):
    tree = parser.parse(source)
    return builder.transform(tree)

def execute(tree):
    if isinstance(tree, Equation):
        return NotImplemented
    if isinstance(tree, Expr):
        if isinstance(tree, Number):
            return tree.value
        if isinstance(tree, Add):
            return execute(tree.left) + execute(tree.right)
        if isinstance(tree, Sub):
            return execute(tree.left) - execute(tree.right)
        if isinstance(tree, Mul):
            return execute(tree.left) * execute(tree.right)
        if isinstance(tree, Div):
            return execute(tree.left) / execute(tree.right)
        if isinstance(tree, Pow):
            return execute(tree.left) ** execute(tree.right)
        if isinstance(tree, Neg):
            return -execute(tree.value)
        

if __name__ == "__main__":
    time = pf()
    result = parse("103*30*203*40/40+39")
    v = execute(result)
    print(result, repr(result))
    print(v)
    end = pf()
    print((end-time)*1e6)
    result = eval("103*30*203*40/40+39")
    print(result)
    end2 = pf()
    print((end2-end)*1e6)