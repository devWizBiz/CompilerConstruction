# External Libraries
import argparse
# Internal Libraries
import lexer

""" Main Function: Generates given output based on the given arguments """
def main():
    
    parser = argparse.ArgumentParser(description='Construction Compiler with various arguments')
    parser.add_argument('-L', '--lexer', help='Run through the lexer')
    parser.add_argument('file', help='Given C source file')
    parser.parse_args()
    
main()