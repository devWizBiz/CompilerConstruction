import pdb

class Optimizer:
    def __init__(self, basicBlocks, symbolTable, optimizations):
        self.basicBlocks = basicBlocks
        self.symbolTable = symbolTable
        self.constProp = optimizations[0]
        self.constFold = optimizations[1]
        self.deadCode = optimizations[2]
        self.optimizedBlocks = {}
        self.varDict = {}

        # Process the basic blocks for optimization
        self.optimize()

    """
    Apply optimizations to the basic blocks.
    """
    def optimize(self):
        for key in self.basicBlocks:
            if len(self.basicBlocks[key]) == 1 and len(self.basicBlocks[key][0][2]) == 1:  # Single three address code case
                name, block, tacList = self.basicBlocks[key][0]
                self.optimizedBlocks[key] = [(name, block, tacList)]
            else:
                # For now, only looking at the first basic block until Flow Control implemented
                name, block, tacList = self.basicBlocks[key][0]
                tacList = self.simplifyBlock(tacList, key)
                self.optimizedBlocks[key] = [(name, block, tacList)] + self.basicBlocks[key][1:]

    """
    Used to see when we stop see change within the block
    """
    def simplifyBlock(self, tacList, name):
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

        if self.deadCode: # Remove dead code at the end of prop/folding
            newTacList = self.useDeadCodeElimination(tacList, name)
            if newTacList != tacList:
                tacList = newTacList
                isChanged = True

        return tacList

    """
        O1: Constant Propagation
    """
    def useConstantPropagation(self, tacList, name):
        varDict = {}
        newTacList = []
        
        for tac in tacList:
            if len(tac) == 3 and tac[1] == '=':  # Assignment
                var, op, value = tac
                value = varDict.get(value, value)
                varDict[var] = value

            # Replace tokens with constant value
            newTac = tuple(varDict.get(token, token) for token in tac)
            newTacList.append(newTac)

        return newTacList


    """
        O2: Constant Folding
    """
    def useConstantFolding(self, tacList, name):
        newTacList = []
        constTable = {}

        for tac in tacList:
            if len(tac) == 5 and tac[3] in {'+', '-', '*', '/'}:
                var, assignment, left, op, right = tac

                try:
                    # Replace with constants
                    left = constTable.get(left, left)
                    right = constTable.get(right, right)

                    # evaluate left / right with operator
                    result = eval(f"{left} {op} {right}")
                    newTac = (var, '=', str(result)) # still an assignment
                    constTable[var] = result
                    newTacList.append(newTac)
                except:
                    newTacList.append(tac)
            else:
                newTacList.append(tac)

        self.varDict.update(constTable)
        return newTacList


    """
        O3: Constant Propagation
    """
    def useDeadCodeElimination(self, tacList, name):
        variablesInUse = []
        newTacList = []

        tacListBackwards = list(reversed(tacList))
        
        for tac in tacListBackwards:
            if len(tac) >= 3 and tac[1] == '=':  # Assignment
                var = tac[0]
                if var in variablesInUse:
                    variablesInUse.append(tac[2])
                    newTacList.insert(0, tac)
                else:
                    continue # Dead Code, do not append to new list
            elif len(tac) >= 2 and tac[0] in {'return'}:  # Return
                if tac[1] in self.symbolTable[name]['vars'] or tac[1] in self.symbolTable['GLOBAL']:
                    variablesInUse.append(tac[1])
                newTacList.insert(0, tac)
            else: # IF
                variablesInUse.append(tac)
                newTacList.insert(0, tac)

        return newTacList

