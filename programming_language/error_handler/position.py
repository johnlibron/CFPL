class Position:

    def __init__(self, index, line, text):
        self.index = index
        self.line = line
        self.text = text

    def advance(self, current_char=None):
        self.index += 1

        if current_char == ';':
            self.line += 1

        return self

    def copy(self):
        return Position(self.index, self.line, self.text)
