# External Libraries
from pathlib import Path
import pprint
import sys
import pdb

YELLOW = '\033[93m'
RED = '\033[91m'
RESTORE = '\033[0m'

def error(msg):
    sys.stderr.write(f"{RED}ERROR: {RESTORE}{msg}\n")
    
def warning(msg):
    sys.stderr.write(f"{YELLOW}Warning: {RESTORE}{msg}\n")
    
def prettyPrintLex(input):
    pprint.pprint(input)

def printSymbolTable(input):
    print("#########--- Symbol Table ---#########")
    print("Global")
    for key in input['Global']:
        try:
            returnType = input['Global'][key]['retType']
            args = input['Global'][key]['args']
            print(f"-- {key}")
            print(f"---- returnType : {returnType}")
            print(f"---- Arguments : {args}")
            print(f"---- Variables:")
            for var in input['Global'][key]['vars']:
                theVar = input['Global'][key]['vars'][var]
                print(f"------ {var} : {theVar}")
        except:
            print(f"-- {key} : {input['Global'][key]}")

def printAST(input):
    print("#########--- Abstract Syntax Tree ---#########")
    print("Program")
    for key in input['Program']:
        print(f"-- {key}")
        for statement in input['Program'][key]:
            print(f"---- {statement}")

def writeToFile(input, fileName):
    with open(fileName, 'w') as file:
        file.write(str(input) + '\n')
        
def checkExtensions(filePath):
    if filePath.endswith('.c'):
        return True

def retrieveFileName(filePath):
    fileName = Path(filePath).stem
    return fileName