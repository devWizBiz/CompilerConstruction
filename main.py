# External Libraries
import argparse

# Internal Libraries
import support
import lexer

"""
Main function that processes a given C source file and optionally runs a lexer.

This function sets up an argument parser to handle command-line arguments, reads
the specified C source file, checks its validity, tokenizes its contents, and writes
the tokens to an output file. If the lexer flag is provided, it also prints the tokenized
output in a readable format.
"""
def main():
    
    # Create argument parser object
    parser = argparse.ArgumentParser(description='Construction Compiler with various arguments')

    # Add Arguments
    parser.add_argument('-L', '--lexer', action='store_true', help='Run through the lexer')
    parser.add_argument('file', help='Given C source file')

    # Parse the arguments
    args = parser.parse_args()

    try:
        contents = open(args.file, "r").read()
    except FileNotFoundError as error:
        support.error(f"{error}")
        return None

    if(support.checkExtensions(args.file) == False):
        support.warning(f"File is not supported. Results may vary\nPATH: {args.file}\n")
    tokens = lexer.tokenize(contents)
    fileName = support.retrieveFileName(args.file)
    support.writeToFile(tokens, f"tokens_{fileName}.txt")

    # Check if the lexer flag is set
    if args.lexer:
        support.prettyPrintOutput(tokens)
        
main()