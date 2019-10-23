from programming_language.error_handler.error import RuntimeError
from programming_language.lexical.token import Token
from programming_language.semantics.value import Value

class Bool(Value):

    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def get_comparison_and(self, other):
        if isinstance(other.value, Bool):
            return Bool(self.value and other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_or(self, other):
        if isinstance(other.value, Bool):
            return Bool(self.value or other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def logical_not(self):
        return Bool(Token.TRUE if self.value == Token.FALSE else Token.FALSE).set_context(self.context), None

    def copy(self):
        copy = Bool(self.value)
        copy.set_pos(self.pos_start)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != Token.FALSE