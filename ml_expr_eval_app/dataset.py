from torch.utils.data import IterableDataset, DataLoader

from exprgen import generate_expressions

class MathExprDataset(IterableDataset):
    def __iter__(self):
        pass
    
    @staticmethod
    def _char_to_idx(c):
        if ord('0') <= c <= ord('9'):
            return c - ord('c')
        