import copy
import pdb
index = 1  # Start after var
tacList = []
tacDict = {}
variableCounter = 1

def generateTAC(abstractSyntaxTree, symbolTable):
    for key in abstractSyntaxTree['Program']:
        if isinstance(abstractSyntaxTree['Program'][key], dict):
            for statement in abstractSyntaxTree['Program'][key]['statements']:
                statementLength = len(statement[1])
                if statement[0] == 'assignment' and statementLength > 4:
                    resultVariable, final_index = processTree(statement[1], index, key, symbolTable)

                    # Assign the final result to the variable
                    tacList.append(f"{statement[1][0]} = {resultVariable}")
                elif statement[0] == 'assignment' and statementLength <= 4:
                    
                    if statementLength == 2:
                        tacList.append(f"{statement[1][0]} = {statement[1][1]}")
                    elif statementLength == 4:
                        tacList.append(f"{statement[1][0]} = {statement[1][2]} {statement[1][1]} {statement[1][3]}")
                elif statement[0] == 'return':
                    tacList.append(f"{statement[0]} {statement[1][0]}")

            copyOfTacList = copy.deepcopy(tacList)
            tacDict.update({key : copyOfTacList})
            tacList.clear()
    
    return tacDict, symbolTable
    
# Process the tree
def processTree(statementList, index, key, symbolTable):
    global variableCounter
    token = statementList[index]
    index += 1

    if token in ['+', '-', '*', '/']:
        left, index = processTree(statementList, index, key, symbolTable)
        right, index = processTree(statementList, index, key, symbolTable)
        tempVar = f't{variableCounter}'
        variableCounter += 1
        
        # Confirm types
        # Left Check
        if left in symbolTable['Global(s)'][key]['vars'] or left in symbolTable['Global(s)']:
            leftType = symbolTable['Global(s)'][key]['vars'][left]
        else:
            leftType = checkType(left)
            
        # Right Check
        if right in symbolTable['Global(s)'][key]['vars'] or left in symbolTable['Global(s)'][key]:
            rightType = symbolTable['Global(s)'][key]['vars'][right]
        else:
            rightType = checkType(right)
            
        # Compare Both
        if leftType == rightType:
            symbolTable['Global(s)'][key]['vars'].update({tempVar : leftType})
            tacList.append(f"{tempVar} = {left} {token} {right}")
        else:
            raise SyntaxError("Mismatch Types")

        return tempVar, index
    else:
        return token, index


def checkType(value):
    try:
        int(value)
        return "int"
    except ValueError:
        pass  # Not an integer

    try:
        float(value)
        return "float"
    except ValueError:
        pass  # Not a float

    return "str"