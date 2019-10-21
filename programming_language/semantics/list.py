from programming_language.error_handler.error import RuntimeError
from programming_language.semantics.number import Number
from programming_language.semantics.value import Value

class List(Value):

    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def __str__(self):
        return ", ".join([str(x) for x in self.elements])

    def __repr__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'

    def add(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def subtract(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RuntimeError(
                    other.pos_start,
                    'Element at this index could not be removed from list because index is out of bounds',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def multiply(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)

    def divide(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RuntimeError(
                    other.pos_start,
                    'Element at this index could not be retrieved from list because index is out of bounds',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start)
        copy.set_context(self.context)
        return copy