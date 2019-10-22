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
        if isinstance(other, Number):
            exponent = 10
            while other.value >= exponent:
                exponent *= 10
            return Number(self.value * exponent + other.value).set_context(self.context), None
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
            return Number(self.value and other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_or(self, other):
        if isinstance(other, Number):
            return Number(self.value or other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def logical_not(self):
        return Number(Token.TRUE if self.value == Token.FALSE else Token.FALSE).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        if self.value in (Token.TRUE, Token.FALSE):
            return self.value != Token.FALSE
        else:
            return self.value != 0