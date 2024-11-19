# External Libraries
import re
import pdb
# Internal Libraries
import support

class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
    
class Parser:
    def __init__(self):
        
        # Initialize token dictionary, token index
        self.tokens = {}
        self.currentTokenIndex = 0

        # Initialize Symbol Table
        
        # Load Parser Pattern for matches in token dictionary
        self.loadParsePattern()
  
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
    Take the TreeNode and turn it into a readable and order format
    """
    def depthFirstSearch(self, node):
        result = ()
        
        def helper(current_node):
            nonlocal result  # Use nonlocal to modify the enclosing `result` variable
            if current_node is None:
                return
            
            try:
                # Append the current value
                result += (current_node.value,)
            except:
                result += (current_node,)
                return
            
            # Traverse the left and right subtrees
            helper(current_node.left)
            helper(current_node.right)
        
        # Start the helper function
        helper(node)
        
        return result

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
    END    
    """
    def parseProgram(self, tokenDict):
        
        # Set internal token dictionary
        self.tokens = tokenDict
        # Keep peeking until no tokens remain
        while self.peekNextToken() is not None:
            info = self.parseFunction()

            if info is None:
                info = self.parseGlobal()

            if info is None:
                unmatchedToken = self.getCurrentToken()
                line = unmatchedToken['LINE']
                column = unmatchedToken['COL']
                value = unmatchedToken['TOKEN']
                support.error(f'Cannot match token found at LINE {line} COLUMN {column}: {value}')       
            
    """
    function <statements,conditions>
    """
    def parseFunction(self):
        # Save index if not function
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
                conditionalStatement = self.parseConditional()
                if conditionalStatement is not None:
                    for line in conditionalStatement:
                        listOfStatements.append(line)
                    continue

            if statement is not None:
                listOfStatements.append(statement)
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
        # Save index if not global variable
        currentIndex = self.currentTokenIndex

        statement = self.parseStatement()
        if statement is not None and statement[0] == "VARIABLE_DECLARATION":
            return statement[1]
        else:
            self.currentTokenIndex = currentIndex
            return None

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
            return (match.lastgroup, (totalTokens[1]['TOKEN'], totalTokens[0]['TOKEN']), None ) 
        elif match is not None and match.lastgroup == "VARIABLE_DECLARATION_ASSIGNMENT":
            expression = self.getExpressionAndEnd()
            if expression is not None:
                return (match.lastgroup, (totalTokens[1]['TOKEN'], totalTokens[0]['TOKEN']),
                         self.depthFirstSearch(TreeNode(totalTokens[1]['TOKEN'], expression)))

        self.currentTokenIndex = currentIndex
            
        # Get two tokens for return / assignment check
        totalTokens = [self.getCurrentToken() for _ in range(2)]
        match = self.isMatch(totalTokens)
        
        if match is not None and match.lastgroup == "VARIABLE_ASSIGNMENT":
            expression = self.getExpressionAndEnd()
            if expression is not None:
                return (match.lastgroup, None, self.depthFirstSearch(TreeNode(totalTokens[0]['TOKEN'], expression)))

        self.currentTokenIndex = currentIndex

        # Get one tokens for return check
        totalTokens = [self.getCurrentToken() for _ in range(1)]
        match = self.isMatch(totalTokens)
        
        if match is not None and match.lastgroup == "RETURN":
            expression = self.getExpressionAndEnd()
            if expression is not None:
                returnTuple = self.depthFirstSearch(expression)
                if len(returnTuple) == 1:
                    returnTuple = returnTuple[0]
                return (match.lastgroup, None, returnTuple)

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

        return ('CONDITIONAL', condition), ('IF', ifStatements), ('ELSE', elseStatements)

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

        return self.depthFirstSearch(TreeNode(operatorToken['TOKEN'], left, right))

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