import random

from mathexpr import AddOperation, SubOperation, MulOperation, DivOperation,\
    PowOperation, Constant, EvalContext

_OPERATIONS = (
    AddOperation, SubOperation, MulOperation, DivOperation,
    PowOperation)

def _generate_branch(rem_depth):
    if rem_depth <= 0:
        return None
    if rem_depth == 1:
        return Constant(random.randint(-5, 5))
    else:
        new_rem_depth = rem_depth - 1
        left = _generate_branch(new_rem_depth)
        right = _generate_branch(new_rem_depth)
        operation = random.choice(_OPERATIONS)(left, right)
        return operation

def generate_expression(depth):
    return _generate_branch(depth)

if __name__ == '__main__':
    context = EvalContext(n_spaces=1)
    n_expressions = 10
    depth = 5
    
    for _ in range(n_expressions):
        expression = generate_expression(depth)
        try:
            print(f'{expression.as_str(context)} = {expression.eval(context)}')
        except ZeroDivisionError:
            pass
