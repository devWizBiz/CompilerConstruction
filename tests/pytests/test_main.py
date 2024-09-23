import sys
from pathlib import Path
import pytest
from unittest.mock import patch, Mock, mock_open

# Add two levels up to sys.path
current_dir = Path.cwd()
two_levels_up = current_dir.parents[1]
sys.path.append(str(two_levels_up))

# Import main after updating sys.path
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

def test_file_not_found():
    with patch('builtins.open', side_effect=FileNotFoundError("No such file or directory: 'non_existent_file.c'")):
        with patch('support.error') as mock_error:
            with patch('argparse.ArgumentParser.parse_args', return_value=Mock(file='non_existent_file.c')):
                main.main()
                mock_error.assert_called_once_with("No such file or directory: 'non_existent_file.c'")

def test_unsupported_file_extension():
    # Mock the content of the file
    with patch("builtins.open", new_callable=mock_open, read_data=sample_content):
        with patch('support.checkExtensions', return_value=False):
            with patch('support.warning') as mock_warning:
                with patch('argparse.ArgumentParser.parse_args', return_value=Mock(file='unsupported_file.txt')):
                    main.main()
                    mock_warning.assert_called_once_with("File is not supported. Results may vary\nPATH: unsupported_file.txt\n")

def test_tokenization_and_file_write():
    # Mock the content of the file
    with patch("builtins.open", new_callable=mock_open, read_data=sample_content):
        with patch('lexer.tokenize', return_value=sample_tokens) as mock_tokenize:
            with patch('support.writeToFile') as mock_write:
                with patch('argparse.ArgumentParser.parse_args', return_value=Mock(file='existent_file.c')):
                    main.main()
                    mock_tokenize.assert_called_once_with(sample_content)
                    mock_write.assert_called_once_with(sample_tokens, "tokens_existent_file.txt")

def test_lexer_flag():
    # Mock the content of the file
    with patch("builtins.open", new_callable=mock_open, read_data=sample_content):
        with patch('lexer.tokenize', return_value=sample_tokens):
            with patch('support.writeToFile'):
                with patch('support.prettyPrintOutput') as mock_pretty_print:
                    with patch('argparse.ArgumentParser.parse_args', return_value=Mock(lexer=True, file='existent_file.c')):
                        main.main()
                        mock_pretty_print.assert_called_once_with(sample_tokens)
