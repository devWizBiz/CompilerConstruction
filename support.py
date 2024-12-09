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
            
def printOptimizedPass(input):
    print("#########--- Optimized Pass Three Address Code ---#########")
    for key in input:
        print(f"-- {key}")
        for tac in input[key]:
            print(f"---- {tac}")

def printASMList(input):
    print("#########--- ASM LIST ---#########")
    for function, ASM in input:
        print(f'{function}:')
        for instr in ASM:
            print(f'{instr}')

def writeToFile(input, fileName, type):
    with open(fileName, 'w') as file:
        if type == "token":
            file.write("#########--- Tokens ---#########\n")
            for token in input:
                file.write(f'{input[token]}\n')
        elif type == "abs":
            file.write("#########--- Abstract Syntax Tree ---#########\n")
            for key in input:
                file.write(f"-- {key}\n")
                for statements in input[key]:
                    file.write(f"---- {statements}\n")
                    for statement in input[key]['statements']:
                        file.write(f"------ {statement}\n")
        elif type == "tac":
            file.write("#########--- Three Address Code ---#########\n")
            for key in input:
                file.write(f"-- {key}\n")
                for statement in input[key]:
                    file.write(f"---- {statement}\n")
        elif type == "st":
            file.write("#########--- Symbol Table ---#########\n")
            listOfKeys = list(input.keys())
            for key in listOfKeys:
                file.write(f"--- {key} ---\n")
                listOfSubKeys = list(input[key].keys())
                for subKey in listOfSubKeys:
                    if subKey != 'vars':
                        file.write(f"-- {subKey} : {input[key][subKey]}\n")
                    else:
                        file.write(f"-- vars:\n")
                        varKeys = list(input[key][subKey])
                        for var in varKeys:
                            file.write(f"--- {var} : {input[key][subKey][var]}\n")
        elif type == "op":
            file.write("#########--- Optimized Pass Three Address Code ---#########\n")
            for key in input:
                file.write(f"-- {key}\n")
                for tac in input[key]:
                    file.write(f"---- {tac}\n")
        else:
            file.write("#########--- ASM LIST ---#########\n")
            for function, ASM in input:
                file.write(f'{function}:\n')
                for instr in ASM:
                    file.write(f'{instr}\n')
        
def checkExtensions(filePath):
    if filePath.endswith('.c'):
        return True

def retrieveFileName(filePath):
    fileName = Path(filePath).stem
    return fileName