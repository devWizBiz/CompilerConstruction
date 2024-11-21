# External Libraries
import re
import sys
import pdb

# Internal Libraries
import support

class Helper:
    def __init__(self, tokens, tokenIndex):
        self.Tokens = tokens
        self.TokenIndex = tokenIndex
        self.SavedIndex = tokenIndex
    
    """
        Increment Token Index
    """
    def incrementIndex(self):
        self.TokenIndex += 1

    """
        Set Save Index
    """
    def saveIndex(self, index):
        self.SavedIndex = index

    """
        Set Token Index
    """
    def setIndex(self, index):
        self.TokenIndex = index

    """
        Update the index for Token and Save index
    """
    def updateIndex(self, index):
        self.setIndex(index)
        self.saveIndex(index)

    """
        Get a single token
    """
    def getToken(self):
        token = self.Tokens.get(self.TokenIndex)
        self.incrementIndex()
        return token

    """
        Get N number of Tokens
    """
    def getTokens(self, numberOfTokens):
        return [self.getToken() for _ in range(numberOfTokens)]        

    """
        Look at the next token, no increment
    """
    def peekNextToken(self):
        token = self.Tokens.get(self.TokenIndex)
        if token is not None:
            token = token['TOKEN']
            return token
        
        return None
        
    """
        Any checks for any statements, functions are here
    """
    def getExpectedMatch(self, toMatch):
        if toMatch == 'FUNCTION_DECLARATION':
            expectedMatch =  [
                    ('TOKEN', {'int', 'float', 'void'}),  # [int|float|void]
                    ('TYPE', {'IDENTIFIER'}),             # IDENTIFIER
                    ('TOKEN', {'('}),                     # (
                    ('TOKEN', {')'}),                     # )
                    ('TOKEN', {'{'})                      # {
                ]
        elif toMatch == 'DECLARATION_ASSIGNMENT':
            expectedMatch = [
                    ('TOKEN', {'int','float'}), # [int|float]
                    ('TYPE', {'IDENTIFIER'}),   # IDENTIFIER
                    ('TOKEN', {'='})            # =
                ]
        elif toMatch == 'DECLARATION':
            expectedMatch = [
                    ('TOKEN', {'int','float'}), # [int|float]
                    ('TYPE', {'IDENTIFIER'}),   # IDENTIFIER
                    ('TOKEN', {';'})            # ;
                ]
        elif toMatch == 'ASSIGNMENT':
            expectedMatch = [
                    ('TYPE', {'IDENTIFIER'}),   # IDENTIFIER
                    ('TOKEN', {'='})            # =
                ]
        elif toMatch == 'RETURN':
            expectedMatch = [
                    ('TOKEN', {'return'})       # return
                ]
        elif toMatch == 'IF':
            expectedMatch = [
                    ('TOKEN', {'if'})           # if
                ]
        elif toMatch == 'ELSE':
            expectedMatch = [
                    ('TOKEN', {'else'})         # else
                ]
        elif toMatch == 'CONDITION':
            expectedMatch = [
                    ('TOKEN', {'('}),           # (
                    ('TYPE', {'IDENTIFIER','INTEGER_CONSTANT', 'FLOATING_CONSTANT'}),   # [IDENTIFIER|INTEGER_CONSTANT|FLOATING_CONSTANT]
                    ('TOKEN', {'==', '!=', '<', '<=', '>', '>='}),                      # [==, !=, <, <=, >, >=]
                    ('TYPE', {'IDENTIFIER','INTEGER_CONSTANT', 'FLOATING_CONSTANT'}),   # [IDENTIFIER|INTEGER_CONSTANT|FLOATING_CONSTANT]
                    ('TOKEN', {')'}),           # )
                ]
        else:
            return None

        return expectedMatch

    """
        Check tokens for match with the expected match
    """
    def checkTokensForMatch(self, allTokens, expectedMatch):
        tokensToCheck = []
        # Always use Type for IDENTIFIER
        for token in allTokens:
            if token['TYPE'] == 'IDENTIFIER':
                tokensToCheck.append(token['TYPE'])
            else:
                tokensToCheck.append(token['TOKEN'])
                
        validMatch = all(tokensToCheck[i] in values for i, (key, values) in enumerate(expectedMatch))
        return validMatch
    
    """
        Flatten out tuples of expressions
    """
    def flattenTuple(self, expression):
        listOfElements = []
        for item in expression:
            if isinstance(item, tuple): 
                listOfElements.extend(self.flattenTuple(item))
            else:
                listOfElements.append(item)
        return tuple(listOfElements)

    """
        Flatten out list for conditionals
    """
    def flattenList(self, allStatements):
        listOfElements = []
        for item in allStatements:
            if isinstance(item, list): 
                listOfElements.extend(self.flattenList(item))
            else:
                listOfElements.append(item)
        return listOfElements


class Parser:
    def __init__(self, tokens):
        self.ProgramHelp = Helper(tokens, 0)

    """
        Parse Program
    """
    def parseProgram(self):
        programHelper = self.ProgramHelp
        symbolTable = SymbolTable()
        abstractSyntaxTree = AbstractSyntaxTree()
        
        while programHelper.peekNextToken() is not None:
            tokens, tokenIndex = programHelper.Tokens, programHelper.TokenIndex
            helper, allInfo = self.parseFunction(tokens, tokenIndex) # or self.parseGlobal
            
            if helper is None:
                helper, allInfo = self.parseGlobal(tokens, tokenIndex)
                symbolTable.addGlobal(allInfo[0], allInfo[1])
                programHelper.updateIndex(helper.TokenIndex)
                continue
                
            if helper is not None: # Symbol Table and AbstractSyntaxTree gets Checked
                type, id, allStatements = allInfo
                symbolTable.addDeclarations(type, id, allStatements)
                abstractSyntaxTree.addStatements(type, id, allStatements)
                # Update the program scopes indexes
                programHelper.updateIndex(helper.TokenIndex)
            else:
                token, type, line, column = programHelper.getToken().values()
                support.error(f'Cannot match token found at LINE {line} COLUMN {column}: {token}')
                sys.exist(1)
        
        return symbolTable, abstractSyntaxTree

    """
        Parse Function
    """
    def parseFunction(self, tokens, tokenIndex):
        functionHelper = Helper(tokens, tokenIndex)

        functionExpected = functionHelper.getExpectedMatch('FUNCTION_DECLARATION')
        functionTokens = functionHelper.getTokens(len(functionExpected))
        isFunctionValid = functionHelper.checkTokensForMatch(functionTokens, functionExpected)
        
        type = functionTokens[0]['TOKEN']
        id = functionTokens[1]['TOKEN']
        
        if isFunctionValid:
            statementHelper, allStatements = self.parseStatements(tokens, functionHelper.TokenIndex)
            
            if allStatements:
                allStatements = functionHelper.flattenList(allStatements)

                # Update saved index
                functionHelper.updateIndex(statementHelper.TokenIndex)
                return functionHelper, (type, id, allStatements)

        return None, None

    """
        Parse Global
    """
    def parseGlobal(self, tokens, tokenIndex):
        globalHelper = Helper(tokens, tokenIndex)
        helper, statement = self.parseDeclaration(tokens, globalHelper.TokenIndex)

        if helper:
            globalHelper.updateIndex(helper.TokenIndex)
            return helper, statement
        
        return None, None

    """
        Parse all statements in function
    """
    def parseStatements(self, tokens, tokenIndex):
        statementsHelper = Helper(tokens, tokenIndex)
        allStatements = []
        while statementsHelper.peekNextToken() != '}': # Closing brace of function
            helper, statement = self.parseDeclaration(tokens, statementsHelper.TokenIndex) 
            
            if statement is None:
                helper, statement = self.parseDeclarationAssignment(tokens, statementsHelper.TokenIndex)
            
            if statement is None:
                helper, statement = self.parseAssignment(tokens, statementsHelper.TokenIndex)

            if statement is None:
                helper, statement = self.parseReturn(tokens, statementsHelper.TokenIndex)

            if statement is None:
                helper, statement = self.parseConditional(tokens, statementsHelper.TokenIndex)

            if statement is not None:
                allStatements.append(statement)

            if helper:
                statementsHelper.updateIndex(helper.TokenIndex)
        
        if len(allStatements) == 0:
            return None, None

        statementsHelper.getToken() # Burn }
        return statementsHelper, allStatements

    """
        Parse Declaration
    """
    def parseDeclaration(self, tokens, tokenIndex):
        declarationHelper = Helper(tokens, tokenIndex)

        declarationExpected = declarationHelper.getExpectedMatch('DECLARATION')
        declarationTokens = declarationHelper.getTokens(len(declarationExpected))
        isDeclarationValid = declarationHelper.checkTokensForMatch(declarationTokens, declarationExpected)
        
        type = declarationTokens[0]['TOKEN']
        id = declarationTokens[1]['TOKEN']

        if isDeclarationValid:
            declarationHelper.saveIndex(declarationHelper.TokenIndex)
            return declarationHelper, (type, id, None, None)
            
        return None, None
            
    """
        Parse Declaration Assignment
    """                   
    def parseDeclarationAssignment(self, tokens, tokenIndex):
        decAssignmentHelper = Helper(tokens, tokenIndex)

        decAssignmentExpected = decAssignmentHelper.getExpectedMatch('DECLARATION_ASSIGNMENT')
        decAssignmentTokens = decAssignmentHelper.getTokens(len(decAssignmentExpected))
        isDecAssignmentValid = decAssignmentHelper.checkTokensForMatch(decAssignmentTokens, decAssignmentExpected)
        
        type = decAssignmentTokens[0]['TOKEN']
        id = decAssignmentTokens[1]['TOKEN']
        
        if isDecAssignmentValid:
            expression = self.parseExpression( decAssignmentHelper )
            decAssignmentHelper.saveIndex(decAssignmentHelper.TokenIndex)

            if expression is not None and decAssignmentHelper.peekNextToken() == ';':
                decAssignmentHelper.getToken() # Consume ';'
                return decAssignmentHelper, (type, id, '=', expression)

        return None, None
    
    """
        Parse Assignment
    """
    def parseAssignment(self, tokens, tokenIndex):
        assignmentHelper = Helper(tokens, tokenIndex)

        assignmentExpected = assignmentHelper.getExpectedMatch('ASSIGNMENT')
        assignmentTokens = assignmentHelper.getTokens(len(assignmentExpected))
        isAssignmentValid = assignmentHelper.checkTokensForMatch(assignmentTokens, assignmentExpected)
        
        id = assignmentTokens[0]['TOKEN']
        
        if isAssignmentValid:
            expression = self.parseExpression( assignmentHelper )
            assignmentHelper.saveIndex(assignmentHelper.TokenIndex)

            if expression is not None and assignmentHelper.peekNextToken() == ';':
                assignmentHelper.getToken() # Consume ';'
                return assignmentHelper, (None, id, '=', expression)

        return None, None        

    """
        Parse Return
    """
    def parseReturn(self, tokens, tokenIndex):
        returnHelper = Helper(tokens, tokenIndex)

        returnExpected = returnHelper.getExpectedMatch('RETURN')
        returnTokens = returnHelper.getTokens(len(returnExpected))
        isReturnValid = returnHelper.checkTokensForMatch(returnTokens, returnExpected)
        
        returnType = returnTokens[0]['TOKEN']

        if isReturnValid:
            expression = self.parseExpression( returnHelper )
            returnHelper.saveIndex(returnHelper.TokenIndex)

            if expression is not None and returnHelper.peekNextToken() == ';':
                returnHelper.getToken() # Consume ';'
                return returnHelper, (None, None, returnType, expression)
            
        return None, None

    """
        Parse Conditional
    """
    def parseConditional(self, tokens, tokenIndex):
        conditionalHelper = Helper(tokens, tokenIndex)
        allStatements = []
        
        ifExpected = conditionalHelper.getExpectedMatch('IF')
        ifToken = conditionalHelper.getTokens(len(ifExpected))
        ifValid = conditionalHelper.checkTokensForMatch(ifToken, ifExpected)
        
        if ifValid:
            conditionExpected = conditionalHelper.getExpectedMatch('CONDITION')
            conditionToken = conditionalHelper.getTokens(len(conditionExpected))
            conditionValid = conditionalHelper.checkTokensForMatch(conditionToken, conditionExpected)
            
            conditionStatement = ('CONDITION', conditionToken[1]['TOKEN'], conditionToken[2]['TOKEN'], conditionToken[3]['TOKEN'])
            allStatements.append(conditionStatement)
            
            if conditionValid:
                conditionalHelper.getToken() # Burn {
                helper, ifStatements = self.parseStatements(tokens, conditionalHelper.TokenIndex)
                ifStatements.append(('IF END', None, None, None))

                if helper:
                    allStatements.append(ifStatements)
                    conditionalHelper.updateIndex(helper.TokenIndex)
        else:
            conditionalHelper.setIndex(conditionalHelper.SavedIndex)

        elseExpected = conditionalHelper.getExpectedMatch('ELSE')
        elseToken = conditionalHelper.getTokens(len(elseExpected))
        elseValid = conditionalHelper.checkTokensForMatch(elseToken, elseExpected)

        if elseValid:
                conditionalHelper.getToken() # Burn {
                helper, elseStatements = self.parseStatements(tokens, conditionalHelper.TokenIndex)
                elseStatements.insert(0, ('ELSE START', None, None, None))

                if helper:
                    allStatements.append(elseStatements)
                    conditionalHelper.updateIndex(helper.TokenIndex)
        else:
            conditionalHelper.setIndex(conditionalHelper.SavedIndex)            
            
        if ifValid or elseValid:
            return conditionalHelper, allStatements

        return None, None
            
    """
    Expr -> Term | Expr + Term | Expr - Term
    """
    def parseExpression(self, helper):
        expression = self.parseTerm(helper)

        while helper.peekNextToken() in ['+', '-']:
            opToken = helper.getToken()
            term = self.parseTerm(helper)
            expression = (opToken['TOKEN'], expression, term)
        
        if isinstance(expression, tuple):
            # if isinstance(expression[1], tuple):
                expression = helper.flattenTuple(expression)
        
        return expression
    
    """
    Term -> Value | Term * Value | Term / Value
    """
    def parseTerm(self, helper):
        term = self.parseValue(helper)
        
        while helper.peekNextToken() in ['*', '/']:
            opToken = helper.getToken()
            value = self.parseValue(helper)
            term = (opToken['TOKEN'], term, value)
        
        return term
    
    """
    Val -> (Expr) | INTEGER/FLOAT | IDENTIFIER | - Value
    """
    def parseValue(self, helper):
        consumedToken = helper.getToken()

        # (Expr)
        if consumedToken['TOKEN'] == '(':
            value = self.parseExpression(helper)
            if helper.peekNextToken() == ')':
                helper.getToken()
                return value

        # INTEGER/FLOAT Constant
        elif consumedToken['TYPE'] in ['INTEGER_CONSTANT', 'FLOATING_CONSTANT']:
            return (consumedToken['TOKEN'])

        # IDENTIFIER
        elif consumedToken['TYPE'] == 'IDENTIFIER':
            return (consumedToken['TOKEN'])

        # - Value
        elif consumedToken['TOKEN'] == '-':
            value = self.parseValue()
            return ('-', None, value)
        
        return None
    
class SymbolTable():
    def __init__(self):
        self.SymbolTableDictionary = {}
        self.SymbolTableDictionary['GLOBAL'] = {}
    
    """
    Add global variable to symbol Table
    """
    def addGlobal(self, type, id):
        if self.existsInTableGlobal(id) == False:
            self.SymbolTableDictionary['GLOBAL'].update({id : type})
            
    """
    Add declarations to symbol Table within scope of function
    """
    def addDeclarations(self, type, key, statements):
        self.SymbolTableDictionary[key] = {'retType' : type, 'params' : None, 'vars' : {} }
        
        for type, id, statement, expression in statements:
            if type in ['int', 'float']:
                if self.existsInTableFunction(key, id) == False:
                    self.SymbolTableDictionary[key]['vars'].update({id : type})
    
    """
    Check for already declared variables within the global scope and function scope
    """    
    def existsInTableFunction(self, key, id):
        if id in self.SymbolTableDictionary[key]['vars'] or id in self.SymbolTableDictionary['GLOBAL']:
            support.error(f'Already Declared {id}')
            sys.exist(1)
        return False

    """
    Check for already declared variables within the global scope
    """  
    def existsInTableGlobal(self, id):
        if id in self.SymbolTableDictionary['GLOBAL']:
            support.error(f'Already Declared {id}')
            sys.exist(1)
        
        return False

        
class AbstractSyntaxTree():
    def __init__(self):
        self.AbstractSyntaxTreeDictionary = {}

    """
    Add statements to the Abstract Syntax Tree Dictionary
    """
    def addStatements(self, type, key, statements):
        self.AbstractSyntaxTreeDictionary[key] = {'statements' : [] }
        
        for type, id, statement, expression in statements:
            if statement is not None and type != 'CONDITION':
                self.AbstractSyntaxTreeDictionary[key]['statements'].append((id, statement, expression))

            if  type in ['CONDITION', 'IF START', 'IF END', 'ELSE START']:
                self.AbstractSyntaxTreeDictionary[key]['statements'].append((type, None, (id, statement, expression)))
