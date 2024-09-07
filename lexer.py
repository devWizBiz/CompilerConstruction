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
    ('UNSUPPORTED', r'.')
]

# Join the token patterns through the OR operator along with it's sub-pattern name
patterns_combined = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_PATTERNS)


"""
Tokenizes the given source code into a structured format.

This function processes the provided code string and extracts tokens based on predefined patterns. 
It skips comments and whitespace, and logs a warning for unsupported tokens. Each token is 
stored with its type, line number, and column position.

    Args:
        code (str): The source code to be tokenized.

    Returns:
        dict: A dictionary where each key is a token ID and each value is a dictionary containing the token's details (TOKEN, TYPE, LINE, COL).

    Raises:
        None

    Examples:
        tokenize("int main() {}")
            {0: {'TOKEN': 'int', 'TYPE': 'KEYWORD', 'LINE': 1, 'COL': 0}, 
            1: {'TOKEN': 'main', 'TYPE': 'IDENTIFIER', 'LINE': 1, 'COL': 4}, 
            2: {'TOKEN': '(', 'TYPE': 'PARENTHESIS', 'LINE': 1, 'COL': 8}, 
            3: {'TOKEN': ')', 'TYPE': 'PARENTHESIS', 'LINE': 1, 'COL': 9}, 
            4: {'TOKEN': '{', 'TYPE': 'BRACE', 'LINE': 1, 'COL': 10}, 
            5: {'TOKEN': '}', 'TYPE': 'BRACE', 'LINE': 1, 'COL': 11}}
"""
def tokenize(code):
    tokens = {}
    tokenID = 0
    compiledPattern = re.compile(patterns_combined)
    for match in compiledPattern.finditer(code):
        kind = match.lastgroup
        value = match.group()
        if kind in ['SINGLELINE_COMMENT', 'MULTILINE_COMMENT', 'WHITESPACE']:  # For now, skip comments and whitespace:
                continue
        elif kind == 'UNSUPPORTED':
            support.warning(f"Unsupported token found: {value}")
            continue
        newToken = {
            "TOKEN": value,
            "TYPE": kind,
            "LINE": code.count('\n', 0, match.start()) + 1,
            "COL": match.start() - code.rfind('\n', 0, match.start())
            }
        tokens[tokenID] = newToken
        tokenID += 1
    return tokens