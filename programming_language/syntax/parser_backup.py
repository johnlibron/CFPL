from programming_language.error_handler.error import InvalidSyntaxError
from programming_language.lexical.token import Token
from programming_language.syntax.nodes import BinaryOperatorNode
from programming_language.syntax.nodes import BoolNode
from programming_language.syntax.nodes import CallNode
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

    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()

    def advance(self, ):
        self.token_index += 1
        self.update_current_token()
        return self.current_token

    def reverse(self, amount=1):
        self.token_index -= amount
        self.update_current_token()
        return self.current_token
    
    def update_current_token(self):
        if self.token_index >= 0 and self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]

    def parse(self):
        result = self.statements()
        if not result.error and self.current_token.type != Token.EOL:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                f"Token cannot appear after previous tokens"
            ))
        return result

    # statements : NEWLINE* statement (NEWLINE+ statement)* NEWLINE*
    def statements(self):
        result = ParseResult()
        statements = []
        pos_start = self.current_token.pos_start.copy()

        while self.current_token == Token.NEWLINE:
            result.register_advancement()
            self.advance()

        statement = result.register(self.statement())
        if result.error: return result
        statements.append(statement)

        more_statements = True

        while True:
            newline_count = 0
            while self.current_token.type == Token.NEWLINE:
                result.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False

            if not more_statements: break
            statement = result.try_register(self.statement())
            if not statement:
                self.reverse(result.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return result.success(ListNode(statements, pos_start))

    # statement : expr
    def statement(self):
        result = ParseResult()
        pos_start = self.current_token.pos_start.copy()

        expr = result.register(self.expr())

        if result.error:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                f"Expected 'VAR', 'IF', 'WHILE', int, float, char, bool, identifier, '+', '-', '(', '[' or 'NOT'"
            ))

        return result.success(expr)
    
    # expr : KEYWORD:VAR IDENTIFIER EQUAL expr
    #      : comp-expr ((KEYWORD:AND|KEYWORD:OR) comp-expr)*
    def expr(self):
        result = ParseResult()

        if self.current_token.matches(Token.KEYWORD, Token.VAR):
            result.register_advancement()
            self.advance()

            if self.current_token.type != Token.IDENTIFIER:
                return result.failure(InvalidSyntaxError(
                    self.current_token.pos_start,
                    f'Expected identifier'
                ))

            var_name = self.current_token
            result.register_advancement()
            self.advance()

            if self.current_token.type != Token.EQ:
                return result.failure(InvalidSyntaxError(
                    self.current_token.pos_start,
                    f"Expected '='"
                ))

            result.register_advancement()
            self.advance()

            expr = result.register(self.expr())
            if result.error: return result
            return result.success(VarAssignNode(var_name, expr))

        node = result.register(self.binary_operation(self.comp_expr, ((Token.KEYWORD, Token.AND), (Token.KEYWORD, Token.OR))))

        if result.error:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                f"Expected 'VAR', 'IF', 'WHILE', int, float, char, bool, identifier, '+', '-', '(', '[', or 'NOT'"
            ))

        return result.success(node)

    # comp-expr : KEYWORD:NOT comp-expr
    #           : arith-expr ((EE|NE|LT|GT|LTE|GTE) arith-expr)*
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
                f"Expected int, float, identifier, '+', '-', '(', '[', 'IF', 'FOR', 'WHILE', or 'NOT'"
            ))

        return result.success(node)

    # arith-expr : term ((PLUS|MINUS) term)*
    def arith_expr(self):
        return self.binary_operation(self.term, (Token.PLUS, Token.MINUS))

    # term : factor ((MUL|DIV|MOD) factor)*
    def term(self):
        return self.binary_operation(self.factor, (Token.MUL, Token.DIV, Token.MOD))

    # factor : (PLUS|MINUS) factor
    #        : call
    def factor(self):
        result = ParseResult()
        token = self.current_token

        if token.type in (Token.PLUS, Token.MINUS):
            result.register_advancement()
            self.advance()
            factor = result.register(self.factor())
            if result.error: return result
            return result.success(UnaryOperatorNode(token, factor))
        
        return self.call()

    # call : atom (LPAREN (expr (COMMA expr)*)? RPAREN)?
    def call(self):
        result = ParseResult()
        atom = result.register(self.atom())
        if result.error: return result

        if self.current_token.type == Token.LPAREN:
            result.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current_token.type == Token.RPAREN:
                result.register_advancement()
                self.advance()
            else:
                arg_nodes.append(result.register(self.expr()))
                if result.error:
                    return result.failure(InvalidSyntaxError(
                        self.current_token.pos_start,
                        f"Expected ')', 'VAR', 'IF', 'FOR', 'WHILE', int, float, identifier, '+', '-', '(', '[', or 'NOT'"
                    ))
                
                while self.current_token.type == Token.COMMA:
                    result.register_advancement()
                    self.advance()

                    arg_nodes.append(result.register(self.expr()))
                    if result.error: return result
                
                if self.current_token.type != Token.RPAREN:
                    return result.failure(InvalidSyntaxError(
                        self.current_token.pos_start,
                        f"Expected ',' or ')'"
                    ))
                    
                result.register_advancement()
                self.advance()

            return result.success(CallNode(atom, arg_nodes))

        return result.success(atom)

    # atom : INT|FLOAT|CHAR|BOOL|IDENTIFIER
    #      : LPAREN expr RPAREN
    #      : list-expr
    #      : if-expr
    #      : while-expr
    def atom(self):
        result = ParseResult()
        token = self.current_token

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
        elif token.type == Token.LPAREN:
            result.register_advancement()
            self.advance()

            expr = result.register(self.expr())
            if result.error: return result

            if self.current_token.type == Token.RPAREN:
                result.register_advancement()
                self.advance()
                return result.success(expr)
            else:
                return result.failure(InvalidSyntaxError("Expected ')'"))
        elif token.type == Token.LSQUARE:
            list_expr = result.register(self.list_expr())
            if result.error: return result
            return result.success(list_expr)
        elif token.matches(Token.KEYWORD, Token.IF):
            if_expr = result.register(self.if_expr())
            if result.error: return result
            return result.success(if_expr)
        elif token.matches(Token.KEYWORD, Token.WHILE):
            while_expr = result.register(self.while_expr())
            if result.error: return result
            return result.success(while_expr)

        return result.failure(InvalidSyntaxError("Expected int, float, char, bool, identifier, '+', '-', '(', '[', 'IF', 'FOR', 'WHILE'"))

    # list-expr : LSQUARE (expr (COMMA expr)*)? RSQUARE
    def list_expr(self):
        result = ParseResult()
        element_nodes = []
        pos_start = self.current_token.pos_start.copy()

        if self.current_token.type != Token.LSQUARE:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                f"Expected '['"
            ))

        result.register_advancement()
        self.advance()

        if self.current_token.type == Token.RSQUARE:
            result.register_advancement()
            self.advance()
        else:
            element_nodes.append(result.register(self.expr()))
            if result.error:
                return result.failure(InvalidSyntaxError(
                    self.current_token.pos_start,
                    f"Expected ']', 'VAR', 'IF', 'WHILE', int, float, identifier, '+', '-', '(', '[', or 'NOT'"
                ))
            
            while self.current_token.type == Token.COMMA:
                result.register_advancement()
                self.advance()

                element_nodes.append(result.register(self.expr()))
                if result.error: return result
            
            if self.current_token.type != Token.RSQUARE:
                return result.failure(InvalidSyntaxError(
                    self.current_token.pos_start,
                    f"Expected ',' or ']'"
                ))
                
            result.register_advancement()
            self.advance()
        
        return result.success(ListNode(element_nodes, pos_start))

    # if-expr : KEYWORD:IF expr KEYWORD:THEN
    #           (expr if-expr-b|if-expr-c?)
    #         | (NEWLINE statements KEYWORD:END|if-expr-b|if-expr-c)
    def if_expr(self):
        result = ParseResult()
        all_cases = result.register(self.if_expr_cases(Token.IF))
        if result.error: return result
        cases, else_case = all_cases
        return result.success(IfNode(cases, else_case))

    # if-expr : KEYWORD:ELIF expr KEYWORD:THEN
    #           (expr if-expr-b|if-expr-c?)
    #         | (NEWLINE statements KEYWORD:END|if-expr-b|if-expr-c)
    def if_expr_b(self):
        return self.if_expr_cases(Token.ELIF)

    # if-expr : KEYWORD:ELSE
    #           expr
    #         | (NEWLINE statements KEYWORD:END)
    def if_expr_c(self):
        result = ParseResult()
        else_case = None
        
        if self.current_token.matches(Token.KEYWORD, Token.ELSE):
            result.register_advancement()
            self.advance()

            if self.current_token.type == Token.NEWLINE:
                result.register_advancement()
                self.advance()

                statements = result.register(self.statements())
                if result.error: return result
                else_case = (statements, True)

                if self.current_token.matches(Token.KEYWORD, Token.END):
                    result.register_advancement()
                    self.advance()
                else:
                    result.failure(InvalidSyntaxError(
                        self.current_token.pos_start,
                        f"Expected 'END'"
                    ))
            else:
                expr = result.register(self.expr())
                if result.error: return result
                else_case = (expr, False)

        return result.success(else_case)

    def if_expr_b_or_c(self):
        result = ParseResult()
        cases, else_case = [], None

        if self.current_token.matches(Token.KEYWORD, Token.ELIF):
            all_cases = result.register(self.if_expr_b())
            if result.error: return result
            cases, else_case = all_cases
        else:
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
        
        if not self.current_token.matches(Token.KEYWORD, Token.THEN):
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                f"Expected 'THEN'"
            ))

        result.register_advancement()
        self.advance()

        if self.current_token.type == Token.NEWLINE:
            result.register_advancement()
            self.advance()

            statements = result.register(self.statements())
            if result.error: return result
            cases.append((condition, statements, True))

            if self.current_token.matches(Token.KEYWORD, Token.END):
                result.register_advancement()
                self.advance()
            else:
                all_cases = result.register(self.if_expr_b_or_c())
                if result.error: return result
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = result.register(self.expr())
            if result.error: return result
            cases.append((condition, expr, False))

            all_cases = result.register(self.if_expr_b_or_c())
            if result.error: return result
            new_cases, else_case = all_cases
            cases.extend(new_cases)
        
        return result.success((cases, else_case))

    # while-expr : KEYWORD:WHILE expr KEYWORD:THEN
    #              expr
    #            | (NEWLINE statements KEYWORD:END)
    def while_expr(self):
        result = ParseResult()
        
        if not self.current_token.matches(Token.KEYWORD, Token.WHILE):
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                f"Expected 'WHILE'"
            ))

        result.register_advancement()
        self.advance()

        condition = result.register(self.expr())
        if result.error: return result

        if not self.current_token.matches(Token.KEYWORD, Token.THEN):
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                f"Expected 'THEN'"
            ))

        result.register_advancement()
        self.advance()
        
        if self.current_token.type == Token.NEWLINE:
            result.register_advancement()
            self.advance()

            body = result.register(self.statements())
            if result.error: return result

            if not self.current_token.matches(Token.KEYWORD, Token.END):
                result.failure(InvalidSyntaxError(
                    self.current_token.pos_start,
                    f"Expected 'END'"
                ))

            result.register_advancement()
            self.advance()
            
            return result.success(WhileNode(condition, body, True))

        body = result.register(self.expr())
        if result.error: return result

        return result.success(WhileNode(condition, body, False))

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