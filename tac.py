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
                if statement[0] == 'assignment':
                    traversal_list = statement[1]
                        
                    # Process the expression starting from index 1
                    result_var, final_index = processTree(traversal_list, index)

                    # Assign the final result to the variable
                    tacList.append(f"{traversal_list[0]} = {result_var}")

            copyOfTacList = copy.deepcopy(tacList)
            tacDict.update({key : copyOfTacList})
            tacList.clear()
    
    return tacDict
    
# Process the tree
def processTree(traversal_list, index):
    global variableCounter
    token = traversal_list[index]
    index += 1

    if token in ['+', '-', '*', '/']:
        left, index = processTree(traversal_list, index)
        right, index = processTree(traversal_list, index)
        tempVar = f't{variableCounter}'
        variableCounter += 1
        tacList.append(f"{tempVar} = {left} {token} {right}")
        return tempVar, index
    else:
        return token, index
