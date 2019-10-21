class Error:

    def __init__(self, pos_start, error_name, details):
        self.pos_start = pos_start
        self.error_name = error_name
        self.details = details
    
    def message(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'Source Code, line {self.pos_start.line + 1}'
        return result

class IllegalCharacterError(Error):
    
    def __init__(self, pos_start, details):
        super().__init__(pos_start, 'Illegal Character', details)

        
class IllegalVarDeclarationError(Error):
    
    def __init__(self, pos_start, details):
        super().__init__(pos_start, 'Illegal Variable Declaration', details)

class ExpectedCharacterError(Error):
    
    def __init__(self, pos_start, details):
        super().__init__(pos_start, 'Expected Character', details)

class InvalidSyntaxError(Error):
    
    def __init__(self, pos_start, details):
        super().__init__(pos_start, 'Invalid Syntax', details)

class RuntimeError(Error):
    
    def __init__(self, pos_start, details, context):
        super().__init__(pos_start, 'Runtime Error', details)
        self.context = context
    
    def message(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        return result
    
    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'  Source Code, line {str(pos.line + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        
        return 'Traceback (most recent call last):\n' + result