class NumberNode:
    
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start

    def __repr__(self):
        return f'{self.token}'

class StringNode:
    
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start

    def __repr__(self):
        return f'{self.token}'

class BoolNode:
    
    def __init__(self, token):
        self.token = token

        self.pos_start = self.token.pos_start

    def __repr__(self):
        return f'{self.token}'

class ListNode:

    def __init__(self, element_nodes, pos_start):
        self.element_nodes = element_nodes

        self.pos_start = pos_start

class VarAccessNode:

    def __init__(self, var_name_token):
        self.var_name_token = var_name_token

        self.pos_start = self.var_name_token.pos_start

class VarAssignNode:

    def __init__(self, var_name_token, value_node):
        self.var_name_token = var_name_token
        self.value_node = value_node

        self.pos_start = self.var_name_token.pos_start

class BinaryOperatorNode:

    def __init__(self, left_node, operator_token, right_node):
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
    
    def __repr__(self):
        return f'({self.left_node}, {self.operator_token}, {self.right_node})'

class UnaryOperatorNode:

    def __init__(self, operator_token, node):
        self.operator_token = operator_token
        self.node = node

        self.pos_start = self.operator_token.pos_start
    
    def __repr__(self):
        return f'({self.operator_token}, {self.node})'

class IfNode:

    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start

class WhileNode:

    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node

        self.pos_start = self.condition_node.pos_start