from programming_language.error_handler.error import IllegalCharacterError
from programming_language.error_handler.error import IllegalVarDeclarationError
from programming_language.error_handler.position import Position
from programming_language.lexical.token import Token
from programming_language.semantics.number import Number

class Lexer:

    def __init__(self, text):
        self.text = text
        self.pos = Position(-1, 0, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None
    
    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == '*':
                length = len(tokens)-1
                if length > 0 and tokens[length].type in (Token.INT, Token.FLOAT, Token.IDENTIFIER):
                    tokens.append(Token(Token.MUL, pos_start=self.pos))
                    self.advance()
                else:
                    tokens.append(self.skip_comment())
            elif self.current_char == ';':
                tokens.append(Token(Token.NEWLINE, pos_start=self.pos))
                self.advance()
            elif self.current_char in Token.DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in Token.LETTERS:
                pos_start = self.pos.copy()
                tokens.append(self.make_keywords())
                tokens, error = self.set_default_values(tokens)
                if error:
                    return tokens, IllegalVarDeclarationError(pos_start, "" + error + "")
            elif self.current_char in '"\'':
                tokens.append(self.make_string())
            elif self.current_char == '+':
                tokens.append(Token(Token.PLUS, pos_start=self.pos)) # Token.POSITIVE
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(Token.MINUS, pos_start=self.pos)) # Token.NEGATIVE
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(Token.DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(Token.MOD, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(Token.LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(Token.RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '<':
                tokens.append(self.make_less_than_or_not_equals())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == '&':
                tokens.append(Token(Token.CONCAT, pos_start=self.pos))
                self.advance()
            elif self.current_char == ':':
                tokens.append(Token(Token.COLON, pos_start=self.pos))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(Token.COMMA, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharacterError(pos_start, "'" + char + "'")

        tokens.append(Token(Token.EOL, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in Token.DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
            num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(Token.INT, int(num_str), pos_start)
        else:
            return Token(Token.FLOAT, float(num_str), pos_start)
    
    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t',
            'r': '\r'
        }

        while self.current_char != None and (self.current_char not in '"\'' or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    if self.current_char == "[":
                        print("the square braces([]) are as escape code")
                    elif self.current_char == "]":
                        print("the square braces([]) are as escape code")
                    else:
                        string += self.current_char
            self.advance()
            escape_character = False

        self.advance()
        if string in Token.BOOL_VALUES:
            return Token(Token.BOOL, string, pos_start)
        else:
            return Token(Token.CHAR, string, pos_start)
        
    def make_keywords(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in Token.LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        if id_str in Token.KEYWORDS:
            token_type = Token.KEYWORD
        elif id_str in Token.DATA_TYPES:
            token_type = Token.DATA_TYPE
        else:
            token_type = Token.IDENTIFIER
        return Token(token_type, id_str, pos_start)

    def set_default_values(self, tokens):
        length = len(tokens)-1
        if length > 0:
            data_type = tokens[length].value
            if data_type in Token.DATA_TYPES:
                pos_start = self.pos.copy()
                data_value = None
                for token in reversed(tokens):
                    if token.value == Token.VAR: break
                    if token.type == Token.IDENTIFIER:
                        if data_value == None and tokens[length+1].type != Token.EQ:
                            tokens.insert(length+1, Token(Token.EQ, None, pos_start))
                            if data_type == Token.INT:
                                tokens.insert(length+2, Token(Token.INT, Number.null, pos_start))
                            elif data_type == Token.FLOAT:
                                tokens.insert(length+2, Token(Token.FLOAT, Number.null, pos_start))
                            elif data_type == Token.BOOL:
                                tokens.insert(length+2, Token(Token.BOOL, Token.FALSE, pos_start))
                            else:
                                tokens.insert(length+2, Token(Token.CHAR, Token.EMPTY, pos_start))
                        else:
                            if data_type != tokens[length+2].type:
                                return [], "VAR " + tokens[length].value
                            data_value = None
                    elif token.type in Token.DATA_TYPES:
                        data_value = token.value
                    length -= 1
        return tokens, None

    def make_equals(self):
        token_type = Token.EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            token_type = Token.EE

        return Token(token_type, pos_start=pos_start)

    def make_less_than_or_not_equals(self):
        token_type = Token.LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            token_type = Token.LTE
        elif self.current_char == '>':
            self.advance()
            token_type = Token.NE

        return Token(token_type, pos_start=pos_start)

    def make_greater_than(self):
        token_type = Token.GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            token_type = Token.GTE

        return Token(token_type, pos_start=pos_start)

    def skip_comment(self):
        pos_start = self.pos.copy()

        self.advance()

        while self.current_char != ';':
            self.advance()

        self.advance()

        return Token(Token.COMMENT, pos_start=pos_start)