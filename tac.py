import pdb
import parser

tacDic = {}
tempCounter = 1  # Counter for temporary variables
tempList = []

def generateTAC( ast, symbolTable ):
    keyIterator = iter(ast['Program'])
    keyCurrent = next(keyIterator)

    while keyCurrent is not None:
        
        function = ast['Program'][keyCurrent]
        
        if function == []: # No Global Declarations found
            keyCurrent = next(keyIterator, None)
            continue
        
        tacDic[keyCurrent] = []
        for statement in function:
            # For an assign, statement[2] always has the potential of being a nested list
            if statement[0] == 'ASSIGN':
                if isinstance(statement[2], list):
                    generateTACExpressionList(statement[2], keyCurrent)
                    # tacDic[keyCurrent].append([statement[1], '=', tempList])
                else:
                    tacDic[keyCurrent].append([statement[1], '=', statement[2]])

            # For a return, statement[1] always has the potential of being a nested list
            if statement[0] == 'RETURN':
                if isinstance(statement[1], list):
                    generateTACExpressionList(statement[1], keyCurrent)
                else:
                    tacDic[keyCurrent].append([statement[0], statement[1]])

                
        keyCurrent = next(keyIterator, None)

    return tacDic

def generateTACExpressionList(expression, keyCurrent):
    global tempCounter, tempList
    if not keyCurrent in tacDic:
        tacDic[keyCurrent] = []

    if isinstance(expression, list):
        left = expression[0]
        op = expression[1]
        right = expression[2]
        
        if isinstance(left, list):
            tmpLeft = generateTACExpressionList(left, keyCurrent)
        else:
            tmpLeft = left
        
        if isinstance(right, list):
            tmpRight = generateTACExpressionList(right, keyCurrent)
        else:
            tmpRight = right
        
        temp_var = "t" + str(tempCounter)
        tempCounter += 1
        
        tempList.append([temp_var,tmpLeft,op,tmpRight])
        
        return temp_var
    else:
        return expression
