class ParseResult:

    def __init__(self):
        self.node = None
        self.error = None
        self.last_registered_advance_count = 0
        self.advance_count = 0

    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self, result):
        self.last_registered_advance_count = result.advance_count
        self.advance_count += result.advance_count
        if result.error: self.error = result.error
        return result.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self
