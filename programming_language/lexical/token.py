import string

class Token:

    def __init__(self, type_, value=None, pos_start=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

    def matches(self, type_, value):
        return self.type == type_ and self.value == value


Token.DIGITS         = '0123456789'
Token.LETTERS        = string.ascii_letters
Token.LETTERS_DIGITS = Token.LETTERS + Token.DIGITS

Token.IDENTIFIER     = 'IDENTIFIER'
Token.KEYWORD        = 'KEYWORD'
Token.DATA_TYPE      = 'DATA_TYPE'

Token.VAR            = 'VAR'
Token.AS             = 'AS'
Token.EQ             = 'EQUAL'

Token.INT            = 'INT'
Token.CHAR           = 'CHAR'
Token.BOOL           = 'BOOL'
Token.FLOAT          = 'FLOAT'

Token.TRUE           = 'TRUE'
Token.FALSE          = 'FALSE'

Token.AND            = 'AND'
Token.OR             = 'OR'
Token.NOT            = 'NOT'

Token.PLUS           = 'PLUS'
Token.MINUS          = 'MINUS'
Token.MUL            = 'MUL'
Token.DIV            = 'DIV'
Token.MOD            = 'MOD'

Token.EE             = 'EQUAL_TO'
Token.NE             = 'NOT_EQUAL_TO'
Token.LT             = 'LESS_THAN'
Token.GT             = 'GREATER_THAN'
Token.LTE            = 'LESS_THAN_OR_EQUAL_TO'
Token.GTE            = 'GREATER_THAN_OR_EQUAL_TO'

Token.POSITIVE       = 'POSITIVE'
Token.NEGATIVE       = 'NEGATIVE'

Token.IF             = 'IF'
Token.ELIF           = 'ELIF'
Token.ELSE           = 'ELSE'

Token.WHILE          = 'WHILE'

Token.LPAREN         = 'LPAREN'
Token.RPAREN         = 'RPAREN'
Token.LSQUARE        = 'LSQUARE'
Token.RSQUARE        = 'RSQUARE'
Token.CONCAT         = 'CONCAT'
Token.COMMA          = 'COMMA'
Token.COLON          = 'COLON'

Token.OUTPUT         = 'OUTPUT'
Token.START          = 'START'
Token.STOP           = 'STOP'
Token.NEWLINE        = 'NEWLINE'
Token.COMMENT        = 'COMMENT'
Token.EOL            = 'EOL'

Token.KEYWORDS = [
    'VAR',
    'AS',
    'AND',
    'OR',
    'NOT',
    'TRUE',
    'FALSE',
    'IF',
    'ELIF',
    'ELSE',
    'WHILE',
    'START',
    'STOP',
    'OUTPUT'
]

Token.DATA_TYPES = [
    'INT',
    'FLOAT',
    'CHAR',
    'BOOL'
]

Token.BOOL_VALUES = [
    'TRUE',
    'FALSE'
]