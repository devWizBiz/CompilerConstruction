# External Libraries
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
        pprint.pprint(input, file)
        
def checkExtensions(filePath):
    if filePath.endswith('.c'):
        return True

def retrieveFileName(filePath):
    fileName = filePath.split('\\')[-1].split('.')[0] # Windows Pathing
    if ( fileName != '' ):
        return fileName
    else:
        return filePath.split('/')[-1].split('.')[0] # Linux Pathing     
