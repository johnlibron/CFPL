
from django.shortcuts import render

from programming_language.lexical.lexer import Lexer
from programming_language.lexical.token import Token
from programming_language.syntax.parser import Parser
from programming_language.syntax.symbol_table import SymbolTable
from programming_language.semantics.context import Context
from programming_language.semantics.interpreter import Interpreter
from programming_language.semantics.number import Number

global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number.null)
global_symbol_table.set("FALSE", Number.false)
global_symbol_table.set("TRUE", Number.true)

def index(request):
    tokens = None
    ast = None
    errors = []
    output = None

    if request.POST:
        # Generate tokens
        source_code = request.POST['source_code']
        if source_code.strip() != "":
            # replace newlines
            lexemes = source_code.replace('\r\n', ';')
            lexer = Lexer(lexemes)
            tokens, error = lexer.make_tokens()

            if error:
                errors.append(error.message())
            else:
                # Generate AST
                parser = Parser(tokens)
                ast = parser.parse()
                if ast.error:
                    errors.append(ast.error.message())
                else:
                    interpreter = Interpreter()
                    context = Context('<program>')
                    context.symbol_table = global_symbol_table
                    output = interpreter.visit(ast.node, context)
                    if output.error:
                        errors.append(output.error.message())
            
    ctx = {
        'tokens': tokens,
        'ast': ast,
        'errors': errors,
        'output': output
    }
    return render(request, 'index.html', ctx)