# External Libraries
import argparse
import pdb

# Internal Libraries
import support
import lexer
from parser import *
import tac
import optimizations

"""
Main function that processes a given C source file and optionally runs a lexer.

This function sets up an argument parser to handle command-line arguments, reads
the specified C source file, checks its validity, tokenizes its contents, and writes
the tokens to an output file. If the lexer flag is provided, it also prints the tokenized
output in a readable format.
"""
def main():
    
    # Create argument parser object
    argParser = argparse.ArgumentParser(description='Construction Compiler with various arguments')

    # Add Arguments
    argParser.add_argument('-L', '--lexer', action='store_true', help='Print tokenized output')
    argParser.add_argument('-P', '--parse', action='store_true', help='Print AST and Symbol Table')
    argParser.add_argument('-T', '--tac', action='store_true', help='Print Three Address Code')
    argParser.add_argument('-O1', '--opt1', action='store_true', help='Print Three Address Code with Constant Folding and Propagation Pass')
    argParser.add_argument('file', help='Given C source file')

    # Parse the arguments
    args = argParser.parse_args()

    try:
        contents = open(args.file, "r").read()
    except FileNotFoundError as error:
        support.error(f"{error}")
        return None
    if(support.checkExtensions(args.file) == False):
        support.warning(f"File is not supported. Results may vary\nPATH: {args.file}\n")

    tokens = lexer.tokenize(contents)
    parser = Parser(tokens)
    parser.parseProgram()
    tacDict, symbolTable = tac.generateTAC(parser.abstractSyntaxTree, parser.symbolTable)
    tactDict = optimizations.constPropFold(tacDict, parser.symbolTable)

    fileName = support.retrieveFileName(args.file)
    support.writeToFile(tokens, f"tokens_{fileName}.txt")
    support.writeToFile(parser.abstractSyntaxTree, f"absSyntaxTree_{fileName}.txt")
    support.writeToFile(symbolTable, f"symbolTable_{fileName}.txt")
    support.writeToFile(tacDict, f"TAC_{fileName}.txt")

    # Check if the flags are set
    if args.lexer:
        support.prettyPrintLex(tokens)

    if args.parse:
        support.printAST(parser.abstractSyntaxTree)
        support.printSymbolTable(symbolTable)

    if args.tac:
        support.printTAC(tacDict)
        
    if args.opt1:
        support.printTAC(tactDict)

if __name__ == "__main__":
    main()