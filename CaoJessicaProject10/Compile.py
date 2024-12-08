import sys
import os
import JackParser


def main():
    userInput = sys.argv[1]

    if os.path.isdir(userInput):
        if not userInput.endswith("/"):
            userInput += "/"
        files = os.listdir(userInput)
        for file in files:
            if file.endswith('.jack'):
                fileName = file.split(".")[0]
                comp = JackParser.CompilationEngine(userInput + file, userInput + fileName + ".xml")
                comp.compileClass()
    #Case input is file, just parse it
    elif os.path.isfile(userInput):
        userInput = userInput.split(".")[0]
        comp = JackParser.CompilationEngine(userInput + ".jack", userInput + ".xml")
        comp.compileClass()
    #Raise an exception
    else:
        raise Exception("The input is not valid, please try again")

if __name__ == "__main__":
    main()