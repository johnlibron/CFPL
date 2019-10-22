
from django.shortcuts import render

from programming_language.lexical.lexer import Lexer
from programming_language.lexical.token import Token
from programming_language.syntax.parser import Parser
from programming_language.syntax.symbol_table import SymbolTable
from programming_language.semantics.context import Context
from programming_language.semantics.interpreter import Interpreter
from programming_language.semantics.number import Number

def index(request):
    tokens = None
    ast = None
    errors = []
    output = None

    if request.POST:
        source_code = request.POST['source_code']
        if source_code.strip():
            # replace newlines
            lexemes = source_code.replace('\r\n', ';')
            # Generate tokens
            lexer = Lexer(lexemes)
            tokens, error = lexer.make_tokens()

            if error:
                errors.append(error.message())
            else:
                inputs = request.POST.get('inputs', False)
                # Generate input tokens
                lexer = Lexer(inputs)
                input_tokens, input_error = lexer.make_tokens()

                if input_error:
                    errors.append(input_error.message())
                else:
                    # Generate AST
                    parser = Parser(tokens, input_tokens)
                    ast = parser.parse()
                    if ast.error:
                        errors.append(ast.error.message())
                    else:
                        interpreter = Interpreter()
                        context = Context('<program>')
                        context.symbol_table = SymbolTable()
                        context.symbol_table.set("NULL", Number.null)
                        context.symbol_table.set("FALSE", Number.false)
                        context.symbol_table.set("TRUE", Number.true)
                        result = interpreter.visit(ast.node, context)
                        if result.error:
                            errors.append(result.error.message())
                        else:
                            output = context.symbol_table.get(ast.output)
            
    ctx = {
        'tokens': tokens,
        'ast': ast,
        'errors': errors,
        'output': output
    }
    return render(request, 'index.html', ctx)