# Test cases for lexer.py
# Written by Chat GPT-4o
import pytest
from unittest import mock
import lexer
import support

# Helper function to load content from a file
def load_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def test_tokenize_valid_content():
    # Load content from testMain.c
    sample_content = load_file_content('tests/source_files/testMain.c')
    sample_tokens = {
        0: {'COL': 1, 'LINE': 1, 'TOKEN': 'int', 'TYPE': 'KEYWORD'},
        1: {'COL': 5, 'LINE': 1, 'TOKEN': 'main', 'TYPE': 'IDENTIFIER'},
        2: {'COL': 9, 'LINE': 1, 'TOKEN': '(', 'TYPE': 'PUNCTUATORS'},
        3: {'COL': 10, 'LINE': 1, 'TOKEN': ')', 'TYPE': 'PUNCTUATORS'},
        4: {'COL': 11, 'LINE': 1, 'TOKEN': '{', 'TYPE': 'PUNCTUATORS'},
        5: {'COL': 5, 'LINE': 2, 'TOKEN': 'int', 'TYPE': 'KEYWORD'},
        6: {'COL': 9, 'LINE': 2, 'TOKEN': 'tmp', 'TYPE': 'IDENTIFIER'},
        7: {'COL': 13, 'LINE': 2, 'TOKEN': '=', 'TYPE': 'PUNCTUATORS'},
        8: {'COL': 15, 'LINE': 2, 'TOKEN': '12', 'TYPE': 'INTEGER_CONSTANT'},
        9: {'COL': 17, 'LINE': 2, 'TOKEN': ';', 'TYPE': 'PUNCTUATORS'},
        10: {'COL': 5, 'LINE': 3, 'TOKEN': 'float', 'TYPE': 'KEYWORD'},
        11: {'COL': 11, 'LINE': 3, 'TOKEN': 't_VarOne', 'TYPE': 'IDENTIFIER'},
        12: {'COL': 20, 'LINE': 3, 'TOKEN': '=', 'TYPE': 'PUNCTUATORS'},
        13: {'COL': 22, 'LINE': 3, 'TOKEN': '3.14', 'TYPE': 'FLOATING_CONSTANT'},
        14: {'COL': 26, 'LINE': 3, 'TOKEN': ';', 'TYPE': 'PUNCTUATORS'},
        15: {'COL': 5, 'LINE': 4, 'TOKEN': 'char', 'TYPE': 'KEYWORD'},
        16: {'COL': 11, 'LINE': 4, 'TOKEN': 't_VarTwo', 'TYPE': 'IDENTIFIER'},
        17: {'COL': 20, 'LINE': 4, 'TOKEN': '=', 'TYPE': 'PUNCTUATORS'},
        18: {'COL': 22, 'LINE': 4, 'TOKEN': "'c'", 'TYPE': 'CHAR_CONSTANT'},
        19: {'COL': 25, 'LINE': 4, 'TOKEN': ';', 'TYPE': 'PUNCTUATORS'},
        20: {'COL': 5, 'LINE': 5, 'TOKEN': 'char', 'TYPE': 'KEYWORD'},
        21: {'COL': 11, 'LINE': 5, 'TOKEN': 't_var3', 'TYPE': 'IDENTIFIER'},
        22: {'COL': 17, 'LINE': 5, 'TOKEN': '[', 'TYPE': 'PUNCTUATORS'},
        23: {'COL': 18, 'LINE': 5, 'TOKEN': ']', 'TYPE': 'PUNCTUATORS'},
        24: {'COL': 20, 'LINE': 5, 'TOKEN': '=', 'TYPE': 'PUNCTUATORS'},
        25: {'COL': 22, 'LINE': 5, 'TOKEN': '"Hello, this is a string"', 'TYPE': 'STRING_CONSTANT'},
        26: {'COL': 47, 'LINE': 5, 'TOKEN': ';', 'TYPE': 'PUNCTUATORS'},
        27: {'COL': 5, 'LINE': 9, 'TOKEN': 'return', 'TYPE': 'KEYWORD'},
        28: {'COL': 12, 'LINE': 9, 'TOKEN': '0', 'TYPE': 'INTEGER_CONSTANT'},
        29: {'COL': 13, 'LINE': 9, 'TOKEN': ';', 'TYPE': 'PUNCTUATORS'},
        30: {'COL': 1, 'LINE': 10, 'TOKEN': '}', 'TYPE': 'PUNCTUATORS'}
    }
    
    tokens = lexer.tokenize(sample_content)
    assert tokens == sample_tokens

def test_tokenize_unsupported_token():
    content_with_unsupported = "int main() { 12TMP }"
    with mock.patch('support.error') as mock_warning:
        tokens = lexer.tokenize(content_with_unsupported)
        assert tokens[0] == {"TOKEN": "int", "TYPE": "KEYWORD", "LINE": 1, "COL": 1}
        assert tokens[1] == {"TOKEN": "main", "TYPE": "IDENTIFIER", "LINE": 1, "COL": 5}
        assert tokens[2] == {"TOKEN": "(", "TYPE": "PUNCTUATORS", "LINE": 1, "COL": 9}
        assert tokens[3] == {"TOKEN": ")", "TYPE": "PUNCTUATORS", "LINE": 1, "COL": 10}
        assert tokens[4] == {"TOKEN": "{", "TYPE": "PUNCTUATORS", "LINE": 1, "COL": 12}
        assert tokens[5] == {"TOKEN": "}", "TYPE": "PUNCTUATORS", "LINE": 1, "COL": 20}
        mock_warning.assert_called_once_with("Unsupported token found at LINE 1 COLUMN 14: 12TMP")

def test_tokenize_empty_content():
    tokens = lexer.tokenize("")
    assert tokens == {}
