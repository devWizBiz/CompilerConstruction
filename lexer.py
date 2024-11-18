# External Libraries
import re
# Internal Libraries
import support

class Tokenizer:
    def  __init__(self):
        
        # Initialize an empty dictionary
        self.tokenDict = {}
        
        # Load Token Pattern for matches in input
        self.loadTokenPattern()

    """
    Loads the token patterns that will be used to determine the match for the input in retrieveTokens.
    """        
    def loadTokenPattern(self):
        # Defined Token Types (ISO/IEC 9899:201x)
        TOKEN_PATTERNS = [
            ('KEYWORD', r'\b(break|else|float|if|int|return|void)\b'),
            ('PUNCTUATORS', r'\(|\)|{|}|-|\+|![=]*|/[=]*(?![/\*]+)|<[=]|>[=]|=[=]*|\*|;'),
            ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
            ('INTEGER_CONSTANT', r'\b\d+\b(?!\.\d)'),
            ('FLOATING_CONSTANT', r'\b\d*\.\d+\b'),
            ('SINGLELINE_COMMENT', r'\/\/.*'),
            ('MULTILINE_COMMENT', r'/\*[\S\s]*\*/'),
            ('WHITESPACE', r'\s+'),
            ('UNSUPPORTED', r'\b.+\b') ]
        
        # Join the token patterns through the OR operator along with it's sub-pattern name
        self.PATTERNS_COMBINED = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_PATTERNS)

    """
    Tokenizes the given source inputStr into a structured format.

    This function processes the provided inputStr string and extracts tokens based on predefined patterns. 
    It skips comments and whitespace, and logs a warning for unsupported tokens. Each token is 
    stored with its type, line number, and column position.
    """
    def findTokens(self, inputStr):
        tokenID = 0
        compiledPattern = re.compile(self.PATTERNS_COMBINED)
        for match in compiledPattern.finditer(inputStr):
            kind = match.lastgroup
            value = match.group()
            line = inputStr.count('\n', 0, match.start()) + 1
            column = match.start() - inputStr.rfind('\n', 0, match.start())
            
            if kind in ['SINGLELINE_COMMENT', 'MULTILINE_COMMENT', 'WHITESPACE']:  # Skip comments and whitespace:
                    continue
            elif kind == 'UNSUPPORTED':
                support.error(f'Unsupported token found at LINE {line} COLUMN {column}: {value}') 
                continue
            
            newToken = {
                'TOKEN': value,
                'TYPE': kind,
                'LINE': line,
                'COL': column
                }
            self.tokenDict[tokenID] = newToken
            tokenID += 1
