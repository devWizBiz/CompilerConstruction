# External Libraries
from pathlib import Path
import pprint
import sys

YELLOW = '\033[93m'
RED = '\033[91m'
RESTORE = '\033[0m'

def error(msg):
    sys.stderr.write(f"{RED}ERROR: {RESTORE}{msg}\n")
    
def warning(msg):
    sys.stderr.write(f"{YELLOW}Warning: {RESTORE}{msg}\n")
    
def prettyPrintOutput(input):
    pprint.pprint(input)

def writeToFile(input, fileName):
    with open(fileName, 'w') as file:
        file.write(str(input) + '\n')
        
def checkExtensions(filePath):
    if filePath.endswith('.c'):
        return True

def retrieveFileName(filePath):
    fileName = Path(filePath).stem
    return fileName