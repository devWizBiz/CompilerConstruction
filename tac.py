import copy
import pdb
index = 1
label = 1
tacList = []
tacDict = {}
variableCounter = 1

def generateTAC(abstractSyntaxTree, symbolTable):
    astProg = abstractSyntaxTree['Program']
    for key in astProg:
        functionStatements = astProg[key]
        for statement in functionStatements:
            if statement[0][0][0] == 'conditional':
                global label
                condition, ifBranch, elseBranch = statement[:]
                
                ifLabel = f"L{label}"
                label += 1
                elseLabel = f"L{label}"
                label += 1
                endLabel = f"L{label}"
                label += 1

                op, left, right = condition[0][-1]
                tacList.append((f"if {left} {op} {right}", "goto", ifLabel))
                tacList.append(("goto", elseLabel))

                tacList.append((ifLabel,))
                for statement in ifBranch:
                    processStatement(statement)

                tacList.append(("goto", endLabel))

                tacList.append((elseLabel,))
                for statement in elseBranch:
                    processStatement(statement)

                tacList.append((endLabel,))
            else:
                if statement[0] == 'return':
                    tacList.append((statement[0], statement[-1][0]))
                elif statement[0] == 'declaration':
                    tacList.append((statement[1], statement[-1][0]))
                elif statement[0] in ['assignment', 'declarationAssignment'] and len(statement[-1]) <= 4:
                    if len(statement[-1]) == 2:
                        tacList.append((statement[-1][0], statement[-1][1]))
                    elif len(statement[-1]) == 4:
                        tacList.append((statement[-1][0], statement[-1][2], statement[-1][1], statement[-1][3]))
                else:
                    resultVariable, final_index = processTree(statement[-1], index, key, symbolTable)

        copyOfTacList = copy.deepcopy(tacList)
        tacDict.update({key : copyOfTacList})
        tacList.clear()
    cfgDict = generateCFG(tacDict)
    return tacDict, symbolTable
    
def processStatement(statement):
    if len(statement) == 2:
        tacList.append((statement[0], statement[1]))
    elif len(statement) == 3:
        if statement[1] != 'assignment':
            tacList.append((statement[1], statement[2]))
        else:
            tacList.append((statement[2]))
    else:
        tacList.append(tuple(statement))

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
        if left in symbolTable[key]['vars']:
            leftType = symbolTable[key]['vars'][left]
        elif left in symbolTable:
            leftType = symbolTable[key]
        else:
            leftType = checkType(left, symbolTable)
            
        # Right Check
        if right in symbolTable[key]['vars']:
            rightType = symbolTable[key]['vars'][right]
        elif right in symbolTable:
            rightType = symbolTable[key]
        else:
            rightType = checkType(right, symbolTable)
            
        # Compare Both
        if leftType == rightType:
            symbolTable[key]['vars'].update({tempVar : leftType})
            tacList.append((tempVar, left, token, right))
        else:
            raise SyntaxError("Mismatch Types")

        return tempVar, index
    else:
        return token, index

# -------- WIP --------------
def generateCFG(tacDict):
    cfgDict = {}

    return cfgDict

def checkType(value, symbolTable): # TODO: Refactor checkType
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