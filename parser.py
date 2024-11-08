import pdb
import re

PARSER_PATTERNS = [
    ('FUNCTION_DECLARATION', r'(void|int|float|char)IDENTIFIER\(\)\{'),
    ('VARIABLE_DECLARATION', r'(int|float|char)IDENTIFIER;'),
    ('VARIABLE_DECLARATION_ASSIGNMENT', r'(int|float|char)IDENTIFIER='),
    ('VARIABLE_ASSIGNMENT', r'IDENTIFIER='),
    ('RETURN', r'return'),
]

# Join the token patterns through the OR operator along with it's sub-pattern name
PATTERNS_COMBINED = '|'.join('(?P<%s>%s)' % pair for pair in PARSER_PATTERNS)
COMPILED_PATTERNS = re.compile(PATTERNS_COMBINED)

class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.value)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.currentTokenIndex = 0

        self.abstractSyntaxTree = {}

        self.symbolTable = {}
        self.symbolTable['Global(s)'] = {}
                
    def getCurrentToken(self):
        currentToken = self.tokens.get(self.currentTokenIndex)
        self.incrementIndex()
        return currentToken
    
    def peekNextToken(self):
        return self.tokens.get(self.currentTokenIndex)
    
    def incrementIndex(self):
        self.currentTokenIndex += 1
    
    def isMatch(self, totalTokens):
        checkForMatch = ""
        for token in totalTokens:
            if token['TYPE'] in ['KEYWORD', 'PUNCTUATORS']:
                checkForMatch += token['TOKEN']
            else:
                checkForMatch += token['TYPE']
                
        # Look for match
        match = COMPILED_PATTERNS.search(checkForMatch)

        return match

    def depthFirstSearch(self, node):
        result = []
        
        def helper(current_node):
            if current_node is None:
                return
            
            try:
                # Append the current value
                result.append(current_node.value)
            except:
                result.append(current_node)
                return result
            
            # Traverse the left and right subtrees
            helper(current_node.left)
            helper(current_node.right)
        
        # Start the helper function
        helper(node)
        
        return result

    def parseProgram(self):
        while self.peekNextToken() is not None:
            
            info = self.parseFunction()
            if info is not None:
                key = next(iter(info.keys()))
                vars = {}

                for statement in info[key]['statements']:
                    if statement[0] == 'declarationAssignment':
                        vars[statement[2][0]] = statement[1]
                    elif statement[0] == 'declaration':
                        vars[statement[2]] = statement[1]

                self.symbolTable[key] = { 'retType' : info[key]['retType'], 'args' : None, 'vars': vars}
                self.abstractSyntaxTree[key] = info[key]['statements']
                continue

            info = self.parseDeclaration()
            if info is not None:
                self.symbolTable['Global(s)'][info[-1]] = info[1]
                continue
            else:
                raise SyntaxError("No valid tokens to use")

        self.abstractSyntaxTree = {"Program": self.abstractSyntaxTree}


    # ['void' | 'int' | 'char' | 'float'] IDENTIFIER () { [statements] }
    def parseFunction(self):
        # Save index if not global variable
        currentIndex = self.currentTokenIndex
        
        # Get five tokens for check
        fiveTokens = [self.getCurrentToken() for _ in range(5)]

        match = self.isMatch(fiveTokens)        
        
        if match is None:
            self.currentTokenIndex = currentIndex
            return None

        # Match found, begin looking for statement(s)
        listOfStatements = []
        while self.peekNextToken() and self.peekNextToken()['TOKEN'] != '}':
            statement = self.parseStatement()
            
            if statement is None:
                statement = self.parseConditional()
                
            if statement is not None:
                if statement[0] in ['declaration', 'declarationAssignment']:
                    statement = (statement[0], statement[1],  tuple(self.depthFirstSearch(statement[2])))
                    listOfStatements.append(statement)
                elif statement[0] in ['assignment',  'return']:
                    statement = ((statement[0]), tuple(self.depthFirstSearch(statement[1])))
                    listOfStatements.append(statement)
                elif statement[0][0] in 'conditional': # TODO: Need to clean this up, probably another function
                    conditionalList = []
                    for condition, treeNode in statement:
                        if isinstance(treeNode, list):
                            tmpList = []
                            for branch in treeNode:
                                if branch[0] in ['declaration', 'declarationAssignment']:
                                    statement = ((condition), branch[1], tuple(self.depthFirstSearch(branch[2])))
                                    tmpList.append(statement)
                                elif branch[0] in ['assignment',  'return']:
                                    statement = ((condition), branch[0], tuple(self.depthFirstSearch(branch[1])))
                                    tmpList.append(statement)
                            conditionalList.append(tmpList)
                        else:
                            statement = ((condition), tuple(self.depthFirstSearch(treeNode)))
                            conditionalList.append([statement])
                    listOfStatements.append(conditionalList)
            else:
                self.currentTokenIndex = currentIndex
                return None
        else: # Function done, create function dictionary and return
            self.getCurrentToken() # Consume '}'
            completedFunction = {fiveTokens[1]['TOKEN']: {'retType': fiveTokens[0]['TOKEN'], 'statements': listOfStatements}}
            return completedFunction

    # 'return' <expression> | 'assignment' <expression> | 'declaration' <expression>
    def parseStatement(self):
        
        statement = self.parseReturn()
        if statement is not None:
            return statement
        
        statement = self.parseDeclaration()
        if statement is not None:
            return statement
        
        statement = self.parseDeclarationAssignment()
        if statement is not None:
            return statement

        statement = self.parseAssignment()
        if statement is not None:
            return statement
        
        return None
    
    # 'return' <expression>
    def parseReturn(self):
        # Save index if not global variable
        currentIndex = self.currentTokenIndex
        
        # Get two tokens for check
        oneTokens = [self.getCurrentToken() for _ in range(1)]
        
        match = self.isMatch(oneTokens)
        
        if match is None or not match.lastgroup == "RETURN":
            self.currentTokenIndex = currentIndex
            return None
        
        expression = self.parseExpression()
        if expression is not None and self.peekNextToken()['TOKEN'] == ';':
            self.getCurrentToken() # Consume ';'
            return ('return', expression)
        else:
            self.currentTokenIndex = currentIndex
            return None
    
    def parseDeclaration(self):
        # Save index if not global variable
        currentIndex = self.currentTokenIndex
        
        # Get three tokens for check
        threeTokens = [self.getCurrentToken() for _ in range(3)]
        
        match = self.isMatch(threeTokens)
        
        if match is None or not match.lastgroup == "VARIABLE_DECLARATION":
            self.currentTokenIndex = currentIndex
            return None
        
        completedDeclaration = ("declaration", threeTokens[0]['TOKEN'], (threeTokens[1]['TOKEN']))
        return completedDeclaration        
    
    def parseDeclarationAssignment(self):
        # Save index if not global variable
        currentIndex = self.currentTokenIndex
        
        # Get three tokens for check
        threeTokens = [self.getCurrentToken() for _ in range(3)]
        
        match = self.isMatch(threeTokens)
        
        if match is None or not match.lastgroup == "VARIABLE_DECLARATION_ASSIGNMENT":
            self.currentTokenIndex = currentIndex
            return None

        expression = self.parseExpression()
        if expression is not None and self.peekNextToken()['TOKEN'] == ';':
            self.getCurrentToken() # Consume ';'
            return ("declarationAssignment", threeTokens[0]['TOKEN'], TreeNode(threeTokens[1]['TOKEN'], expression))
        else:
            self.currentTokenIndex = currentIndex
            return None

    # 'assignment' <expression>    
    def parseAssignment(self):
        # Save index if not global variable
        currentIndex = self.currentTokenIndex
        
        # Get two tokens for check
        twoTokens = [self.getCurrentToken() for _ in range(2)]
        
        match = self.isMatch(twoTokens)
        
        if match is None or not match.lastgroup == 'VARIABLE_ASSIGNMENT':
            self.currentTokenIndex = currentIndex
            return None

        expression = self.parseExpression()
        if expression is not None and self.peekNextToken()['TOKEN'] == ';':
            self.getCurrentToken() # Consume ';'
            return ('assignment', TreeNode(twoTokens[0]['TOKEN'], expression))
        else:
            self.currentTokenIndex = currentIndex
            return None

    # 'if' <conditional expression> [statements] 'else' [statements]
    def parseConditional(self):
        currentIndex = self.currentTokenIndex
        
        ifToken = self.getCurrentToken()
        if ifToken['TOKEN'] != 'if':
            self.currentTokenIndex = currentIndex
            return None

        if self.getCurrentToken()['TOKEN'] != '(':
            self.currentTokenIndex = currentIndex
            return None

        # Parse condition (IDENTIFIER|INTEGER_CONSTANT (comparison operator) IDENTIFIER|INTEGER_CONSTANT)
        condition = self.parseCondition()
        if condition is None:
            self.currentTokenIndex = currentIndex
            return None

        if self.getCurrentToken()['TOKEN'] != ')':
            self.currentTokenIndex = currentIndex
            return None

        if self.getCurrentToken()['TOKEN'] != '{':
            self.currentTokenIndex = currentIndex
            return None

        ifStatements = []
        while self.peekNextToken() and self.peekNextToken()['TOKEN'] != '}':
            statement = self.parseStatement()
            if statement is not None:
                ifStatements.append(statement)
            else:
                self.currentTokenIndex = currentIndex
                return None

        self.getCurrentToken()

        elseStatements = []
        if self.peekNextToken() and self.peekNextToken()['TOKEN'] == 'else':
            self.getCurrentToken()  # Consume 'else'
            
            if self.getCurrentToken()['TOKEN'] != '{':
                self.currentTokenIndex = currentIndex
                return None

            while self.peekNextToken() and self.peekNextToken()['TOKEN'] != '}':
                statement = self.parseStatement()
                if statement is not None:
                    elseStatements.append(statement)
                else:
                    self.currentTokenIndex = currentIndex
                    return None

            self.getCurrentToken()

        return ('conditional', condition), ('if', ifStatements), ('else', elseStatements)


    def parseCondition(self):
        left = self.parseValue()
        if left is None:
            return None

        operatorToken = self.getCurrentToken()
        if operatorToken['TOKEN'] not in ['==', '!=', '<', '<=', '>', '>=']:
            return None

        right = self.parseValue()
        if right is None:
            return None

        return TreeNode(operatorToken['TOKEN'], left, right)

    # Expr -> Term | Expr + Term | Expr - Term
    def parseExpression(self):
        expression = self.parseTerm()

        while self.peekNextToken()['TOKEN'] in ['+', '-']:
            opToken = self.getCurrentToken()
            term = self.parseTerm()
            expression = TreeNode(opToken['TOKEN'], expression, term)
        
        return expression
        
    # Term -> Value | Term * Value | Term / Value
    def parseTerm(self):
        term = self.parseValue()
        
        while self.peekNextToken()['TOKEN'] in ['*', '/']:
            opToken = self.getCurrentToken()
            value = self.parseValue()
            term = TreeNode(opToken['TOKEN'], term, value)
        
        return term

    # Val -> (Expr) | Constant | ID | - Val
    def parseValue(self):
        consumedToken = self.getCurrentToken()

        # (Expr)
        if consumedToken['TOKEN'] == '(':
            value = self.parseExpression()
            if self.peekNextToken()['TOKEN'] == ')':
                self.getCurrentToken()
                return value

        # Constant
        elif consumedToken['TYPE'] in ['INTEGER_CONSTANT', 'FLOATING_CONSTANT', 'CHAR_CONSTANT', 'STRING_CONSTANT']:
            return TreeNode(consumedToken['TOKEN'])

        # ID
        elif consumedToken['TYPE'] == 'IDENTIFIER':
            return TreeNode(consumedToken['TOKEN'])

        # - Value
        elif consumedToken['TOKEN'] == '-':
            value = self.parseValue()
            return TreeNode('-', None, value)
        
        return None