# External Libraries
import argparse

# Internal Libraries
import support
from lexer import Tokenizer
from parser import Parser
from tac import TAC
from optimizer import Optimizer
from assemblyGeneration import asmGenerator

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
    argParser.add_argument('-L', '--lexer', action='store_true', help='Tokenized output')
    argParser.add_argument('-P', '--parse', action='store_true', help='AST and Symbol Table')
    argParser.add_argument('-T', '--tac', action='store_true', help='Three Address Code')
    argParser.add_argument('-O1', '--opt1', action='store_true', help='Constant Propagation optimization (last used optimization will be shown)')
    argParser.add_argument('-O2', '--opt2', action='store_true', help='Constant Folding optimization (last used optimization will be shown)')
    argParser.add_argument('-O3', '--opt3', action='store_true', help='Dead Code Elimination optimization (last used optimization will be shown)')
    argParser.add_argument('-A', '--asm', action='store_true', help='Assemble Generation')
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

    # Create token object, find tokens
    tokenObj = Tokenizer()
    tokenObj.findTokens( contents )
    
    # Create parser object, parse the contents
    parser = Parser(tokenObj.tokenDict)
    ST, AST = parser.parseProgram()
    
    # Create three address code
    tac = TAC()
    tac.generateTAC(AST.AbstractSyntaxTreeDictionary, ST.SymbolTableDictionary)

    # Create optimization pass
    optimizations = [args.opt1, args.opt2, args.opt3 ]
    if(optimizations):
        optimize = Optimizer(tac.basicBlockDict, ST.SymbolTableDictionary, optimizations)
        tac.basicBlockDict = optimize.basicBlocks
    
    # Create Assembly
    asm = asmGenerator(tac.basicBlockDict, ST.SymbolTableDictionary, tokenObj.tokenDict)

    fileName = support.retrieveFileName(args.file)
    support.writeToFile(tokenObj.tokenDict, f"tokens_{fileName}.txt")
    support.writeToFile(AST.AbstractSyntaxTreeDictionary, f"absSyntaxTree_{fileName}.txt")
    support.writeToFile(tac.tactDict, f"TAC_{fileName}.txt")
    support.writeToFile(ST.SymbolTableDictionary, f"symbolTable_{fileName}.txt")
    support.writeToFile(optimize.optimizedBlocks, f"optimizedPass_{fileName}.txt")
    support.writeToFile(asm.asmList, f"asmList_{fileName}.txt")

    # Check if the flags are set
    if args.lexer:
        support.prettyPrintLex(tokenObj.tokenDict)

    if args.parse:
        support.printAST(AST.AbstractSyntaxTreeDictionary)
        support.printSymbolTable(ST.SymbolTableDictionary)

    if args.tac:
        support.printTAC(tac.tactDict)
        
    if args.opt1 or args.opt2 or args.opt3:
        support.printOptimizedPass(optimize.optimizedBlocks)
        
    if args.asm:
        support.printASMList(asm.asmList)

if __name__ == "__main__":
    main()