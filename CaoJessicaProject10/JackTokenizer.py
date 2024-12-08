import re


class JackTokenizer:

    KeywordsCodes = {"class", "constructor", "function", "method", "field", 
                     "static", "var", "int", "char", "boolean", "void", "true", 
                     "false", "null", "this", "let", "do", "if", "else", 
                     "while", "return"}
    SymbolsCodes = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*',
                    '/', '&', '<', '>', '=', '~'}

    def __init__(self, file):
        """
        Initializes the tokenizer

        Args:
            file (string): Path to the Jack source file.

        Attributes:
            file (file object): Jack file
            currtoken (tuple): The current token being processed
            lines (string): The complete source code read from the file.
            tokens (list): list[tuples] where each tuple is token type and its value.
        """
        self.file = open(file)
        self.currtoken = ""
        self.lines = self.file.read()  # Read code
        self.removeComments()  # Remove comments
        self.tokens = self.tokenize()
        self.tokens = self.replaceSymbols()

    def removeComments(self):
        """ 
        Removes comments from jack file
        """
        current = 0
        filtered = ''
        end = 0
        while current< len(self.lines):
            currentChar = self.lines[current]
            if currentChar == "\"":
                end = self.lines.find("\"", current+1)
                filtered += self.lines[current:end+1]
                current = end + 1
            elif currentChar == "/":
                if self.lines[current + 1] == "/":
                    end = self.lines.find("\n", current + 1)
                    current = end + 1
                    filtered += " "
                elif self.lines[current + 1] == "*":
                    end = self.lines.find("*/", current + 1)
                    current = end + 2
                    filtered += " "
                else:
                    filtered += self.lines[current]
                    current += 1
            else:
                filtered += self.lines[current]
                current += 1
        self.lines = filtered
        return

    def tokenize(self):
        """
        Tokenizes the source code into lexical elements.

        Each token is represented as a tuple where the first element is the 
        token type (like keyword or symbol). The second element is the token 
        value (like class or "{").

        returns: list[tuple]: tuples in the form (token type, token value).
        """
        return [self.token(word) for word in self.split(self.lines)]

    def token(self, word):
        """
        Returns token tuple.

        input: word (string)
        returns: tuple[string, string]
        """
        if re.match(self.keywordsRegex, word) is not None: 
            return ("keyword", word)
        elif re.match(self.symbolsRegex, word) is not None: 
            return ("symbol", word)
        elif re.match(self.integerRegex, word) is not None:  
            return ("integerConstant", word)
        elif re.match(self.stringsRegex, word) is not None:  
            return ("stringConstant", word[1:-1])
        else:                                            
            return ("identifier", word)


    keywordsRegex = '(?!\w)|'.join(KeywordsCodes) + '(?!\w)'
    symbolsRegex = '[' + re.escape('|'.join(SymbolsCodes)) + ']'
    integerRegex = r'\d+'
    stringsRegex = r'"[^"\n]*"'
    identifiersRegex = r'[\w]+'
    word = re.compile(keywordsRegex + '|' + symbolsRegex + '|' + integerRegex \
                      + '|' + stringsRegex + '|' + identifiersRegex)

    def split(self, line):
        """
        Finds all occurrences of lexical elements (keywords, symbols, integers, 
        strings, and identifiers) in a line from file and returns it as a list

        input: line (string)
        returns: list[string]
        """
        return self.word.findall(line)

    def replaceSymbols(self):
        """
        Replaces symbols with their xml code for each tuple token 
            - `<` becomes `&lt;`
            - `>` becomes `&gt;`
            - `"` becomes `&quot;`
            - `&` becomes `&amp;`

        returns: list[tuple]: A list of tokens with symbols replaced.
        """
        return [self.replace(pair) for pair in self.tokens]

    def replace(self, pair):
        """
        Creates tuple token for symbols 

        input: pair (tuple): A token tuple of the form (token type, token value).

        returns: tuple the token tuple with non xml symbols replaced, if necessary.
        """
        token, value = pair
        if   value == '<': 
            return (token, '&lt;')
        elif value == '>': 
            return (token, '&gt;')
        elif value == '"': 
            return (token, '&quot;')
        elif value == '&': 
            return (token, '&amp;')
        else:              
            return (token, value)

    def hasMoreTokens(self):
        """
        Checks if there are more tokens to process

        returns: bool
        """
        return self.tokens != []

    def advance(self):
        """
        Advances to the next token in the list of tokens and pops off the 
        token after advancing.

        Removes the next token from the list and sets it as the current token.

        returns: tuple
        """
        self.currtoken = self.tokens.pop(0)
        return self.currtoken

    def peek(self):
        """
        Returns the next token without removing it from the list or 
        ("ERROR", 0) if no tokens are left.

        returns: tuple
        """
        if self.hasMoreTokens():
            return self.tokens[0]
        else:
            return ("ERROR", 0)

    def getToken(self):
        """
        Returns the type of the current token
        """
        return self.currtoken[0]

    def getValue(self):
        """
        Returns the current value
        """
        return self.currtoken[1]