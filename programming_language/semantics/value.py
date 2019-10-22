from programming_language.error_handler.error import RuntimeError
from programming_language.semantics.runtime_result import RuntimeResult

class Value:

    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None):
        self.pos_start = pos_start
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def add(self, other):
        return None, self.illegal_operation(other)

    def subtract(self, other):
        return None, self.illegal_operation(other)

    def multiply(self, other):
        return None, self.illegal_operation(other)

    def divide(self, other):
        return None, self.illegal_operation(other)

    def modulo(self, other):
        return None, self.illegal_operation(other)

    def concat(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_and(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_or(self, other):
        return None, self.illegal_operation(other)

    def execute(self, args):
        return RuntimeResult().failure(self.illegal_operation())

    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other: other = self
        return RuntimeError(
            self.pos_start,
            'Illegal operation',
            self.context
        )