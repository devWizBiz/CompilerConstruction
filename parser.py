# External Libraries
import pdb

# Internal Libraries
import support

SymbolTable = {"Global": {}}
AST = {"Program": {}}

def parserProgram(tokens):
    parseFunctions(tokens, 0)
    return AST, SymbolTable

def parseFunctions(tokens, tokenCount):
    consumedToken = tokens[tokenCount]
    
    tokenCount += 1  # Increment the counter after reading the token

    if consumedToken['TOKEN'] in ['void', 'char', 'int', 'float']:  # For now, support just 'int'
        typeDeclaration = consumedToken['TOKEN']
        consumedToken = tokens[tokenCount]
        tokenCount += 1
        
        if consumedToken['TYPE'] == 'IDENTIFIER':
            storedIdentifier = consumedToken['TOKEN']
            consumedToken = tokens[tokenCount]
            tokenCount += 1

            if consumedToken['TOKEN'] == '(': # args not supported as of now
                params = None
                consumedToken = tokens[tokenCount]
                tokenCount += 1

                if consumedToken['TOKEN'] == ')':
                    consumedToken = tokens[tokenCount]
                    tokenCount += 1

                    if consumedToken['TOKEN'] == '{':
                        closingBraceIndex = lookAhead(tokenCount, tokens, '}')  # Look ahead for closing brace
                        
                        if closingBraceIndex != -1:
                            statements = []
                            SymbolTable['Global'][storedIdentifier] = {'retType':typeDeclaration, "args":params, "vars":{}}
                            AST['Program'][storedIdentifier] =  statements
                            parseStatements(tokenCount, tokens, typeDeclaration, storedIdentifier, statements)
                            if closingBraceIndex < len(tokens) - 1:
                                return parseFunctions(tokens, closingBraceIndex + 1)  # Continue parsing into more functions after closing brace
                        else:
                            support.error('Expected closing "}" but not found.')

            elif consumedToken['TOKEN'] == ';':  # Global variable declaration
                SymbolTable['Global'][storedIdentifier] = typeDeclaration
                return parseFunctions(tokens, tokenCount)  # Continue parsing after declaration # ERROR CHECKING

            else:
                support.error(f'Expected "(" or ";", instead received "{consumedToken["TOKEN"]}"')

        else:
            support.error(f'Expected an IDENTIFIER, instead received "{consumedToken["TOKEN"]}"')

    else:
        support.error(f'Expected "void", "char", "int", "float", instead received "{consumedToken["TOKEN"]}"')

def parseStatements(tokenCount, tokens, functionDeclaration, functionIdentifier, statements):
    consumedToken = tokens[tokenCount]
    tokenCount += 1
    
    if consumedToken['TOKEN'] == '}':
        return statements
    
    if consumedToken['TOKEN'] in ['int', 'char', 'float']: # Variable Declaration / Assignment
        typeDeclaration = consumedToken['TOKEN']
        consumedToken = tokens[tokenCount]
        tokenCount += 1
        
        if consumedToken['TYPE'] == 'IDENTIFIER':
            storedIdentifier = consumedToken['TOKEN']
            consumedToken = tokens[tokenCount]
            
            tokenCount += 1
            
            if consumedToken['TOKEN'] == ';':
                SymbolTable['Global'][functionIdentifier]["vars"].update({storedIdentifier: typeDeclaration})
                return parseStatements(tokenCount, tokens, functionDeclaration, functionIdentifier, statements)
            
            elif consumedToken['TOKEN'] == '[':
                consumedToken = tokens[tokenCount]
                tokenCount += 1
                
                if consumedToken['TOKEN'] == ']':
                    SymbolTable['Global'][functionIdentifier]["vars"].update({storedIdentifier+"[]": typeDeclaration})
                    consumedToken = tokens[tokenCount]
                    tokenCount += 1
                    
                    if consumedToken['TOKEN'] == '=': # Assign
                        consumedToken = tokens[tokenCount]
                        tokenCount += 1
                        
                        if consumedToken['TYPE'] in ['STRING_CONSTANT', 'CHAR_CONSTANT']:
                            statements.append(["ASSIGN", storedIdentifier+"[]", consumedToken['TOKEN']])
                            consumedToken = tokens[tokenCount]
                            tokenCount += 1
                        
                        if consumedToken['TOKEN'] == ';':
                            return parseStatements(tokenCount, tokens, functionDeclaration, functionIdentifier, statements)
            
            elif consumedToken['TOKEN'] == '=':
                SymbolTable['Global'][functionIdentifier]["vars"].update({storedIdentifier: typeDeclaration})
                consumedToken = tokens[tokenCount]
                tokenCount += 1

                expression = []
                expression.append(consumedToken['TOKEN'])

                if consumedToken['TYPE'] == 'INTEGER_CONSTANT' and typeDeclaration == 'int':
                    statements.append(["ASSIGN", storedIdentifier, consumedToken['TOKEN']])
                    consumedToken = tokens[tokenCount]
                    tokenCount += 1
                
                elif consumedToken['TYPE'] == 'FLOATING_CONSTANT' and typeDeclaration == 'float':
                    statements.append(["ASSIGN", storedIdentifier, consumedToken['TOKEN']])
                    consumedToken = tokens[tokenCount]
                    tokenCount += 1
                    
                elif consumedToken['TYPE'] in ['CHAR_CONSTANT', 'STRING_CONSTANT'] and typeDeclaration == 'char':
                    statements.append(["ASSIGN", storedIdentifier, consumedToken['TOKEN']])
                    consumedToken = tokens[tokenCount]
                    tokenCount += 1

                elif consumedToken['TYPE'] == 'IDENTIFIER': # TODO: Check if the identifier is declared
                    statements.append(["ASSIGN", storedIdentifier, consumedToken['TOKEN']])
                    consumedToken = tokens[tokenCount]
                    tokenCount += 1
            
                else:
                    support.error(f'Expected "{typeDeclaration}", instead received "{consumedToken["TOKEN"]}"')
                    
                if consumedToken['TOKEN'] in ['+', '-', '*', '/'] and typeDeclaration in ['int', 'float']:
                    expression.append(consumedToken['TOKEN'])
                    consumedToken = tokens[tokenCount]
                    tokenCount += 1

                    expression.append(consumedToken['TOKEN'])
                    statements.append(expression)

                    if consumedToken['TYPE'] == 'INTEGER_CONSTANT' and typeDeclaration == 'int':
                        consumedToken = tokens[tokenCount]
                        tokenCount += 1

                    elif consumedToken['TYPE'] == 'FLOATING_CONSTANT' and typeDeclaration == 'float':
                        consumedToken = tokens[tokenCount]
                        tokenCount += 1

                    elif consumedToken['TYPE'] == 'IDENTIFIER': # TODO: Check if the identifier is declared
                        consumedToken = tokens[tokenCount]
                        tokenCount += 1

                if consumedToken['TOKEN'] == ';':
                    return parseStatements(tokenCount, tokens, functionDeclaration, functionIdentifier, statements)
                
            else:
                support.error(f'Expected ";" or "=", instead received "{consumedToken["TOKEN"]}"')
    
    elif consumedToken['TYPE'] == 'IDENTIFIER': # Assignments
        storedIdentifier = consumedToken['TOKEN']
        storedType = SymbolTable['Global'][functionIdentifier]["vars"][storedIdentifier]
        consumedToken = tokens[tokenCount]
        tokenCount += 1
        
        if consumedToken['TOKEN'] == '=':
            consumedToken = tokens[tokenCount]
            tokenCount += 1
            expression = []
            expression.append(consumedToken['TOKEN'])
            
            if consumedToken['TYPE'] == 'INTEGER_CONSTANT' and storedType == 'int':
                statements.append(["ASSIGN", storedIdentifier, consumedToken['TOKEN']])
                consumedToken = tokens[tokenCount]
                tokenCount += 1
            
            elif consumedToken['TYPE'] == 'FLOATING_CONSTANT' and storedType == 'float':
                statements.append(["ASSIGN", storedIdentifier, consumedToken['TOKEN']])
                consumedToken = tokens[tokenCount]
                tokenCount += 1
                
            elif consumedToken['TYPE'] in ['CHAR_CONSTANT', 'STRING_CONSTANT'] and storedType == 'char':
                statements.append(["ASSIGN", storedIdentifier, consumedToken['TOKEN']])
                consumedToken = tokens[tokenCount]
                tokenCount += 1

            elif consumedToken['TYPE'] == 'IDENTIFIER' and storedType == SymbolTable['Global'][functionIdentifier]["vars"][consumedToken['TOKEN']]: 
                statements.append(["ASSIGN", storedIdentifier, consumedToken['TOKEN']])
                consumedToken = tokens[tokenCount]
                tokenCount += 1
        
            else:
                support.error(f'Expected "{storedType}", instead received "{consumedToken["TOKEN"]}"')            

            if consumedToken['TOKEN'] in ['+', '-', '*', '/'] and storedType in ['int', 'float']:
                expression.append(consumedToken['TOKEN'])
                consumedToken = tokens[tokenCount]
                tokenCount += 1

                expression.append(consumedToken['TOKEN'])
                statements.append(expression)
                
                if consumedToken['TYPE'] == 'INTEGER_CONSTANT' and storedType == 'int':
                    consumedToken = tokens[tokenCount]
                    tokenCount += 1

                elif consumedToken['TYPE'] == 'FLOATING_CONSTANT' and storedType == 'float':
                    consumedToken = tokens[tokenCount]
                    tokenCount += 1

                elif consumedToken['TYPE'] == 'IDENTIFIER' and storedType == SymbolTable['Global'][functionIdentifier]["vars"][consumedToken['TOKEN']]: 
                    consumedToken = tokens[tokenCount]
                    tokenCount += 1

                
            if consumedToken['TOKEN'] == ';':
                return parseStatements(tokenCount, tokens, functionDeclaration, functionIdentifier, statements)
            
        elif consumedToken['TOKEN'] == ';':  
            return parseStatements(tokenCount, tokens, functionDeclaration, functionIdentifier, statements)
        
        else:
            support.error(f'Expected "=", instead received "{consumedToken["TOKEN"]}"')
    
    elif consumedToken['TOKEN'] == 'return': # Returns
        consumedToken = tokens[tokenCount]
        tokenCount += 1

        if consumedToken['TYPE'] == 'INTEGER_CONSTANT' and functionDeclaration == 'int':
            statements.append(["RETURN", consumedToken['TOKEN']])
            
        elif consumedToken['TYPE'] == 'FLOATING_CONSTANT' and functionDeclaration == 'float':
            statements.append(["RETURN", consumedToken['TOKEN']])
            
        elif consumedToken['TYPE'] in ['CHAR_CONSTANT', 'STRING_CONSTANT'] and functionDeclaration == 'char':
            statements.append(["RETURN", consumedToken['TOKEN']])
            
        elif consumedToken['TYPE'] == 'IDENTIFIER': # TODO: Check if the identifier is declared and right type
            statements.append(["RETURN", consumedToken['TOKEN']])

        else:
            support.error(f'Expected "{functionDeclaration}", instead received "{consumedToken["TOKEN"]}"')

        consumedToken = tokens[tokenCount]
        tokenCount += 1
        
        if consumedToken['TOKEN'] == ';':
            closingBraceIndex = lookAhead(tokenCount, tokens, '}')  # Look ahead for closing brace
            if closingBraceIndex == tokenCount:
                return statements
            else:
                return parseStatements(tokenCount, tokens, functionDeclaration, statements)
        
def lookAhead(tokenCount, tokens, searchToken):
    while tokenCount < len(tokens):
        if tokens[tokenCount]['TOKEN'] == searchToken:
            return tokenCount  # Return index of the closing brace
        tokenCount += 1
    return -1  # Return -1 if closing brace == not found
