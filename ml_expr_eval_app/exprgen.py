import random

from mathexpr import AddOperation, SubOperation, MulOperation, DivOperation,\
    Constant, EvalContext

_OPERATIONS = (AddOperation, SubOperation, MulOperation, DivOperation)

def _generate_branch(rem_depth, const_range=(-5, 5)):
    if rem_depth <= 0:
        return None
    if rem_depth == 1:
        return Constant(random.randint(*const_range))
    else:
        new_rem_depth = rem_depth - 1
        left = _generate_branch(new_rem_depth)
        right = _generate_branch(new_rem_depth)
        operation = random.choice(_OPERATIONS)(left, right)
        return operation

def generate_expressions(count, depth):
    for _ in range(count):
        done = False
        while not done:
            expr = _generate_branch(depth)
            try:
                expr.eval()
            except (ZeroDivisionError, OverflowError):
                pass
            else:
                done = True
                yield expr

if __name__ == '__main__':
    context = EvalContext(dec_places=0, n_spaces=1)
    n_expressions = 10
    depth = 5
    
    for expr in generate_expressions(n_expressions, depth):
        print(f'{expr.as_str(context)} = {expr.eval(context)}')
