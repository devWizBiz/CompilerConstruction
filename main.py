# External Libraries
import argparse
# Internal Libraries
import lexer

def error(msg):
    RED = '\033[91m'
    END = '\033[0m'
    print(f"{RED}ERROR: {msg}{END}")

""" Main Function: Generates given output based on the given arguments """
def main():
    
    # Create argument parser object
    parser = argparse.ArgumentParser(description='Construction Compiler with various arguments')

    # Add Arguments
    parser.add_argument('-L', '--lexer', action='store_true', help='Run through the lexer')
    parser.add_argument('file', help='Given C source file')

    # Parse the arguments
    args = parser.parse_args()

    # Check if the lexer flag is set
    if args.lexer:
        try:
            contents = open(args.file, "r").read()
            lexObj = lexer.Lexer(contents)
        except FileNotFoundError:
            error(f"File not found.\nPATH: {args.file}")
    else:
        error(f"Cannot process file without lexer.\nPATH: {args.file}")
    
main()