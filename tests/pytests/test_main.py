# Test cases for main.py
# Written by Chat GPT-4o
import pytest
from unittest import mock
import main
import support
import lexer

# Sample content for testing
sample_content = "int main() { return 0; }"
sample_tokens = {
    0: {"TOKEN": "int", "TYPE": "KEYWORD", "LINE": 1, "COL": 0},
    1: {"TOKEN": "main", "TYPE": "IDENTIFIER", "LINE": 1, "COL": 4},
    2: {"TOKEN": "(", "TYPE": "PUNCTUATORS", "LINE": 1, "COL": 8},
    3: {"TOKEN": ")", "TYPE": "PUNCTUATORS", "LINE": 1, "COL": 9},
    4: {"TOKEN": "{", "TYPE": "PUNCTUATORS", "LINE": 1, "COL": 10},
    5: {"TOKEN": "return", "TYPE": "KEYWORD", "LINE": 1, "COL": 12},
    6: {"TOKEN": "0", "TYPE": "INTEGER_CONSTANT", "LINE": 1, "COL": 19},
    7: {"TOKEN": ";", "TYPE": "PUNCTUATORS", "LINE": 1, "COL": 20},
    8: {"TOKEN": "}", "TYPE": "PUNCTUATORS", "LINE": 1, "COL": 21}
}

def mock_open(file_name, *args, **kwargs):
    if file_name == 'existent_file.c':
        return mock.mock_open(read_data=sample_content)()
    raise FileNotFoundError

def test_file_not_found():
    with mock.patch('builtins.open', mock_open):
        with mock.patch('support.error') as mock_error:
            with mock.patch('argparse.ArgumentParser.parse_args', return_value=mock.Mock(file='non_existent_file.c')):
                main.main()
                mock_error.assert_called_once_with("FileNotFoundError(2, 'No such file or directory: 'non_existent_file.c')")

def test_unsupported_file_extension():
    with mock.patch('builtins.open', mock_open):
        with mock.patch('support.checkExtensions', return_value=False):
            with mock.patch('support.warning') as mock_warning:
                with mock.patch('argparse.ArgumentParser.parse_args', return_value=mock.Mock(file='unsupported_file.txt')):
                    main.main()
                    mock_warning.assert_called_once_with("File is not supported. Results may vary\nPATH: unsupported_file.txt\n")

def test_tokenization_and_file_write():
    with mock.patch('builtins.open', mock_open):
        with mock.patch('lexer.tokenize', return_value=sample_tokens) as mock_tokenize:
            with mock.patch('support.writeToFile') as mock_write:
                with mock.patch('argparse.ArgumentParser.parse_args', return_value=mock.Mock(file='existent_file.c')):
                    main.main()
                    mock_tokenize.assert_called_once_with(sample_content)
                    mock_write.assert_called_once_with(sample_tokens, "tokens.txt")

def test_lexer_flag():
    with mock.patch('builtins.open', mock_open):
        with mock.patch('lexer.tokenize', return_value=sample_tokens):
            with mock.patch('support.writeToFile'):
                with mock.patch('support.prettyPrintOutput') as mock_pretty_print:
                    with mock.patch('argparse.ArgumentParser.parse_args', return_value=mock.Mock(lexer=True, file='existent_file.c')):
                        main.main()
                        mock_pretty_print.assert_called_once_with(sample_tokens)
