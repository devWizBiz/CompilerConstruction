# External Libraries
import pdb
# Internal Libraries
# N/A

index = 0
tacList = []
variableCounter = 1
label = 1

class TAC:
    def __init__(self):
        self.tactDict = {}
        self.basicBlockDict = {}

    """
    Assemble the three address code while updating the Symbol Table
    """
    def generateTAC(self, abstractSyntaxTree, symbolTable):
        
        self.addLabels(abstractSyntaxTree)
        
        global index
        ifLabel = ""
        for key in abstractSyntaxTree:
            self.tactDict[key] = []
            for var, assignment, expression in abstractSyntaxTree[key]['statements']:
                    if var not in ['if', None]:
                        if isinstance(expression, tuple) and len(expression) > 3:
                            resultVariable, finalIndex = self.processTree(expression, index, key, symbolTable)
                            for tmpVar, left, op, right in tacList:
                                self.tactDict[key].append((tmpVar, '=', left, op, right))
                            tacList.clear()
                            self.tactDict[key].append((var, '=', tmpVar))
                        else:
                            if isinstance(expression, tuple):
                                op, left, right = expression
                                self.tactDict[key].append((var, '=', left, op, right))
                            elif expression is not None:
                                self.tactDict[key].append((var, '=', expression))
                            else:
                                self.tactDict[key].append((var))
                    elif assignment == 'return':
                        if isinstance(expression, tuple):
                            resultVariable, finalIndex = self.processTree(expression, index, key, symbolTable)
                            for tmpVar, left, op, right in tacList:
                                self.tactDict[key].append((tmpVar, '=', left, op, right))
                            tacList.clear()
                            self.tactDict[key].append(('return', tmpVar))
                        else:
                            self.tactDict[key].append(('return', expression))
                    else:
                        self.tactDict[key].append((var, assignment, expression))

        self.generateBasicBlocks()

    """
    Process the tree to include the new tempVariables and correct order of operations
    """
    def processTree(self, statementList, index, key, symbolTable):
        
        global variableCounter
        token = statementList[index]
        index += 1

        if token in ['+', '-', '*', '/', '==', '!=', '<', '<=', '>', '>=']:
            left, index = self.processTree(statementList, index, key, symbolTable)
            right, index = self.processTree(statementList, index, key, symbolTable)
            tempVar = f't{variableCounter}'
            variableCounter += 1
            
            # Confirm types
            # Left Check
            leftType = self.checkType(left, key, symbolTable)
                
            # Right Check
            rightType = self.checkType(right, key, symbolTable)
                
            # Compare Both
            if leftType == rightType:
                symbolTable[key]['vars'].update({tempVar : leftType})
                tacList.append((tempVar, left, token, right))
            else:
                raise SyntaxError("Mismatch Types")

            return tempVar, index
        else:
            return token, index
    
    """
    Ensure the types match
    """
    def checkType(self, val, key, symbolTable):

        if val in symbolTable[key]['vars']: # Function Scope
            return symbolTable[key]['vars'][val]
        elif val in symbolTable: # Global Scope
            return symbolTable[key]
        else: # INTEGER_CONSTANT or FLOAT_CONSTANT
            if '.' in val:
                return 'float'
            else:
                return 'int'
            
    """
    Add appropriate labeling for conditionals
    """
    def addLabels(self, ast):
        global label
        listOfLabels = []
        listOfStatements = []
        for key in ast:
            for statement in ast[key]['statements']:
                if statement[0] == 'CONDITION':
                    ifLabel = f'L{label}'
                    elseLabel = f'L{label + 1}'
                    label += 2

                    listOfLabels.append(ifLabel)
                    listOfLabels.append(elseLabel)

                    listOfStatements.append(('if', statement[-1], ('goto', ifLabel, 'else', elseLabel)))
                    listOfStatements.append((f'{ifLabel}:', None, None))
                    listOfLabels.remove(ifLabel)
                elif statement[0] in ['IF END', 'ELSE START']:
                    if len(listOfLabels) > 0:
                        lastLabel = listOfLabels.pop()
                        listOfStatements.append((f'{lastLabel}:', None, None))
                    else:
                        continue
                else:
                    listOfStatements.append(statement)

            ast[key]['statements'] = list(listOfStatements)
            listOfStatements.clear()
    
    """
    Generate Basic Blocks from the three address code
    """
    def generateBasicBlocks(self):
        
        blockCount = 1
        for key in self.tactDict:
            self.basicBlockDict[key] = []
            blockName = key
            basicBlock = []
            for tac in self.tactDict[key]:
                if isinstance(tac, tuple):
                    basicBlock.append(tac)
                else:
                    self.basicBlockDict[key].append((blockName, f'B{blockCount}', list(basicBlock)))
                    blockName = tac[:-1]
                    basicBlock.clear()
                    blockCount += 1
            else:
                self.basicBlockDict[key].append((blockName, f'B{blockCount}', list(basicBlock)))
