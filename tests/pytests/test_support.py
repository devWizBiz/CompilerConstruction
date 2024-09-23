# Test for support.py
# Written by Chat GPT-4o
import pytest
from unittest import mock
import support

def test_error():
    with mock.patch('sys.stderr.write') as mock_write:
        support.error("Test error message")
        mock_write.assert_called_once_with("\033[91mERROR: \033[0mTest error message\n")

def test_warning():
    with mock.patch('sys.stderr.write') as mock_write:
        support.warning("Test warning message")
        mock_write.assert_called_once_with("\033[93mWarning: \033[0mTest warning message\n")

def test_prettyPrintOutput():
    sample_data = {"key": "value"}
    with mock.patch('pprint.pprint') as mock_pprint:
        support.prettyPrintOutput(sample_data)
        mock_pprint.assert_called_once_with(sample_data)

def test_writeToFile():
    sample_data = {"key": "value"}
    with mock.patch('builtins.open', mock.mock_open()) as mock_file:
        support.writeToFile(sample_data, "test_file.txt")
        mock_file.assert_called_once_with("test_file.txt", 'w')
        handle = mock_file()

        # Adjust based on pprint's formatted output
        handle.write.assert_called_once_with("{'key': 'value'}\n")
