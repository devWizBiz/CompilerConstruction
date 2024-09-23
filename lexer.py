# External Libraries
import re

# Internal Libraries
import support

# Defined Token Types (ISO/IEC 9899:201x)
TOKEN_PATTERNS = [
    ('KEYWORD', r'\b(auto|break|case|char|const|continue|do|default|else|enum|'
                r'extern|float|for|if|inline|int|long|register|restrict|return|'
                r'short|signed|sizeof|static|switch|typedef|union|unsigned|void|'
                r'volatile|while)\b'),
    ('PUNCTUATORS', r'\[|\]|\(|\)|{|}|[\.](?![\.])|[\.]{3}|-[=>-]*|\+[\+=]*|&[&=]*|'
                    r'\*[=]*|~|![=]*|/[=]*(?![/\*]+)|%[=>]*|<[<=:%]*[=]*|>[>=]*[=]*|=[=]*|'
                    r'\^[=]*|\|[\|=]*|\?|:[>]*|;|,'),
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('INTEGER_CONSTANT', r'\b\d+\b(?!\.\d)'),
    ('FLOATING_CONSTANT', r'\b\d*\.\d+\b'),
    ('STRING_CONSTANT', r'\".*\"'),
    ('CHAR_CONSTANT', r'\'[^\'\\\n]\''),
    ('SINGLELINE_COMMENT', r'\/\/.*'),
    ('MULTILINE_COMMENT', r'/\*[\S\s]*\*/'),
    ('WHITESPACE', r'\s+'),
    ('UNSUPPORTED', r'\b.+\b')
]

# Join the token patterns through the OR operator along with it's sub-pattern name
PATTERNS_COMBINED = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_PATTERNS)

"""
Tokenizes the given source code into a structured format.

This function processes the provided code string and extracts tokens based on predefined patterns. 
It skips comments and whitespace, and logs a warning for unsupported tokens. Each token is 
stored with its type, line number, and column position.
"""
def tokenize(code):
    tokens = {}
    tokenID = 0
    compiledPattern = re.compile(PATTERNS_COMBINED)
    for match in compiledPattern.finditer(code):
        kind = match.lastgroup
        value = match.group()
        line = code.count('\n', 0, match.start()) + 1
        column = match.start() - code.rfind('\n', 0, match.start())
        if kind in ['SINGLELINE_COMMENT', 'MULTILINE_COMMENT', 'WHITESPACE']:  # For now, skip comments and whitespace:
                continue
        elif kind == 'UNSUPPORTED':
            support.error(f"Unsupported token found at LINE {line} COLUMN {column}: {value}") 
            continue
        newToken = {
            "TOKEN": value,
            "TYPE": kind,
            "LINE": line,
            "COL": column
            }
        tokens[tokenID] = newToken
        tokenID += 1
    return tokens