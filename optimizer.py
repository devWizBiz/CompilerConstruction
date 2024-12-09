import pdb

class Optimizer:
    def __init__(self, tacList, symbolTable, optimizations):
        self.tacList = tacList
        self.symbolTable = symbolTable
        self.constProp = optimizations[0]
        self.constFold = optimizations[1]
        self.deadCode = optimizations[2]
        self.optimizedTAC = {}
        self.varDict = {}

        # Process the basic blocks for optimization
        self.optimize()

    """
    Apply optimizations to the basic blocks.
    """
    def optimize(self):
        for key in self.tacList:
            tacList = self.tacList[key]
            tacList = self.simplifyBlock(tacList, key)
            self.optimizedTAC[key] = tacList

    """
    Used to see when we stop see change within the block
    """
    def simplifyBlock(self, tacList, name):
        isChanged = True

        if self.deadCode: # Remove dead code at the beginning
            newTacList = self.useDeadCodeElimination(tacList, name)
            if newTacList != tacList:
                tacList = newTacList
                isChanged = True

        while isChanged:
            isChanged = False

            if self.constProp:
                newTacList = self.useConstantPropagation(tacList, name)
                if newTacList != tacList:
                    tacList = newTacList
                    isChanged = True
                    

            if self.constFold:
                newTacList = self.useConstantFolding(tacList, name)
                if newTacList != tacList:
                    tacList = newTacList
                    isChanged = True

        if self.deadCode: # Remove dead code at the end after Propagation/Folding used
            newTacList = self.useDeadCodeElimination(tacList, name)
            if newTacList != tacList:
                tacList = newTacList

        return tacList

    """
        O1: Constant Propagation
    """
    def useConstantPropagation(self, tacList, name):
        newTacList = []
        varDict = {}
        for tac in tacList:
            if len(tac) == 3 and tac[1] == '=':  # Assignment
                var, assign, value = tac
                valueType = self.checkType(value, name)

                if valueType in ['int', 'float']:
                    newTac = (value, assign, value) # Set left var to constant
                    varDict[var] = value
                else:
                    if value in varDict:
                        newTac = (var, assign, varDict[value] )
                        varDict[var] = varDict[value]
                    else:
                        newTac = tac # Keep old value and move on
            elif len(tac) == 2:
                right = tac[1]
                if right in varDict:
                    newTac = (tac[0], varDict[right])
                else:
                    newTac = tac # Keep old value and move on
            elif len(tac) == 3 and tac[0] == 'if':
                left, comp, right = tac[1]
                if left in varDict:
                    left = varDict[left]

                if right in varDict:
                    right = varDict[right]
                newTac = (tac[0], (left, comp, right), tac[2])
            elif len(tac) == 5:
                result, assign, left, op, right = tac
                
                if result in varDict: # Reassignment, fold must happen first!
                    varDict.pop(result)
                    newTac = tac
                else:                
                    if left in varDict:
                        left = varDict[left]

                    if right in varDict:
                        right = varDict[right]
                    newTac = (result, assign, left, op, right)
            else:
                newTac = tac
            
            newTacList.append(newTac)

        return newTacList

    """
        O2: Constant Folding
    """
    def useConstantFolding(self, tacList, name):
        newTacList = []

        for tac in tacList:
            if len(tac) == 5 and tac[3] in {'+', '-', '*', '/'}:
                result, assign, left, op, right = tac

                leftType = self.checkType(left, name)
                rightType = self.checkType(right, name)

                if leftType == 'id':
                    newTacList.append(tac)
                    continue

                if rightType == 'id':
                    newTacList.append(tac)
                    continue

                resultVal = eval(f'{left} {op} {right}')
                newTacList.append((result, assign, str(resultVal)))
            else:
                newTacList.append(tac) # Just care for operators, all other statements can just be appended

        return newTacList

    """
        O3: Dead Elimination
    """
    def useDeadCodeElimination(self, tacList, name):
        newTacList = []
        
        # Return if there is only one line
        if len(tacList) == 1:
            return tacList

        for index in range(len(tacList)):
            result = None
            left = None
            right = None
            varUsed = 0
            indexedTAC = tacList[index]
            if len(indexedTAC) == 2:
                varToCheck = indexedTAC[1]
            elif len(indexedTAC) == 3 and indexedTAC[0] != 'if' and isinstance(indexedTAC, tuple):
                varToCheck = indexedTAC[0]
            elif len(indexedTAC) == 3 and indexedTAC[0] == 'if':
                newTacList.append(indexedTAC)
                continue           
            elif len(indexedTAC) == 5:
                varToCheck = indexedTAC[0]
            else:
                newTacList.append(indexedTAC)
                continue           

            varType = self.checkType(varToCheck, name)
            if varType != 'id' and indexedTAC[0] not in ['return', 'if']:
                # Constant Prop took place
                continue
            elif index == len(tacList) - 1:
                newTacList.append(indexedTAC)
                continue

            for secondary in range(index + 1, len(tacList)):
                tac = tacList[secondary]
                if len(tac) == 2:
                    right = tac[1]
                elif len(tac) == 3 and tac[0] != 'if' and isinstance(tac, tuple):
                    left, assign, right = tac
                elif len(tac) == 3 and tac[0] == 'if':
                    left, comp, right = tac[1]
                elif len(tac) == 5:
                    result, assign, left, op, right = tac
                else:
                    newTacList.append(tacList[index]) # Label
                    break

                if left is not None:
                    leftType = self.checkType(left, name)
                    if leftType == 'id':
                        if varToCheck == left:
                            varUsed += 1
                            newTacList.append(tacList[index])
                            break

                if right is not None:
                    rightType = self.checkType(right, name)
                    if rightType == 'id':
                        if varToCheck == right:
                            varUsed += 1
                            newTacList.append(tacList[index])
                            break

                if result is not None:
                    resultType = self.checkType(result, name)
                    if resultType == 'id':
                        if varToCheck == result:
                            varUsed += 1
                            newTacList.append(tacList[index])
                            break
        return newTacList

    """
    Ensure we are just checking identifiers
    """
    def checkType(self, val, key):
        if val in self.symbolTable[key]['vars']: # Function Scope
            return 'id'
        elif val in self.symbolTable: # Global Scope
            return 'id'
        else: # INTEGER_CONSTANT or FLOAT_CONSTANT
            if '.' in val:
                return 'float'
            else:
                return 'int'
