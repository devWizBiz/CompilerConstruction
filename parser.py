# External Libraries
import re
import pdb
# Internal Libraries
# N/A

# TMP
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.value)
class Parser:
    def __init__(self):
        
        # Initialize token dictionary, token index
        self.tokens = {}
        self.currentTokenIndex = 0
        
        # Load Parser Pattern for matches in token dictionary
        self.loadParsePattern()

    # TMP
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
    
    """
    Loads the parse patterns that will be used to determine the match for the input of the tokens dictionary.
    """        
    def loadParsePattern(self):

        # Defined Parser Patterns
        PARSER_PATTERNS = [
        ('FUNCTION_DECLARATION', r'(void|int|float|char)IDENTIFIER\(\)\{'),
        ('VARIABLE_DECLARATION', r'(int|float|char)IDENTIFIER;'),
        ('VARIABLE_DECLARATION_ASSIGNMENT', r'(int|float|char)IDENTIFIER='),
        ('VARIABLE_ASSIGNMENT', r'IDENTIFIER='),
        ('RETURN', r'return'), ]
        
        # Join the token patterns through the OR operator along with it's sub-pattern name
        PATTERNS_COMBINED = '|'.join('(?P<%s>%s)' % pair for pair in PARSER_PATTERNS)
        self.COMPILED_PATTERNS = re.compile(PATTERNS_COMBINED)

    """
    Check for match against the compiled patters
    """
    def isMatch(self, totalTokens):
        checkForMatch = ""
        for token in totalTokens:
            if token['TYPE'] in ['KEYWORD', 'PUNCTUATORS']:
                checkForMatch += token['TOKEN']
            else:
                checkForMatch += token['TYPE']
                
        # Look for match
        match = self.COMPILED_PATTERNS.search(checkForMatch)
        return match

    """
    Get expression and check for semi-colon
    """
    def getExpressionAndEnd(self):
            expression = self.parseExpression()
            if expression is not None and self.peekNextToken()['TOKEN'] == ';':
                self.getCurrentToken() # Consume ';'
                return expression
            else:
                return None

    """
    Peek at the next token using the token index
    """
    def peekNextToken(self):
        return self.tokens.get(self.currentTokenIndex)

    """
    Retrieve the current token and increment
    """
    def getCurrentToken(self):
        currentToken = self.tokens.get(self.currentTokenIndex)
        self.incrementIndex()
        return currentToken

    """
    Increment the token index
    """
    def incrementIndex(self):
        self.currentTokenIndex += 1

    """
    START
        - Parse Function
            -- Parse Statement
                --- Parse declaration
                --- Parse assignment / return
                    ---- Parse Expression
                        ----- Parse Term
                            ------ Parse Value
            -- Parse Conditional
                --- Parse Statements
        - Parse Global
            -- Parse declaration
    END    
    """
    def parseProgram(self, tokenDict):
        
        # Set internal token dictionary
        self.tokens = tokenDict
        # Keep peeking until no tokens remain
        while self.peekNextToken() is not None:
            info = self.parseFunction()
            
    """
    function <statements,conditions>
    """
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
                if statement[0] in ['VARIABLE_DECLARATION', 'VARIABLE_DECLARATION_ASSIGNMENT']:
                    statement = (statement[0], statement[1],  tuple(self.depthFirstSearch(statement[2])))
                    listOfStatements.append(statement)
                elif statement[0] in ['VARIABLE_ASSIGNMENT',  'RETURN']:
                    statement = ((statement[0]), tuple(self.depthFirstSearch(statement[1])))
                    listOfStatements.append(statement)
                elif statement[0][0] in 'conditional': # TODO: Need to clean this up, probably another function
                    conditionalList = []
                    for condition, treeNode in statement:
                        if isinstance(treeNode, list):
                            tmpList = []
                            for branch in treeNode:
                                if branch[0] in ['VARIABLE_DECLARATION', 'VARIABLE_DECLARATION_ASSIGNMENT']:
                                    statement = ((condition), branch[1], tuple(self.depthFirstSearch(branch[2])))
                                    tmpList.append(statement)
                                elif branch[0] in ['VARIABLE_ASSIGNMENT',  'RETURN']:
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
    
    """
    declaration to Symbol Table
    """
    def parseGlobal(self):
        pass
    
    """
    declaration to Symbol Table
    return <expression> | assignment <expression>
    """
    def parseStatement(self):
        currentIndex = self.currentTokenIndex
        
        # Get three tokens for declaration / declaration assignment check
        totalTokens = [self.getCurrentToken() for _ in range(3)]
        match = self.isMatch(totalTokens)
    
        if match is not None and match.lastgroup == "VARIABLE_DECLARATION":
            completedDeclaration = (match.lastgroup, totalTokens[0]['TOKEN'], (totalTokens[1]['TOKEN']))
            return completedDeclaration 
        elif match is not None and match.lastgroup == "VARIABLE_DECLARATION_ASSIGNMENT":
            expression = self.getExpressionAndEnd()
            if expression is not None:
                # Append Symbol Table
                return (match.lastgroup, totalTokens[0]['TOKEN'], TreeNode(totalTokens[1]['TOKEN'], expression))

        self.currentTokenIndex = currentIndex
            
        # Get two tokens for return / assignment check
        totalTokens = [self.getCurrentToken() for _ in range(2)]
        match = self.isMatch(totalTokens)
        
        if match is not None and match.lastgroup == "VARIABLE_ASSIGNMENT":
            expression = self.getExpressionAndEnd()
            if expression is not None:
                return (match.lastgroup, TreeNode(totalTokens[0]['TOKEN'], expression))

        self.currentTokenIndex = currentIndex

        # Get one tokens for return check
        totalTokens = [self.getCurrentToken() for _ in range(1)]
        match = self.isMatch(totalTokens)
        
        if match is not None and match.lastgroup == "RETURN":
            expression = self.getExpressionAndEnd()
            if expression is not None:
                return (match.lastgroup, expression)

        # No other options
        self.currentTokenIndex = currentIndex
        return None
    
    """
    if <condition> <statements> else <statements>
    """
    def parseConditional(self):
        currentIndex = self.currentTokenIndex
        
        currentToken = self.getCurrentToken()
        if currentToken['TOKEN'] != 'if':
            self.currentTokenIndex = currentIndex
            return None
        
        if self.getCurrentToken()['TOKEN'] != '(':
            self.currentTokenIndex = currentIndex
            return None

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

    """
    condition <IDENTIFIER|INTEGER_CONSTANT> <comparison operator> <IDENTIFIER|INTEGER_CONSTANT>
    """
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

    """
    Expr -> Term | Expr + Term | Expr - Term
    """
    def parseExpression(self):
        expression = self.parseTerm()

        while self.peekNextToken()['TOKEN'] in ['+', '-']:
            opToken = self.getCurrentToken()
            term = self.parseTerm()
            expression = TreeNode(opToken['TOKEN'], expression, term)
        
        return expression
    
    """
    Term -> Value | Term * Value | Term / Value
    """
    def parseTerm(self):
        term = self.parseValue()
        
        while self.peekNextToken()['TOKEN'] in ['*', '/']:
            opToken = self.getCurrentToken()
            value = self.parseValue()
            term = TreeNode(opToken['TOKEN'], term, value)
        
        return term
    
    """
    Val -> (Expr) | INTEGER/FLOAT | IDENTIFIER | - Value
    """
    def parseValue(self):
        consumedToken = self.getCurrentToken()

        # (Expr)
        if consumedToken['TOKEN'] == '(':
            value = self.parseExpression()
            if self.peekNextToken()['TOKEN'] == ')':
                self.getCurrentToken()
                return value

        # INTEGER/FLOAT Constant
        elif consumedToken['TYPE'] in ['INTEGER_CONSTANT', 'FLOATING_CONSTANT']:
            return TreeNode(consumedToken['TOKEN'])

        # IDENTIFIER
        elif consumedToken['TYPE'] == 'IDENTIFIER':
            return TreeNode(consumedToken['TOKEN'])

        # - Value
        elif consumedToken['TOKEN'] == '-':
            value = self.parseValue()
            return TreeNode('-', None, value)
        
        return None