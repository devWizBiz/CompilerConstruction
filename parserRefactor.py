# External Libraries
import pdb
import re

# Internal Libraries
import support

# Global
SymbolTable = {"Global": {}}
AST = {"Program": {}}

PARSER_PATTERNS = [
    ('GLOBAL_FUNCTION_DECLARATION', r'(void||int||float||char)IDENTIFIER\(\)\{\}'),
    ('GLOBAL_FUNCTION_DECLARATION_PARTIAL', r'(void||int||float||char)IDENTIFIER\(\)\{'),
    ('GLOBAL_VARIABLE_DECLARATION', r'(int||float||char)IDENTIFIER;'),
    ('GLOBAL_VARIABLE_ASSIGNMENT_FLOAT', r'floatIDENTIFIER=FLOATING_CONSTANT;'),
    ('GLOBAL_VARIABLE_ASSIGNMENT_INT', r'intIDENTIFIER=INTEGER_CONSTANT;'),
    ('GLOBAL_VARIABLE_ASSIGNMENT_CHAR', r'charIDENTIFIER=CHAR_CONSTANT;'),
    ('GLOBAL_VARIABLE_ASSIGNMENT_STRING', r'charIDENTIFIER\[\]=STRING_CONSTANT;'),
]

# Join the tokenPos patterns through the OR operator along with it's sub-pattern name
PATTERNS_COMBINED = '|'.join('(?P<%s>%s)' % pair for pair in PARSER_PATTERNS)
COMPILED_PATTERNS = re.compile(PATTERNS_COMBINED)

def parserProgram(tokens):
    tokenPos = 0
    parseFunctions(tokens, tokenPos)
    return AST, SymbolTable

def parseFunctions(tokens, tokenPos):

    # Check against RegEx    
    searchString = ""
    tokensInfo = []
    while tokenPos < len(tokens):

        if tokens[tokenPos]['TYPE'] in ['KEYWORD', 'PUNCTUATORS']:
            searchValue = tokens[tokenPos]['TOKEN']
        else:
            searchValue = tokens[tokenPos]['TYPE']
        
        searchString += searchValue
        tokensInfo.append((tokens[tokenPos]['TOKEN'], tokens[tokenPos]['TYPE']))
        
        match = COMPILED_PATTERNS.search(searchString)
        if not match:
            tokenPos += 1
            continue
    
        if match.lastgroup == 'GLOBAL_VARIABLE_DECLARATION':
            SymbolTable["Global"][tokensInfo[1][0]] = tokensInfo[0][0]
        
        elif match.lastgroup in ['GLOBAL_VARIABLE_ASSIGNMENT_FLOAT', 'GLOBAL_VARIABLE_ASSIGNMENT_INT', 
                                'GLOBAL_VARIABLE_ASSIGNMENT_CHAR', 'GLOBAL_VARIABLE_ASSIGNMENT_STRING']:
            SymbolTable["Global"][tokensInfo[1][0]] = tokensInfo[0][0]
        
        elif match.lastgroup == 'GLOBAL_FUNCTION_DECLARATION_PARTIAL':
            lookingIndex = lookAhead(tokens, tokenPos, '}')
            
            if lookingIndex != -1:
                searchString += tokens[lookingIndex]['TOKEN']
                match = COMPILED_PATTERNS.search(searchString)
            
                if match.lastgroup == 'GLOBAL_FUNCTION_DECLARATION':
                    SymbolTable["Global"][tokensInfo[1][0]] = {'retType':tokensInfo[0][0], "args":"None", "vars":{}}
                    tokenPos = parseStatements(tokens, tokenPos)
                    parseFunctions(tokens, tokenPos)
                    break               
        
        tokenPos += 1
        searchString = "" # Reset the search string
        tokensInfo = [] # Reset the tokens info


def parseStatements( tokens, tokenPos):
    lookAheadIndex = lookAhead(tokens, tokenPos, '}') # STUBBED
    return lookAheadIndex + 1

def checkExpression():
    pass

def lookAhead(tokens, tokenIndex, searchToken):
    while tokenIndex < len(tokens):
        if tokens[tokenIndex]['TOKEN'] == searchToken:
            return tokenIndex  # Return index of the search tokenPos
        tokenIndex += 1
    return -1  # Return -1 
