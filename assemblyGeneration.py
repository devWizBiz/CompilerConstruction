class asmGenerator():
    def __init__(self, tac, symbolTable, tokens):
        self.tac = tac
        self.symbolTable = symbolTable
        self.tokens = tokens
        self.asmList = []
        
        self.generate()
    
    def generate(self):
        for func in self.tac:
            asm = self.functionGeneration(func)
            self.asmList.extend(asm)

    def functionGeneration(self, func):
        asmList = self.generatePrelude(func)
        registers = ['rax', 'rbx', 'rcx', 'rdx']
        for funcName, basicNumber, tacList in self.tac[func]:
            registerUsed = 0
            for tac in tacList:
                if tac[0] == 'return':
                    value = tac[1]
                    valueChecked = self.checkValueType(value)
                    if valueChecked not in ['INTEGER_CONSTANT', 'FLOATING_CONSTANT']:
                        value = self.symbolTable[func]['vars'][tac[1]]

                    postludeTup = self.generatePostlude()
                    asmList.append(('mov', registers[registerUsed], value))
                    asmList.append(postludeTup)
                    asmList.append(('ret'))
                elif len(tac) == 3 and tac[0] != 'if': # Assignment
                    left, assign, right = tac
                    left = self.symbolTable[func]['vars'][left]
                    valueChecked = self.checkValueType(right)

                    if valueChecked not in ['INTEGER_CONSTANT', 'FLOATING_CONSTANT']:
                        right = self.symbolTable[func]['vars'][right]
                        
                    asmList.append(('mov', left, right))
                elif len(tac) == 5: # Assignment with Op
                    value, assign, left, op, right = tac 
                    
                    valueChecked = self.checkValueType(value)
                    if valueChecked not in ['INTEGER_CONSTANT', 'FLOATING_CONSTANT']:
                        value = self.symbolTable[func]['vars'][value]

                    valueChecked = self.checkValueType(left)
                    if valueChecked not in ['INTEGER_CONSTANT', 'FLOATING_CONSTANT']:
                        left = self.symbolTable[func]['vars'][left]

                    valueChecked = self.checkValueType(right)
                    if valueChecked not in ['INTEGER_CONSTANT', 'FLOATING_CONSTANT']:
                        right = self.symbolTable[func]['vars'][right]
                        
                    if op == '+':
                        op = 'add'
                    elif op == '-':
                        op = 'sub'
                    elif op == '*':
                        op = 'mul'
                    elif op == '/':
                        op = 'div'
                        
                    tmpList = [ ('mov', 'rax', left),
                                ('mov', 'rbx', right),
                                (op, 'rax', 'rbx'),
                                ('mov', value, 'rax')]
                    asmList.extend(tmpList)
                else:
                    asmList.append(tac)
        return asmList

    def generatePrelude(self, func):
        numberOfBytes = self.findTotalNumberOfBytes(func)
        if numberOfBytes == 0:
            preludeList = [(f'{func}:', ('mov', 'rsp', 'rbp'))]
        else:
            preludeList = [(f'{func}:', ('mov', 'rsp', 'rbp')),
                                        ('sub', 'rsp', str(numberOfBytes))]
            byteIndex = 4
            for var in self.symbolTable[func]['vars']:
                self.symbolTable[func]['vars'][var] = f'rbp-{byteIndex}'
                byteIndex += 4

        return preludeList
                
    def generatePostlude(self):
        postludeTuple = ('mov', 'rbp', 'rsp')
        return postludeTuple
    
    def findTotalNumberOfBytes(self, func):
        # Each int is 8 bytes, floats?
        return (len(self.symbolTable[func]['vars']) * 8)
    
    def checkValueType(self, searchValue):
        for tokenID in self.tokens:
            token, type, line, column = self.tokens[tokenID].values()
            if searchValue == token:
                return type
