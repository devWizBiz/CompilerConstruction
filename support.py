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
    listOfKeys = list(input.keys())
    for key in listOfKeys:
        print(f"--- {key} ---")
        listOfSubKeys = list(input[key].keys())
        for subKey in listOfSubKeys:
            if subKey != 'vars':
                print(f"-- {subKey} : {input[key][subKey]}")
            else:
                print(f"-- vars:")
                varKeys = list(input[key][subKey])
                for var in varKeys:
                    print(f"--- {var} : {input[key][subKey][var]}")
                            
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