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
                    resultVariable, final_index = processTree(statement[1], index)

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
    
    return tacDict
    
# Process the tree
def processTree(statementList, index):
    global variableCounter
    token = statementList[index]
    index += 1

    if token in ['+', '-', '*', '/']:
        left, index = processTree(statementList, index)
        right, index = processTree(statementList, index)
        tempVar = f't{variableCounter}'
        variableCounter += 1
        tacList.append(f"{tempVar} = {left} {token} {right}")
        return tempVar, index
    else:
        return token, index
