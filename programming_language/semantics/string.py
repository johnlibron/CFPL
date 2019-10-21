from programming_language.semantics.number import Number
from programming_language.semantics.value import Value

class String(Value):

    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return f'"{self.value}"'

    def __str__(self):
        return self.value

    def add(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multiply(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return len(self.value) > 0