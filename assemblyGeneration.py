import pdb
import sys
class asmGenerator():
    def __init__(self, tac, symbolTable, fileName):
        self.tac = tac
        self.symbolTable = symbolTable
        self.fileName = fileName
        self.asmList = []
        
        self.generate()
        
        self.generateASMFile()
    
    def generate(self):
        for func in self.tac:
            asm = self.functionGeneration(func)
            funcASM = (func, asm)
            self.asmList.append(funcASM)

    def functionGeneration(self, func):
        asmList = self.generatePrelude(func)
        for tac in self.tac[func]:
            if tac[0] == 'return':
                value = tac[1]
                
                valueChecked = self.checkValueType(value, self.symbolTable, func)
                if valueChecked not in ['int', 'float']:
                    value = self.symbolTable[func]['vars'][tac[1]]

                postludeTup = self.generatePostlude()
                asmList.append(('mov', 'rax', value))
                asmList.append(postludeTup)
                asmList.append(('ret'))
            elif len(tac) == 3 and tac[0] != 'if' and isinstance(tac,tuple): # Assignment
                left, assign, right = tac
                left = self.symbolTable[func]['vars'][left]
                valueChecked = self.checkValueType(right, self.symbolTable, func)

                if valueChecked not in ['int', 'float']:
                    right = self.symbolTable[func]['vars'][right]
                    
                asmList.append(('mov', left, right))
            elif len(tac) == 5: # Assignment with Op
                value, assign, left, op, right = tac 
                
                valueChecked = self.checkValueType(value, self.symbolTable, func)
                if valueChecked not in ['int', 'float']:
                    value = f'[{self.symbolTable[func]['vars'][value]}]'

                leftChecked = self.checkValueType(left, self.symbolTable, func)
                if leftChecked not in ['int', 'float']:
                    left = f'[{self.symbolTable[func]['vars'][left]}]'

                rightChecked = self.checkValueType(right, self.symbolTable, func)
                if rightChecked not in ['int', 'float']:
                    right = f'[{self.symbolTable[func]['vars'][right]}]'
                    
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
            elif len(tac) == 3 and tac[0] == 'if':
                statement, comparison, goto = tac
                left, comp, right = comparison
                goto, ifLabel, elseStatement, elseLabel = goto

                leftChecked = self.checkValueType(left, self.symbolTable, func)
                if leftChecked not in ['int', 'float']:
                    left = self.symbolTable[func]['vars'][left]

                rightChecked = self.checkValueType(right, self.symbolTable, func)
                if rightChecked not in ['int', 'float']:
                    right = self.symbolTable[func]['vars'][right]

                if comp == '==':
                    comp = 'jne'
                elif comp == '!=':
                    comp = 'je'
                elif comp == '<=':
                    comp = 'jg'
                elif comp == '>=':
                    comp = 'jl'
                    
                tmpList = [ ('mov', 'eax', left),
                            ('cmp', 'eax', right),
                            (comp, f'.{elseLabel}')]
                asmList.extend(tmpList)                    
            else:
                asmList.append(tac)
        return asmList

    def generatePrelude(self, func):
        numberOfBytes = self.findTotalNumberOfBytes(func)
        if numberOfBytes == 0:
            preludeList = [('mov', 'rsp', 'rbp')]
        else:
            preludeList = [('mov', 'rsp', 'rbp'), ('sub', 'rsp', str(numberOfBytes))]
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
    
    def checkValueType(self, val, symbolTable, key):
        if val in symbolTable[key]['vars']: # Function Scope
            return symbolTable[key]['vars'][val]
        elif val in symbolTable: # Global Scope
            return symbolTable[key]
        else: # INTEGER_CONSTANT or FLOAT_CONSTANT
            if '.' in val:
                return 'float'
            else:
                return 'int'

    def generateASMFile(self):
        with open(f'{self.fileName}.asm', 'w') as file:
            file.write(f'section .data\n\nsection .text\n')
            for function in self.asmList:
                file.write(f'    global {function[0]}\n')
                
            file.write('\n')
                
            for function, ASM in self.asmList:
                file.write(f'{function}:\n')
                for instr in ASM:
                    if isinstance(instr, tuple) and len(instr) == 3:
                        left, mid, right = instr
                        file.write(f'{left} {mid} {right}\n')
                    elif isinstance(instr, tuple) and len(instr) == 2:
                        left, right = instr
                        file.write(f'{left} {right}\n')
                    else:
                        if instr[0] == 'L': # Label
                            file.write(f'.{instr}\n')
                        else:                            
                            file.write(f'{instr}\n')
                file.write('\n')