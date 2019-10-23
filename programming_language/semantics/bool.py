from programming_language.error_handler.error import RuntimeError
from programming_language.lexical.token import Token
from programming_language.semantics.number import Number
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
        if isinstance(other, Bool):
            self.value = True if self.value == Token.TRUE else False
            other.value = True if other.value == Token.TRUE else False
            return Bool(Token.TRUE if self.value and other.value else Token.FALSE).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_or(self, other):
        if isinstance(other, Bool):
            self.value = True if self.value == Token.TRUE else False
            other.value = True if other.value == Token.TRUE else False
            return Bool(Token.TRUE if self.value or other.value else Token.FALSE).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_not(self):
        self.value = True if self.value == Token.TRUE else False
        return Bool(Token.TRUE if self.value == False else Token.FALSE).set_context(self.context), None

    def copy(self):
        copy = Bool(self.value)
        copy.set_pos(self.pos_start)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        self.value = True if self.value == Token.TRUE else False
        return self.value != False