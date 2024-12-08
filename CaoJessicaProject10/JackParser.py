import JackTokenizer

class CompilationEngine:

    binaryOp = {'+', '-', '*', '/', '|', '=', '&lt;', '&gt;', '&amp;'}
    unaryOp = {'-', '~'}
    keywordConstant = {'true', 'false', 'null', 'this'}

    def __init__(self, input, output):
        """
        Creates a new compilation engine with the given input and output files.
        """
        self.tokenizer = JackTokenizer.JackTokenizer(input)
        self.parsedRules = []
        self.outputFile = open(output, 'w')
        self.indent = ""

    def addIndent(self):
        """
        Indents the line
        """
        self.indent += "    "

    def deleteIndent(self):
        """
        Same as shift tab!
        """
        self.indent = self.indent[:-4]

    def writeNonTerminalStart(self, rule):
        """
        Writes opening tag <rule> 
        """
        self.outputFile.write(self.indent+"<"+rule+">\n")
        self.parsedRules.append(rule)
        self.addIndent()

    def writeNonTerminalEnd(self):
        """
        Writes closing tag <rule> 
        """
        self.deleteIndent()
        rule = self.parsedRules.pop()
        self.outputFile.write(self.indent+"</"+rule+">\n")

    def writeTerminal(self, token, value):
        """
        Writes <token> token value <token>
        """
        self.outputFile.write(self.indent+"<"+token+"> "+value+" </"+token+">\n")

    def advance(self):
        """
        Sets tokenizer to go to the next token to write.
        """
        token, value = self.tokenizer.advance()
        self.writeTerminal(token, value)

    def nextValueIn(self, lst):
        """
        Checks if the value of the next token matches any value in a given list.
        """
        value = self.tokenizer.peek()[1]
        return value in lst

    def nextValueIs(self, val):
        """
        Checks if the next value is val 
        """
        value = self.tokenizer.peek()[1]
        return value == val

    def nextTokenIs(self, tok):
        """
        Checks if next token is tok
        """
        token = self.tokenizer.peek()[0]
        return token == tok

    def compileClass(self):
        """
        Compiles a complete class.
        """
        self.writeNonTerminalStart('class')
        self.advance()  # get 'class' keyword
        self.advance()  # get class name
        self.advance()  # get '{' symbol
        if self.existClassVarDec():
            self.compileClassVarDec()
        while self.existSubroutine():
            self.compileSubroutine()
        self.advance() #get '}' symbol
        self.writeNonTerminalEnd()
        self.outputFile.close()

    def existClassVarDec(self):
        """
        Checks if next token indicates class variable declaration
        """
        return self.nextValueIs("static") or self.nextValueIs("field")

    def existSubroutine(self):
        """
        Checks if next token indicates subroutine declaration
        """
        return self.nextValueIs("constructor") or self.nextValueIs("method")\
               or self.nextValueIs("function")

    def compileClassVarDec(self):
        """
        Compiles one or more class variable declarations and writes the 
        corresponding XML output.
        """
        while self.existClassVarDec():
            self.writeNonTerminalStart('classVarDec')
            self.writeClassVarDec()
            self.writeNonTerminalEnd()

    def writeClassVarDec(self):
        """
        Writes a single class variable declaration to the XML output.
        """
        self.advance()  # get 'static' or 'field'
        self.advance()  # get var type
        self.advance()  # get var name
        while self.nextValueIs(","):
            self.advance()  # get ',' symbol
            self.advance()  # get var name
        self.advance()  # get ';' symbol

    def compileSubroutine(self):
        """
        Compiles a complete method, function, or constructor.
        """
        self.writeNonTerminalStart('subroutineDec')
        self.advance()  # get subroutine type
        self.advance()  # get subroutine return type / 'constructor'
        self.advance()  # get subroutine name / 'new'
        self.advance()  # get '(' symbol
        self.compileParameterList()
        self.advance()  # get ')' symbol
        self.compileSubroutineBody()
        self.writeNonTerminalEnd()


    def compileParameterList(self):
        """
        Compiles a (possibly empty) parameter list, not including the enclosing "()"
        """
        self.writeNonTerminalStart('parameterList')
        while self.existParameter():
            self.writeParam()
        self.writeNonTerminalEnd()

    def existParameter(self):
        """
        Checks if the next tokens indicate a parameter in a parameter list.
        """
        return not self.nextTokenIs("symbol")

    def writeParam(self):
        """
        Writes a single parameter (type and name) from a parameter list to 
        the XML output.
        """
        self.advance()  # get parameter type
        self.advance()  # get parameter name
        if self.nextValueIs(","):
            self.advance()  # get ',' symbol


    def compileSubroutineBody(self):
        """
        Compiles the body of a subroutine declaration, including variable declarations
        and statements, and writes the corresponding XML output.
        """
        self.writeNonTerminalStart('subroutineBody')
        self.advance()  # get '{' symbol
        while self.existVarDec():
            self.compileVarDec()
        self.compileStatements()
        self.advance()  # get '}' symbol
        self.writeNonTerminalEnd()

    def existVarDec(self):
        """
        Checks if the next value is a variable declaration
        """
        return self.nextValueIs("var")

    def compileVarDec(self):
        """
        Compiles a variable declaration.
        """
        self.writeNonTerminalStart('varDec')
        self.advance()  # get 'var' keyword
        self.advance()  # get var type
        self.advance()  # get var name
        while self.nextValueIs(","):
            self.advance()  # get ',' symbol
            self.advance()  # get var name
        self.advance()  # get ';' symbol
        self.writeNonTerminalEnd()

    def compileStatements(self):
        """
        Compiles a sequence of statements, not including the enclosing "{}".
        """
        self.writeNonTerminalStart('statements')
        while self.existStatement():
            if   self.nextValueIs("do"):     self.compileDo()
            elif self.nextValueIs("let"):    self.compileLet()
            elif self.nextValueIs("if"):     self.compileIf()
            elif self.nextValueIs("while"):  self.compileWhile()
            elif self.nextValueIs("return"): self.compileReturn()
        self.writeNonTerminalEnd()

    def existStatement(self):
        """
        Checks if next value is a statement.
        """
        return self.nextValueIs("do") \
            or self.nextValueIs("let")\
            or self.nextValueIs("if")\
            or self.nextValueIs("while")\
            or self.nextValueIs("return")\

    def compileDo(self):
        """
        Compiles a do statement
        """
        self.writeNonTerminalStart('doStatement')
        self.advance()  # get 'do' keyword
        self.compileSubroutineCall()
        self.advance()  # get ';' symbol
        self.writeNonTerminalEnd()

    def compileSubroutineCall(self):
        """
        Compiles a subroutine call.
        """
        self.advance()  # get class/subroutine/var name
        if self.nextValueIs("."):  # case of className.subroutineName
            self.advance()  # get '.' symbol
            self.advance()  # get subroutine name
        self.advance()  # get '(' symbol
        self.compileExpressionList()
        self.advance()  # get ')' symbol

    def compileExpressionList(self):
        """
        ompiles a list of expressions, including separating commas.
        """
        self.writeNonTerminalStart('expressionList')
        if self.existExpression():
            self.compileExpression()
        while self.nextValueIs(","):  # case of multiple expressions
            self.advance()  # get ',' symbol
            self.compileExpression()
        self.writeNonTerminalEnd()

    def compileLet(self):
        """
        Compiles a let statement, including optional array indexing and the 
        assigned expression,
        """
        self.writeNonTerminalStart('letStatement')
        self.advance()  # get 'let' keyword
        self.advance()  # get var name
        if self.nextValueIs("["): #case of varName[expression]
            self.writeArrayIndex()
        self.advance()  # get '='
        self.compileExpression()
        self.advance()  # get ';' symbol
        self.writeNonTerminalEnd()

    def writeArrayIndex(self):
        """
        Writes the XML output for array indexing, including the brackets and 
        the contained expression.
        """
        self.advance()  # get '[' symbol
        self.compileExpression()
        self.advance()  # get ']' symbol

    def compileWhile(self):
        """
        Compiles a while statement
        """
        self.writeNonTerminalStart('whileStatement')
        self.advance()  # get 'while' keyword
        self.advance()  # get '(' symbol
        self.compileExpression()
        self.advance()  # get ')' symbol
        self.advance()  # get '{' symbol
        self.compileStatements()
        self.advance()  # get '}' symbol
        self.writeNonTerminalEnd()

    def compileReturn(self):
        """
        Compiles a return statement.
        """
        self.writeNonTerminalStart('returnStatement')
        self.advance()  # get 'return' keyword
        while self.existExpression():
            self.compileExpression()
        self.advance()  # get ';' symbol
        self.writeNonTerminalEnd()

    def existExpression(self):
        """
        Checks if the next tokens indicate the presence of an expression.
        """
        return self.existTerm()

    def existTerm(self):
        """
        Checks if the next tokens indicate the presence of a term.
        """
        # token, value = self.tokenizer.peek()
        return self.nextTokenIs("integerConstant") or self.nextTokenIs("stringConstant")\
               or self.nextTokenIs("identifier") or (self.nextValueIn(self.unaryOp))\
               or (self.nextValueIn(self.keywordConstant)) or (self.nextValueIs('('))

    def compileIf(self):
        """
        Compiles an if statement, possibly with a trailing else clause.
        """
        self.writeNonTerminalStart('ifStatement')
        self.advance()  # get 'if' keyword
        self.advance()  # get '(' symbol
        self.compileExpression()
        self.advance()  # get ')' symbol
        self.advance()  # get '{' symbol
        self.compileStatements()
        self.advance()  # get '}' symbol
        if self.nextValueIs("else"):
            self.advance()  # get 'else' keyword
            self.advance()  # get '{' symbol
            self.compileStatements()
            self.advance()  # get '}' symbol
        self.writeNonTerminalEnd()

    def compileExpression(self):
        """
        Compiles an expression.
        """
        self.writeNonTerminalStart('expression')
        self.compileTerm()
        while self.nextValueIn(self.binaryOp):
            self.advance()  # get op symbol
            self.compileTerm()
        self.writeNonTerminalEnd()

    def compileTerm(self):
        """
        Compiles a term
        """
        self.writeNonTerminalStart('term')
        if self.nextTokenIs("integerConstant") or self.nextTokenIs("stringConstant")\
                or (self.nextValueIn(self.keywordConstant)):
            self.advance()  # get constant
        elif self.nextTokenIs("identifier"):
            self.advance()  # get class/var name
            if self.nextValueIs("["):  # case of varName[expression]
                self.writeArrayIndex()
            if self.nextValueIs("("):
                self.advance()  # get '(' symbol
                self.compileExpressionList()
                self.advance()  # get ')' symbol
            if self.nextValueIs("."):  # case of subroutine call
                self.advance()  # get '.' symbol
                self.advance()  # get subroutine name
                self.advance()  # get '(' symbol
                self.compileExpressionList()
                self.advance()  # get ')' symbol
        elif self.nextValueIn(self.unaryOp):
            self.advance()  # get unary operation symbol
            self.compileTerm()
        elif self.nextValueIs("("):
            self.advance()  # get '(' symbol
            self.compileExpression()
            self.advance()  # get ')' symbol
        self.writeNonTerminalEnd()