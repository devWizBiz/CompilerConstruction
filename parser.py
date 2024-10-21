import pdb

class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.value)

# Testing node structure
def dfs(node):
    if node is None:
        return
    print(node.value)
    dfs(node.left)
    dfs(node.right)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.currentTokenIndex = 0
        
    def getCurrentToken(self):
        currentToken = self.tokens.get(self.currentTokenIndex)
        self.incrementIndex()
        return currentToken
    
    def peekNextToken(self):
        return self.tokens.get(self.currentTokenIndex)
    
    def incrementIndex(self):
        self.currentTokenIndex += 1
    
    def parseProgram(self):
        f = {}
        while self.peekNextToken() is not None:
            info = self.parseFunction()
            if info is not None:
                f.update(info)
            else:
                info = self.parseGlobalVariable()
                f.update(info)
        return {"Program": f}

    # ['int' | 'char' | 'float'] IDENTIFIER ;
    def parseGlobalVariable(self):
        typeToken = self.getCurrentToken()
        idToken = self.getCurrentToken()
        if typeToken['TOKEN'] in ['int', 'char', 'float'] and idToken['TYPE'] == 'IDENTIFIER':
            if self.peekNextToken()['TOKEN'] == ';':
                self.getCurrentToken()
                return {idToken['TOKEN']: typeToken['TOKEN']}
        
        self.currentTokenIndex -= 2
        return None
    
    # ['void' | 'int' | 'char' | 'float'] IDENTIFIER () { [statements] }
    def parseFunction(self):
        currentIndex = self.currentTokenIndex
        typeToken = self.getCurrentToken()
        idToken = self.getCurrentToken()
        allTokens = [self.getCurrentToken() for _ in range(3)]
        
        # Check for function grammar
        if (typeToken['TOKEN'] in ['void', 'int', 'char', 'float'] and
            [token['TOKEN'] for token in allTokens] == ['(', ')', '{'] and
            idToken['TYPE'] == 'IDENTIFIER'):
                function = {idToken['TOKEN']: {'retType': typeToken['TOKEN'], 'statements': []}}
                
                # Parse the function body until the closing brace is encountered
                function[idToken['TOKEN']]['statements'] = []
                while self.peekNextToken() and self.peekNextToken()['TOKEN'] != '}':
                    statement = self.parseStatement()
                    if statement is not None:
                        function[idToken['TOKEN']]['statements'].append(statement)
                
                # Consume the closing brace
                if self.peekNextToken() and self.getCurrentToken()['TOKEN'] == '}':
                    return function
        
        # If parsing fails, reset the index to reattempt
        self.currentTokenIndex = currentIndex
        return None

    # 'return' <expression> | 'assignment' <expression> | 'declaration' <expression> #TODO: Implement declaration parsing
    def parseStatement(self):
        currentIndex = self.currentTokenIndex
        statementToken = self.getCurrentToken()
        
        # 'return' <expression>
        if statementToken['TOKEN'] == 'return':
            expression = self.parseExpression()
            if expression is not None and self.peekNextToken()['TOKEN'] == ';':
                self.getCurrentToken()
                return ['return', expression]
            else:
                self.currentTokenIndex = currentIndex
                return None
            
        # 'assignment' <expression>    
        if statementToken['TYPE'] == 'IDENTIFIER':
            if self.peekNextToken()['TOKEN'] == '=':
                consumedToken = self.getCurrentToken()
                expression = self.parseExpression()
                if expression is not None and self.peekNextToken()['TOKEN'] == ';':
                    self.getCurrentToken()
                    return ['assignment', TreeNode(statementToken['TOKEN'], expression)]
            else:
                self.currentTokenIndex = currentIndex
                return None

        # If we hit this point, the statement is not valid, reset the token index
        self.currentTokenIndex = currentIndex
        return None
    
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

    # Val -> (Expr) | INT | ID | - Val
    def parseValue(self):
        consumedToken = self.getCurrentToken()

        # (Expr)
        if consumedToken['TOKEN'] == '(':
            value = self.parseExpression()
            if self.peekNextToken()['TOKEN'] == ')':
                self.getCurrentToken()
                return value

        # Int
        elif consumedToken['TYPE'] in ['INTEGER_CONSTANT']:
            return TreeNode(consumedToken['TOKEN'])

        # ID
        elif consumedToken['TYPE'] == 'IDENTIFIER':
            return TreeNode(consumedToken['TOKEN'])

        # - Value
        elif consumedToken['TOKEN'] == '-':
            value = self.parseValue()
            return TreeNode('-', None, value)
        
        return None