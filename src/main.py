from lexer import Lexer
from parser import Parser


def main():
    # Get user input
    user_input = input("Enter a mathematical expression: ")

    # Create lexer and generate tokens
    lexer = Lexer(user_input)
    tokens = list(lexer.tokenize())

    # Print tokens for debugging (optional)
    print("Tokens:", tokens)

    # Specify the path to your grammar file
    grammar_file = 'C:\\Users\\hadar\\PythonCourrse\\LPproject2\\grammar\\grammar.bnf'

    # Create parser and parse the expression
    parser = Parser(tokens, grammar_file)
    result = parser.parse()

    # Print the parse tree
    print("Parse Tree:")
    print(result)


if __name__ == '__main__':
    main()
