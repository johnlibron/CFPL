from programming_language.error_handler.error import InvalidSyntaxError
from programming_language.lexical.token import Token
from programming_language.syntax.nodes import BinaryOperatorNode
from programming_language.syntax.nodes import BoolNode
from programming_language.syntax.nodes import IfNode
from programming_language.syntax.nodes import ListNode
from programming_language.syntax.nodes import NumberNode
from programming_language.syntax.nodes import StringNode
from programming_language.syntax.nodes import UnaryOperatorNode
from programming_language.syntax.nodes import VarAccessNode
from programming_language.syntax.nodes import VarAssignNode
from programming_language.syntax.nodes import WhileNode
from programming_language.syntax.parse_result import ParseResult

class Parser:

    def __init__(self, tokens, input_tokens):
        self.tokens = tokens
        # TODO update tokens in view with the input tokens
        self.input_tokens = input_tokens
        self.token_index = -1
        self.input_token_index = -1
        self.advance()
        self.input_advance()

    def advance(self, ):
        self.token_index += 1
        if self.token_index >= 0 and self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def input_advance(self, ):
        self.input_token_index += 1
        if self.input_token_index >= 0 and self.input_token_index < len(self.input_tokens):
            self.current_input_token = self.input_tokens[self.input_token_index]
        return self.current_input_token

    def parse(self):
        result = self.statements()
        if not result.error and self.current_token.type != Token.EOL:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Invalid statement"
            ))
        return result

    def statements(self):
        result = ParseResult()
        statements = []
        pos_start = self.current_token.pos_start.copy()

        while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
            result.register_advancement()
            self.advance()

        if not self.current_token.matches(Token.KEYWORD, Token.START):
            statement = result.register(self.var_statement())
            if result.error: return result
            statements.extend(statement)

            more_var_statements = True

            while True:
                newline_count = 0
                while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
                    result.register_advancement()
                    self.advance()
                    newline_count += 1
                if newline_count == 0:
                    more_var_statements = False

                if not more_var_statements or self.current_token.matches(Token.KEYWORD, Token.START): break
                statement = result.register(self.var_statement())
                if result.error: return result
                statements.extend(statement)

        if self.current_token.type == Token.EOL:
            return result.success(ListNode(statements, pos_start))
            
        pos_start = self.current_token.pos_start.copy()

        if not self.current_token.matches(Token.KEYWORD, Token.START):
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'START'"
            ))
        
        result.register_advancement()
        self.advance()

        if self.current_token.type != Token.NEWLINE:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'NEWLINE'"
            ))

        result.register_advancement()
        self.advance()

        while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
            result.register_advancement()
            self.advance()
        
        if not self.current_token.matches(Token.KEYWORD, Token.OUTPUT):
            statement = result.register(self.statement())
            if result.error: return result
            statements.append(statement)

        more_statements = True

        while True:
            newline_count = 0
            while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
                result.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False

            # evaluate the output variables with its data types
            if self.current_token.matches(Token.KEYWORD, Token.OUTPUT):
                var_name = self.current_token
                result.register_advancement()
                self.advance()

                if self.current_token.type != Token.COLON:
                    return result.failure(InvalidSyntaxError(
                        self.current_token.pos_start,
                        "Expected 'COLON'"
                    ))

                result.register_advancement()
                self.advance()

                output = result.register(self.expr())
                if result.error:
                    return result.failure(InvalidSyntaxError(
                        self.current_token.pos_start,
                        "Invalid output statement"
                    ))

                statements.append(VarAssignNode(var_name, output))

                if self.current_token.type != Token.NEWLINE:
                    return result.failure(InvalidSyntaxError(
                        self.current_token.pos_start,
                        "Expected 'NEWLINE'"
                    ))

                result.register_advancement()
                self.advance()

            if self.current_token.type == Token.EOL:
                return result.failure(InvalidSyntaxError(
                    self.current_token.pos_start,
                    "Expected 'STOP'"
                ))

            if not more_statements or self.current_token.matches(Token.KEYWORD, Token.STOP): break
            statement = result.register(self.statement())
            if result.error: return result
            statements.append(statement)

        if not self.current_token.matches(Token.KEYWORD, Token.STOP):
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'STOP'"
            ))
        
        result.register_advancement()
        self.advance()

        while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
            result.register_advancement()
            self.advance()
            if self.current_token.type == Token.EOL: break
        
        return result.success(ListNode(statements, pos_start))

    def var_statement(self):
        result = ParseResult()
        variables = []

        while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
            result.register_advancement()
            self.advance()

        if not self.current_token.matches(Token.KEYWORD, Token.VAR):
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'VAR'"
            ))

        result.register_advancement()
        self.advance()

        while True:
            var_assign = result.register(self.var_assign())
            if result.error: return result
            variables.append(var_assign)

            if self.current_token.type == Token.COMMA:
                result.register_advancement()
                self.advance()
            else:
                if not self.current_token.matches(Token.KEYWORD, Token.AS):
                    return result.failure(InvalidSyntaxError(
                        self.current_token.pos_start,
                        "Expected 'AS'"
                    ))

                result.register_advancement()
                self.advance()

                if self.current_token.type != Token.DATA_TYPE:
                    return result.failure(InvalidSyntaxError(
                        self.current_token.pos_start,
                        "Invalid 'DATA_TYPE'"
                    ))

                result.register_advancement()
                self.advance()

                return result.success(variables)

        return result.failure(InvalidSyntaxError(
            self.current_token.pos_start,
            "Expected 'VAR', int, float, char, bool, identifier, 'AS', 'DATA_TYPE'"
        ))
    
    def var_assign(self):
        result = ParseResult()

        if self.current_token.type != Token.IDENTIFIER:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                'Expected identifier'
            ))

        var_name = self.current_token
        result.register_advancement()
        self.advance()

        if self.current_token.type != Token.EQ:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected '='"
            ))

        result.register_advancement()
        self.advance()

        var_value = result.register(self.var_value())
        if result.error: return result

        if self.current_input_token.type == Token.COMMA and self.current_input_token != Token.EOL:
            self.input_advance()

        return result.success(VarAssignNode(var_name, var_value))

    def var_value(self):
        result = ParseResult()
        token = self.current_token
        if self.current_input_token.type in (Token.INT, Token.FLOAT, Token.CHAR, Token.BOOL) and self.current_input_token != Token.EOL:
            token = self.current_input_token
            self.input_advance()

        if token.type in (Token.INT, Token.FLOAT):
            result.register_advancement()
            self.advance()
            return result.success(NumberNode(token))
        elif token.type == Token.CHAR:
            result.register_advancement()
            self.advance()
            return result.success(StringNode(token))
        elif token.type == Token.BOOL:
            result.register_advancement()
            self.advance()
            return result.success(BoolNode(token))
        elif token.type == Token.IDENTIFIER:
            result.register_advancement()
            self.advance()
            return result.success(VarAccessNode(token))
        else:
            return result.failure(InvalidSyntaxError(
                token.pos_start,
                "Expected int, float, char, bool, or identifier"
            ))

    def statement(self):
        result = ParseResult()
        
        while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
            result.register_advancement()
            self.advance()
        
        if self.current_token.value in Token.KEYWORDS:
            expr = result.register(self.expr())
            if result.error:
                print(result.error.details)
                return result.failure(InvalidSyntaxError(
                    self.current_token.pos_start,
                    "Invalid expr"
                ))

            return result.success(expr)

        if self.current_token.type != Token.IDENTIFIER:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected identifier"
            ))

        var_name = self.current_token
        result.register_advancement()
        self.advance()

        if self.current_token.type != Token.EQ:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected '='"
            ))

        result.register_advancement()
        self.advance()

        expr = result.register(self.expr())
        if result.error:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Invalid statement"
            ))

        return result.success(VarAssignNode(var_name, expr))
    
    def expr(self):
        result = ParseResult()

        if self.current_token.type == Token.IDENTIFIER:
            var_name = self.current_token

        node = result.register(self.binary_operation(self.comp_expr, ((Token.KEYWORD, Token.AND), (Token.KEYWORD, Token.OR))))
        if result.error: return result

        if self.current_token.type == Token.EQ:
            result.register_advancement()
            self.advance()
            
            expr = result.register(self.expr())
            if result.error: return result
            return result.success(VarAssignNode(var_name, expr))

        return result.success(node)

    def comp_expr(self):
        result = ParseResult()

        if self.current_token.matches(Token.KEYWORD, Token.NOT):
            operator_token = self.current_token
            result.register_advancement()
            self.advance()

            node = result.register(self.comp_expr())
            if result.error: return result
            return result.success(UnaryOperatorNode(operator_token, node))

        node = result.register(self.binary_operation(self.arith_expr, (Token.EE, Token.NE, Token.LT, Token.GT, Token.LTE, Token.GTE)))

        if result.error:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected int, float, char, bool, identifier, '+', '-', '(', 'NOT', 'IF', or 'WHILE'"
            ))

        return result.success(node)

    def arith_expr(self):
        return self.binary_operation(self.term, (Token.PLUS, Token.MINUS, Token.CONCAT))

    def term(self):
        return self.binary_operation(self.factor, (Token.MUL, Token.DIV, Token.MOD))

    def factor(self):
        result = ParseResult()
        token = self.current_token

        if token.type in (Token.PLUS, Token.MINUS):
            result.register_advancement()
            self.advance()
            factor = result.register(self.factor())
            if result.error: return result
            return result.success(UnaryOperatorNode(token, factor))
        
        return self.atom()

    def atom(self):
        result = ParseResult()
        token = self.current_token

        if token.type in (Token.INT, Token.FLOAT):
            result.register_advancement()
            self.advance()
            return result.success(NumberNode(token))

        elif token.type in (Token.CHAR, Token.CONCAT):
            result.register_advancement()
            self.advance()
            return result.success(StringNode(token))

        elif token.type == Token.BOOL:
            result.register_advancement()
            self.advance()
            return result.success(BoolNode(token))

        elif token.type == Token.IDENTIFIER:
            result.register_advancement()
            self.advance()
            return result.success(VarAccessNode(token))

        elif token.type == Token.LPAREN:
            result.register_advancement()
            self.advance()

            expr = result.register(self.expr())
            if result.error: return result

            if self.current_token.type != Token.RPAREN:
                return result.failure(InvalidSyntaxError(
                    self.current_token.pos_start,
                    "Expected ')'"
                ))
                
            result.register_advancement()
            self.advance()
            return result.success(expr)
                
        elif token.matches(Token.KEYWORD, Token.IF):
            if_expr = result.register(self.if_expr())
            if result.error: return result
            return result.success(if_expr)

        elif token.matches(Token.KEYWORD, Token.WHILE):
            while_expr = result.register(self.while_expr())
            if result.error: return result
            return result.success(while_expr)

        return result.failure(InvalidSyntaxError(
            token.pos_start,
            "Expected expr"
        ))

    def if_expr(self):
        result = ParseResult()
        all_cases = result.register(self.if_expr_cases(Token.IF))
        if result.error: return result
        cases, else_case = all_cases
        return result.success(IfNode(cases, else_case))

    def if_expr_b(self):
        return self.if_expr_cases(Token.ELIF)

    def if_expr_c(self):
        result = ParseResult()
        else_case = None
        
        if not self.current_token.matches(Token.KEYWORD, Token.ELSE):
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'ELSE'"
            ))

        result.register_advancement()
        self.advance()

        if self.current_token.type != Token.NEWLINE:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'NEWLINE'"
            ))

        result.register_advancement()
        self.advance()

        while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
            result.register_advancement()
            self.advance()

        if not self.current_token.matches(Token.KEYWORD, Token.START):
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'START'"
            ))

        result.register_advancement()
        self.advance()

        if self.current_token.type != Token.NEWLINE:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'NEWLINE'"
            ))

        result.register_advancement()
        self.advance()

        while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
            result.register_advancement()
            self.advance()

        while True:
            statement = result.register(self.statement())
            if result.error: return result
            else_case = statement

            if self.current_token.type != Token.NEWLINE:
                return result.failure(InvalidSyntaxError(
                    self.current_token.pos_start,
                    "Expected 'NEWLINE'"
                ))

            result.register_advancement()
            self.advance()

            while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
                result.register_advancement()
                self.advance()

            if self.current_token.matches(Token.KEYWORD, Token.STOP):
                result.register_advancement()
                self.advance()
                break

        if self.current_token.type != Token.NEWLINE:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'NEWLINE'"
            ))

        result.register_advancement()
        self.advance()

        while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
            result.register_advancement()
            self.advance()

        return result.success(else_case)

    def if_expr_b_or_c(self):
        result = ParseResult()
        cases, else_case = [], None

        if self.current_token.matches(Token.KEYWORD, Token.ELIF):
            all_cases = result.register(self.if_expr_b())
            if result.error: return result
            cases, else_case = all_cases
        elif self.current_token.matches(Token.KEYWORD, Token.ELSE):
            else_case = result.register(self.if_expr_c())
            if result.error: return result

        return result.success((cases, else_case))

    def if_expr_cases(self, case_keyword):
        result = ParseResult()
        cases = []
        else_case = None

        if not self.current_token.matches(Token.KEYWORD, case_keyword):
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                f"Expected '{case_keyword}'"
            ))

        result.register_advancement()
        self.advance()

        condition = result.register(self.expr())
        if result.error: return result

        if self.current_token.type != Token.NEWLINE:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'NEWLINE'"
            ))

        result.register_advancement()
        self.advance()

        while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
            result.register_advancement()
            self.advance()

        if not self.current_token.matches(Token.KEYWORD, Token.START):
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'START'"
            ))

        result.register_advancement()
        self.advance()

        if self.current_token.type != Token.NEWLINE:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'NEWLINE'"
            ))

        result.register_advancement()
        self.advance()

        while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
            result.register_advancement()
            self.advance()

        while True:
            statement = result.register(self.statement())
            if result.error: return result
            cases.append((condition, statement))

            if self.current_token.type != Token.NEWLINE:
                return result.failure(InvalidSyntaxError(
                    self.current_token.pos_start,
                    "Expected 'NEWLINE'"
                ))

            result.register_advancement()
            self.advance()

            while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
                result.register_advancement()
                self.advance()

            if self.current_token.matches(Token.KEYWORD, Token.STOP):
                result.register_advancement()
                self.advance()
                break

        if self.current_token.type != Token.NEWLINE:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'NEWLINE'"
            ))

        result.register_advancement()
        self.advance()

        while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
            result.register_advancement()
            self.advance()

        all_cases = result.register(self.if_expr_b_or_c())
        if result.error: return result
        new_cases, else_case = all_cases
        cases.extend(new_cases)
        
        return result.success((cases, else_case))

    def while_expr(self):
        result = ParseResult()
        
        if not self.current_token.matches(Token.KEYWORD, Token.WHILE):
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'WHILE'"
            ))

        result.register_advancement()
        self.advance()

        condition = result.register(self.expr())
        if result.error: return result

        if self.current_token.type != Token.NEWLINE:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'NEWLINE'"
            ))

        result.register_advancement()
        self.advance()

        while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
            result.register_advancement()
            self.advance()

        if not self.current_token.matches(Token.KEYWORD, Token.START):
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'START'"
            ))

        result.register_advancement()
        self.advance()

        if self.current_token.type != Token.NEWLINE:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'NEWLINE'"
            ))

        result.register_advancement()
        self.advance()

        while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
            result.register_advancement()
            self.advance()

        body = result.register(self.statement())
        if result.error: return result

        if self.current_token.type != Token.NEWLINE:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'NEWLINE'"
            ))

        result.register_advancement()
        self.advance()

        while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
            result.register_advancement()
            self.advance()

        if not self.current_token.matches(Token.KEYWORD, Token.STOP):
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'STOP'"
            ))

        result.register_advancement()
        self.advance()

        if self.current_token.type != Token.NEWLINE:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                "Expected 'NEWLINE'"
            ))

        result.register_advancement()
        self.advance()

        while self.current_token.type == Token.NEWLINE or self.current_token.type == Token.COMMENT:
            result.register_advancement()
            self.advance()
        
        return result.success(WhileNode(condition, body))

    def binary_operation(self, func_a, ops, func_b=None):
        if func_b == None: func_b = func_a

        result = ParseResult()
        left = result.register(func_a())
        if result.error: return result

        while self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops:
            operator_token = self.current_token
            result.register_advancement()
            self.advance()
            
            right = result.register(func_b())
            if result.error: return result
            left = BinaryOperatorNode(left, operator_token, right)
            
        return result.success(left)