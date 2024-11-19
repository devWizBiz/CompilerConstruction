import pdb
index = 0
label = 1
tacList = []
variableCounter = 1

class TAC:
    def __init__(self):
        self.tactDict = {}

    """
    Assemble the three address code while updating the Symbol Table
    """
    def generateTAC(self, abstractSyntaxTree, symbolTable):
        for key in abstractSyntaxTree:
            self.tactDict[key] = []
            for type, assignment in abstractSyntaxTree[key]['statements']:
                if( assignment not in ['STARTS', 'ENDS']):
                    if len(assignment) == 1:
                        self.tactDict[key].append((type, assignment))
                    elif len(assignment) == 2:
                        left, right = assignment
                        self.tactDict[key].append((left, '=', right))
                    elif len(assignment) == 3:
                        resultVariable, exitingIndex = self.processTree(assignment, index, key, symbolTable)
                        tmpVar, left, operator, right = tacList[0]

                        if type != 'CONDITIONAL':
                            self.tactDict[key].append((tmpVar, '=', left, operator, right))
                        else:
                            self.tactDict[key].append(('CONDITION', tmpVar, '=', left, operator, right))

                        if type == 'RETURN':
                            self.tactDict[key].append(('RETURN', tmpVar))

                        tacList.clear()
                    elif len(assignment) == 4:
                        assign, operator, left, right = assignment
                        self.tactDict[key].append((assign, '=', left, operator, right))
                    elif len(assignment) > 4:
                        resultVariable, exitingIndex = self.processTree(assignment, index + 1, key, symbolTable)
                        for tmpVar, left, operator, right in tacList:
                            self.tactDict[key].append((tmpVar, '=', left, operator, right))
                        self.tactDict[key].append((assignment[0], '=', tmpVar))
                        
                        if type == 'RETURN':
                            self.tactDict[key].append(('RETURN', tmpVar))

                        tacList.clear()  

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