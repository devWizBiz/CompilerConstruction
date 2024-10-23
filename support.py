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
    print("Global(s)")
    for key in input['Global(s)']:
        try:
            returnType = input['Global(s)'][key]['retType']
            args = input['Global(s)'][key]['args']
            print(f"-- {key}")
            print(f"---- returnType : {returnType}")
            print(f"---- Arguments : {args}")
            print(f"---- Variables:")
            for var in input['Global(s)'][key]['vars']:
                theVar = input['Global(s)'][key]['vars'][var]
                print(f"------ {var} : {theVar}")
        except:
            print(f"-- {key} : {input['Global(s)'][key]}")

def printAST(input):
    print("#########--- Abstract Syntax Tree ---#########")
    input = input['Program']
    for key in input:
        print(f"-- {key}")
        if type(input[key]) == dict:
            for statement in input[key]:
                print(f"---- {statement} : {input[key][statement]}")
        else:
            print(f"---- {input[key]}")
            
def printTAC(input):
    print("#########--- Three Address Code ---#########")
    for key in input:
        print(f"-- {key}")
        for statement in input[key]:
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