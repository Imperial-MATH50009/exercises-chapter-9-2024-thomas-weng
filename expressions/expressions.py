class Expression: # noqa D100
    """Docstring."""

    def __init__(self, *operands):
        self.operands = operands

    def change_other(self, other):
        if isinstance(other, Expression):
            return other
        return Number(other)

    def __add__(self, other):
        return Add(self, other)

    def __sub__(self, other):
        return Sub(self, other)

    def __mul__(self, other):
        return Mul(self, other)

    def __truediv__(self, other):
        return Div(self, other)

    def __pow__(self, other):
        return Pow(self, other)

    def __radd__(self, other):
        return Add(self.change_other(other), self)

    def __rsub__(self, other):
        return Sub(self.chnange_other(other), self)

    def __rmul__(self, other):
        return Mul(self.change_other(other), self)

    def __rtruediv__(self, other):
        return Div(self.change_other(other), self)

    def __rpow__(self, other):
        return Pow(self.change_other(other), self)

class Operator(Expression):
    precedence = 0

    def __repr__(self):
        return type(self).name + repr(self.operands)

    associativity = 'left'  # can be 'left' or 'right'

    def __str__(self):
        left, right = self.operands
        left_str = f"({left})" if isinstance(left, Expression) and left.precedence < self.precedence else str(left)

        if self.associativity == 'right':
            right_str = f"({right})" if isinstance(right, Expression) and right.precedence <= self.precedence else str(right)
        else:  # left-associative
            right_str = f"({right})" if isinstance(right, Expression) and right.precedence < self.precedence else str(right)

        return f"{left_str} {self.symbol} {right_str}"


class Terminal(Expression):
    precedence = 5

    def __init__(self, value):
        self.value = value
        super().__init__()

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)


class Number(Terminal):
    def __init__(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Symbol must be an int or a float")
        super().__init__(value)


class Symbol(Terminal):
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("Symbol must be a string")
        super().__init__(name)


class Add(Operator):
    precedence = 1
    symbol = '+'


class Sub(Operator):
    precedence = 1
    symbol = '-'


class Mul(Operator):
    precedence = 2
    symbol = '*'


class Div(Operator):
    precedence = 2
    symbol = '/'


class Pow(Operator):
    precedence = 3
    symbol = "^"
    associativity = "right"