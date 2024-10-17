# Global Variables
TokenCounter = 0
SymbolTable = {"Global": {}}
AST = {"Program": {"Global": []}}

def parseProgram(tokens):
    parseFunctions(tokens)
    return AST, SymbolTable

def parseFunctions(tokens):
    while peekNextToken(tokens) is not None:

        typeToken = consumeNextToken(tokens)
        if typeToken['TOKEN'] in ['int', 'float', 'char', 'void']:
            identifierToken = consumeNextToken(tokens)

            if identifierToken['TYPE'] == 'IDENTIFIER':
                peekToken = peekNextToken(tokens)

                if peekToken is not None and peekToken['TOKEN'] != '(':
                    parseGlobalDeclaration(tokens, typeToken['TOKEN'], identifierToken['TOKEN'])
                elif peekToken is not None and peekToken['TOKEN'] == '(':
                    functionName = identifierToken['TOKEN']
                    returnType = typeToken['TOKEN']
                    consumeNextToken(tokens) # Burn '('
                    consumeNextToken(tokens) # Burn ')'
                    consumedToken = consumeNextToken(tokens)

                    if consumedToken['TOKEN'] == '{':
                        addSymbol(functionName, returnType, True)
                        addASTNode( functionName )
                        parseStatements(tokens, functionName)

                else:
                    raise SyntaxError(f"Unexpected token after identifier: {peekToken['TOKEN']}")

            else:
                raise SyntaxError(f"Expected identifier after type, got: {identifierToken['TOKEN']}")

        else:
            raise SyntaxError(f"Expected type, got: {typeToken['TOKEN']}")

def parseGlobalDeclaration(tokens, varType, varName):
    consumedToken = peekNextToken(tokens)

    if consumedToken['TOKEN'] == ';':
        consumeNextToken(tokens) # Burn ';'
        addSymbol(varName, varType, False)

    elif consumedToken['TOKEN'] == '=':
        consumeNextToken(tokens) # Burn '='
        value = parseExpressions(tokens)
        addSymbol(varName, varType, False)

        modifyNode('Global', 'ASSIGN', varName, value)

        if peekNextToken(tokens)['TOKEN'] == ';':
            consumeNextToken(tokens) # Burn ';'

    else:
        raise SyntaxError(f"Expected ';' or '=', got: {consumedToken['TOKEN']}")

def parseStatements(tokens, functionName): # SUPPORTS: DECLARATIONS, ASSIGNMENTS, RETURN STATEMENTS
    while peekNextToken(tokens) is not None and peekNextToken(tokens)['TOKEN'] != '}':
        consumedToken = peekNextToken(tokens)
        
        if consumedToken['TOKEN'] in ['int', 'float', 'char']:
            typeToken = consumeNextToken(tokens)  
            varType = typeToken['TOKEN']
            identifierToken = consumeNextToken(tokens) 
        
            if identifierToken['TYPE'] != 'IDENTIFIER':
                raise SyntaxError(f"Expected identifier, got: {identifierToken['TOKEN']}")
            varName = identifierToken['TOKEN']
            consumedToken = peekNextToken(tokens)
        
            if consumedToken['TOKEN'] == '[':
                consumeNextToken(tokens) # Burn '['
                consumedToken = consumeNextToken(tokens)
                if consumedToken['TOKEN'] != ']':
                    raise SyntaxError(f"Expected ']', got: {consumedToken['TOKEN']}")
                varName += '[]'
            consumedToken = peekNextToken(tokens)
        
            if consumedToken['TOKEN'] == '=':
                consumeNextToken(tokens) # Burn '['
                value = parseExpressions(tokens)
                modifyNode( functionName, 'ASSIGN', varName, value)
            else:
                pass

            modifySymbol(functionName, varName, varType)
        
            if peekNextToken(tokens)['TOKEN'] == ';':
                consumeNextToken(tokens)
            else:
                raise SyntaxError(f"Expected ';', got: {peekNextToken(tokens)['TOKEN']}")
        
        elif consumedToken['TOKEN'] == 'return':
            consumeNextToken(tokens)  # Burn 'return'
            value = parseExpressions(tokens)
            modifyNode( functionName, 'RETURN', None, value)
        
            if peekNextToken(tokens)['TOKEN'] == ';':
                consumeNextToken(tokens) # Burn ';'
        
            else:
                raise SyntaxError(f"Expected ';', got: {peekNextToken(tokens)['TOKEN']}")
        
        elif consumedToken['TYPE'] == 'IDENTIFIER':
            identifierToken = consumeNextToken(tokens) 
            varName = identifierToken['TOKEN']
            consumedToken = peekNextToken(tokens)
        
            if consumedToken['TOKEN'] == '=':
                consumeNextToken(tokens) # Burn '='
                value = parseExpressions(tokens)
                modifyNode( functionName, 'ASSIGN', varName, value)
        
                if peekNextToken(tokens)['TOKEN'] == ';':
                    consumeNextToken(tokens) # Burn ';'
        
                else:
                    raise SyntaxError(f"Expected ';', got: {peekNextToken(tokens)['TOKEN']}")
        
            else:
                consumeNextToken(tokens) # Burn ';'
        
        else:
            consumeNextToken(tokens) # Burn token
    
    if peekNextToken(tokens) is not None and peekNextToken(tokens)['TOKEN'] == '}':
        consumeNextToken(tokens) # Burn '}'
    
    else:
        raise SyntaxError(f"Expected closing braces, got: {peekNextToken(tokens)['TOKEN']}")

# Expr -> Term | Expr + Term | Expr - Term
def parseExpressions(tokens):

    # Term
    expr = parseTerm(tokens)

    # Expr + Term | Expr - Term
    while peekNextToken(tokens) is not None and peekNextToken(tokens)['TOKEN'] in ['+', '-']:
        opToken = consumeNextToken(tokens)
        term = parseTerm(tokens)
        expr = [expr, opToken['TOKEN'], term]

    return expr

# Term -> Value | Term * Value | Term / Value
def parseTerm(tokens):

    # Value
    term = parseValue(tokens)

    # Term * Value | Term / Value
    while peekNextToken(tokens) is not None and peekNextToken(tokens)['TOKEN'] in ['*', '/']:
        opToken = consumeNextToken(tokens)
        value = parseValue(tokens)
        term = [term, opToken['TOKEN'], value]

    return term

# Val -> (Expr) | Constant | ID | - Val
def parseValue(tokens):
    consumedToken = consumeNextToken(tokens)

    # (Expr)
    if consumedToken['TOKEN'] == '(':
        expr = parseExpressions(tokens)
        if peekNextToken(tokens)['TOKEN'] == ')':
            consumeNextToken(tokens)
            return expr
        else:
            raise SyntaxError(f"Expected ')', got: {peekNextToken(tokens)['TOKEN']}")

    # Constant
    elif consumedToken['TYPE'] in ['INTEGER_CONSTANT', 'FLOATING_CONSTANT', 'STRING_CONSTANT', 'CHAR_CONSTANT']:
        return consumedToken['TOKEN']

    # ID
    elif consumedToken['TYPE'] == 'IDENTIFIER':
        return consumedToken['TOKEN']

    # - Value
    elif consumedToken['TOKEN'] == '-':
        value = parseValue(tokens)
        return ['-', value]

    else:
        raise SyntaxError(f"Unexpected token: {consumedToken['TOKEN']}")

def consumeNextToken(tokens):
    global TokenCounter
    
    if TokenCounter in tokens:
        consumedToken = tokens[TokenCounter]
        TokenCounter += 1
        return consumedToken
    
    else:
        return None

def peekNextToken(tokens):
    if TokenCounter in tokens:
        return tokens[TokenCounter]
    else:
        return None

def addSymbol(storedIdentifier, typeDeclaration, isFunc, params=None, variables=None):
    if not isFunc:
        SymbolTable['Global'][storedIdentifier] = typeDeclaration
    else:
        SymbolTable['Global'][storedIdentifier] = {'retType': typeDeclaration, "args": params, "vars": {}}

def modifySymbol( functionName, varName, varType):
    SymbolTable['Global'][functionName]['vars'][varName] = varType

        
def addASTNode( functionName ):
    AST['Program'][functionName] = []
    
def modifyNode( functionName, TYPE, varName, value):
    if TYPE == 'RETURN':
        AST['Program'][functionName].append([TYPE, value])
    else:
        AST['Program'][functionName].append([TYPE, varName, value])