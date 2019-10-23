from programming_language.error_handler.error import RuntimeError
from programming_language.lexical.token import Token
from programming_language.semantics.value import Value

class Number(Value):

    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def add(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def subtract(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multiply(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def divide(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RuntimeError(
                    other.pos_start,
                    'Division by zero',
                    self.context
                )

            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def modulo(self, other):
        if isinstance(other, Number):
            return Number(self.value % other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def concat(self, other):
        if isinstance(other, Number) or isinstance(other.value, str):
            return Number(str(self.value) + str(other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(Token.TRUE if self.value == other.value else Token.FALSE).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(Token.TRUE if self.value != other.value else Token.FALSE).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(Token.TRUE if self.value < other.value else Token.FALSE).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(Token.TRUE if self.value > other.value else Token.FALSE).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(Token.TRUE if self.value <= other.value else Token.FALSE).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(Token.TRUE if self.value >= other.value else Token.FALSE).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_and(self, other):
        if isinstance(other, Number):
            self.value = True if self.value == Token.TRUE else False
            other.value = True if other.value == Token.TRUE else False
            return Number(Token.TRUE if self.value and other.value else Token.FALSE).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_or(self, other):
        if isinstance(other, Number):
            self.value = True if self.value == Token.TRUE else False
            other.value = True if other.value == Token.TRUE else False
            return Number(Token.TRUE if self.value or other.value else Token.FALSE).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_not(self):
        self.value = True if self.value == Token.TRUE else False
        return Number(Token.TRUE if self.value == Token.FALSE else Token.FALSE).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        self.value = True if self.value == Token.TRUE else False
        return self.value != 0 or self.value != False