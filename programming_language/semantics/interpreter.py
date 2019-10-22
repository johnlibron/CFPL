from programming_language.error_handler.error import RuntimeError
from programming_language.lexical.token import Token
from programming_language.semantics.list import List
from programming_language.semantics.number import Number
from programming_language.semantics.string import String
from programming_language.semantics.runtime_result import RuntimeResult

class Interpreter:

    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node, context):
        return RuntimeResult().success(Number(node.token.value).set_context(context).set_pos(node.pos_start))

    def visit_StringNode(self, node, context):
        return RuntimeResult().success(String(node.token.value).set_context(context).set_pos(node.pos_start))

    def visit_BoolNode(self, node, context):
        return RuntimeResult().success(String(node.token.value).set_context(context).set_pos(node.pos_start))

    def visit_ListNode(self, node, context):
        result = RuntimeResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(result.register(self.visit(element_node, context)))
            if result.error: return result

        return result.success(List(elements).set_context(context).set_pos(node.pos_start))

    def visit_VarAccessNode(self, node, context):
        result = RuntimeResult()
        var_name = node.var_name_token.value
        value = context.symbol_table.get(var_name)

        if not value:
            return result.failure(RuntimeError(
                node.pos_start,
                f"'{var_name}' is not defined",
                context
            ))

        value = value.copy().set_pos(node.pos_start).set_context(context)
        return result.success(value)

    def visit_VarAssignNode(self, node, context):
        result = RuntimeResult()
        var_name = node.var_name_token.value
        value = result.register(self.visit(node.value_node, context))
        if result.error: return result

        context.symbol_table.set(var_name, value)
        return result.success(value)

    def visit_BinaryOperatorNode(self, node, context):
        result = RuntimeResult()
        left = result.register(self.visit(node.left_node, context))
        if result.error: return result
        right = result.register(self.visit(node.right_node, context))
        if result.error: return result

        error = None

        if node.operator_token.type == Token.PLUS:
            answer, error = left.add(right)
        elif node.operator_token.type == Token.MINUS:
            answer, error = left.subtract(right)
        elif node.operator_token.type == Token.MUL:
            answer, error = left.multiply(right)
        elif node.operator_token.type == Token.DIV:
            answer, error = left.divide(right)
        elif node.operator_token.type == Token.MOD:
            answer, error = left.modulo(right)
        elif node.operator_token.type == Token.CONCAT:
            answer, error = left.concat(right)
        elif node.operator_token.type == Token.EE:
            answer, error = left.get_comparison_eq(right)
        elif node.operator_token.type == Token.NE:
            answer, error = left.get_comparison_ne(right)
        elif node.operator_token.type == Token.LT:
            answer, error = left.get_comparison_lt(right)
        elif node.operator_token.type == Token.GT:
            answer, error = left.get_comparison_gt(right)
        elif node.operator_token.type == Token.LTE:
            answer, error = left.get_comparison_lte(right)
        elif node.operator_token.type == Token.GTE:
            answer, error = left.get_comparison_gte(right)
        elif node.operator_token.matches(Token.KEYWORD, Token.AND):
            answer, error = left.get_comparison_and(right)
        elif node.operator_token.matches(Token.KEYWORD, Token.OR):
            answer, error = left.get_comparison_or(right)

        if error:
            return result.failure(error)
        else:
            return result.success(answer.set_pos(node.pos_start))

    def visit_UnaryOperatorNode(self, node, context):
        result = RuntimeResult()
        number = result.register(self.visit(node.node, context))
        if result.error: return result

        error = None

        if node.operator_token.type == Token.MINUS:
            number, error = number.multiply(Number(-1))
        elif node.operator_token.matches(Token.KEYWORD, Token.NOT):
            answer, error = number.logical_not()

        if error:
            return result.failure(error)
        else:
            return result.success(number.set_pos(node.pos_start))

    def visit_IfNode(self, node, context):
        result = RuntimeResult()

        for condition, expr in node.cases:
            condition_value = result.register(self.visit(condition, context))
            if result.error: return result
            
            if condition_value.is_true():
                expr_value = result.register(self.visit(expr, context))
                if result.error: return result
                return result.success(expr_value)

        if node.else_case:
            expr = node.else_case
            expr_value = result.register(self.visit(expr, context))
            if result.error: return result
            return result.success(expr_value)

        return result.success(Number.null)

    def visit_WhileNode(self, node, context):
        result = RuntimeResult()
        elements = []

        while True:
            condition = result.register(self.visit(node.condition_node, context))
            if result.error: return result

            if not condition.is_true(): break
            
            elements.append(result.register(self.visit(node.body_node, context)))
            if result.error: return result

        return result.success(
            List(elements).set_context(context).set_pos(node.pos_start)
        )
