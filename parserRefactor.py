# External Libraries
import pdb
import re

# Internal Libraries
import support

PARSER_PATTERNS = [
    ('FUNCTION_DECLARATION', r'(void||int||float||char)IDENTIFIER)\(\)\{\}'),
    ('VARIABLE_DECLARATION', r'(int||float||char)IDENTIFIER;'),
    ('VARIABLE_ASSIGNMENT_FLOAT', r'floatIDENTIFIER=FLOATING_CONSTANT;'),
    ('VARIABLE_ASSIGNMENT_INT', r'intIDENTIFIER=INTEGER_CONSTANT;'),
    ('VARIABLE_ASSIGNMENT_CHAR', r'charIDENTIFIER=CHAR_CONSTANT;'),
    ('VARIABLE_ASSIGNMENT_STRING', r'charIDENTIFIER\[\]=STRING_CONSTANT;'),
]

# Join the token patterns through the OR operator along with it's sub-pattern name
PATTERNS_COMBINED = '|'.join('(?P<%s>%s)' % pair for pair in PARSER_PATTERNS)
COMPILED_PATTERNS = re.compile(PATTERNS_COMBINED)

def parserProgram(tokens):
    tokensLeft = len(tokens)
    parseFunctions(tokens, tokensLeft)

def parseFunctions(tokens, tokensLeft):

    # Check against RegEx    
    searchString = ""
    for token in tokens:

        if tokens[token]['TYPE'] in ['KEYWORD', 'PUNCTUATORS']:
            searchValue = tokens[token]['TOKEN']
        else:
            searchValue = tokens[token]['TYPE']
        searchString += searchValue
        
        for match in COMPILED_PATTERNS.finditer(searchString):
            print(f'Test String: {searchString}')
            print(f'Matched string: {match.group()}')
            print(f'Matched Type: {match.lastgroup}')
            print(f'Start position: {match.start()}')
            print(f'End position: {match.end()}')
            print('---')
            searchString = "" # Reset
        else:
            pdb.set_trace()
    
    parseStatements()

def parseStatements():
    pass

def checkExpression():
    pass

def lookAhead(tokens, tokenIndex, searchToken):
    while tokenIndex < len(tokens):
        if tokens[tokenIndex]['TOKEN'] == searchToken:
            return tokenIndex  # Return index of the search Token
        tokenIndex += 1
    return -1  # Return -1 
