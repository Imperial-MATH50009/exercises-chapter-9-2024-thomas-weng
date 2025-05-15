"""DOCSRTING."""
import numbers
from functools import singledispatch


class Expression:
    """DOCSRTING."""

    def __init__(self, *operands):
        """DOCSRTING."""
        self.operands = operands

    def __add__(self, other):
        """DOCSRTING."""
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Add(self, other)

    def __radd__(self, other):
        """DOCSRTING."""
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Add(other, self)

    def __sub__(self, other):
        """DOCSRTING."""
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Sub(self, other)

    def __rsub__(self, other):
        """DOCSRTING."""
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Sub(other, self)

    def __mul__(self, other):
        """DOCSRTING."""
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Mul(self, other)

    def __rmul__(self, other):
        """DOCSRTING."""
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Mul(other, self)

    def __truediv__(self, other):
        """DOCSRTING."""
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Div(self, other)

    def __rtruediv__(self, other):
        """DOCSRTING."""
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Div(other, self)

    def __pow__(self, other):
        """DOCSRTING."""
        if isinstance(other, numbers.Number):
            other = Number(other)
        return Pow(self, other)

    def __rpow__(self, other):
        """DOCSRTING."""
        if isinstance(other, numbers.Number):
            return Pow(Number(other), self)
        return NotImplemented


class Operator(Expression):
    """DOCSRTING."""

    def __repr__(self):
        """DOCSRTING."""
        return type(self).__name__ + repr(self.operands)

    def __str__(self):
        """DOCSRTING."""

        def brack(expr):
            if expr.prec < self.prec:
                return f"({expr!s})"
            else:
                return str(expr)

        return " ".join((brack(self.operands[0]),
                        self.symbol, brack(self.operands[1])))


class Add(Operator):
    """DOCSRTING."""

    prec = 0
    symbol = "+"


class Sub(Operator):
    """DOCSRTING."""

    prec = 0
    symbol = "-"


class Mul(Operator):
    """DOCSRTING."""

    prec = 1
    symbol = "*"


class Div(Operator):
    """DOCSRTING."""

    prec = 1
    symbol = "/"


class Pow(Operator):
    """DOCSRTING."""

    prec = 2
    symbol = "^"


class Terminal(Expression):
    """DOCSRTING."""

    prec = 3

    def __init__(self, value):
        """DOCSRTING."""
        self.value = value
        super().__init__()

    def __repr__(self):
        """DOCSRTING."""
        return repr(self.value)

    def __str__(self):
        """DOCSRTING."""
        return str(self.value)


class Symbol(Terminal):
    """Docstring."""

    def __init__(self, value):
        """DOCSRTING."""
        if isinstance(value, str):
            super().__init__(value)


class Number(Terminal):
    """DOCSRTING."""

    def __init__(self, value):
        """DOCSRTING."""
        if isinstance(value, numbers.Number):
            super().__init__(value)


def postvisitor(expr, fn, **kwargs):
    """DOCSRTING."""
    stack = []
    visited = {}
    stack.append(expr)
    while stack:
        e = stack[-1]
        stack = stack[:-1]
        unvisited_children = []
        for o in e.operands:
            if o not in visited:
                unvisited_children.append(o)

        if unvisited_children:
            stack.append(e)
            for i in unvisited_children:
                stack.append(i)
        else:
            visited[e] = fn(e, *(visited[o] for o in e.operands), **kwargs)

    return visited[expr]


@singledispatch
def differentiate(expr, *o, **kwargs):
    """DOCSRTING."""
    raise NotImplementedError(
        f"Cannot differentiate a {type(expr).__name__}")


@differentiate.register(Number)
def _(expr, *o, **kwargs):
    return 0.0


@differentiate.register(Symbol)
def _(expr, *o, **kwargs):
    if kwargs['var'] == expr.value:
        return 1.0
    else:
        return 0.0


@differentiate.register(Add)
def _(expr, *o, **kwargs):
    return o[0] + o[1]


@differentiate.register(Sub)
def _(expr, *o, **kwargs):
    return o[0] - o[1]


@differentiate.register(Mul)
def _(expr, *o, **kwargs):
    return (o[0]*expr.operands[1] + o[1]*expr.operands[0])


@differentiate.register(Div)
def _(expr, *o, **kwargs):
    return (o[0] * expr.operands[1] - expr.operands[0]
            * o[1]) / (expr.operands[1]**2)


@differentiate.register(Pow)
def _(expr, *o, **kwargs):
    return expr.operands[1] * \
            (expr.operands[0] ** (expr.operands[1] - 1)) * o[0]
