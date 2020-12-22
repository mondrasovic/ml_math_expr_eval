import abc
import numbers
import operator
import dataclasses


@dataclasses.dataclass()
class EvalContext:
    dec_places: int = 3
    n_spaces: int = 1


class Expression(abc.ABC):
    @abc.abstractmethod
    def eval(self, context=None):
        pass
    
    @abc.abstractmethod
    def as_str(self, context=None):
        pass


class Constant(Expression):
    def __init__(self, val):
        self.val = val
    
    def eval(self, context=None):
        return self.val
    
    def as_str(self, context=None):
        dec_places = 3 if context is None else context.dec_places
        return f'{self.val:.{dec_places}f}'


class MathOperation(Expression):
    def __init__(self, x, y, operation, symbol, *, requires_brackets=True):
        self.x = self._as_constant(x)
        self.y = self._as_constant(y)
        self.operation = operation
        self.symbol = symbol
        self.requires_brackets = requires_brackets
    
    def eval(self, context=None):
        left_val, right_val = self.x.eval(context), self.y.eval(context)
        return self.operation(left_val, right_val)
    
    def as_str(self, context=None):
        sep = '' if context is None else context.n_spaces * ' '
        left_str, right_str = self.x.as_str(context), self.y.as_str(context)
        
        if self.requires_brackets:
            if not isinstance(self.x, Constant):
                left_str = f'({left_str})'
            if not isinstance(self.y, Constant):
                right_str = f'({right_str})'
        
        return f'{left_str}{sep}{self.symbol}{sep}{right_str}'
    
    @staticmethod
    def _as_constant(val):
        return Constant(val) if isinstance(val, numbers.Number) else val


class AddOperation(MathOperation):
    def __init__(self, x, y):
        super().__init__(x, y, operator.add, '+', requires_brackets=False)


class SubOperation(MathOperation):
    def __init__(self, x, y):
        super().__init__(x, y, operator.sub, '-')


class MulOperation(MathOperation):
    def __init__(self, x, y):
        super().__init__(x, y, operator.mul, '*')


class DivOperation(MathOperation):
    def __init__(self, x, y):
        super().__init__(x, y, operator.truediv, '/')


class PowOperation(MathOperation):
    def __init__(self, x, y):
        super().__init__(x, y, operator.pow, '^')


if __name__ == '__main__':
    context = EvalContext(n_spaces=1)
    expr = MulOperation(
        AddOperation(2, 5), AddOperation(
            PowOperation(2, 2), DivOperation(1, SubOperation(2, 1))))
    print(expr.eval(context))
    print(expr.as_str(context))
