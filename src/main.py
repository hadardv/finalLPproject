from src.lexer import Lexer
from src.parser import Parser


def main():

    user_input = input("Enter a mathematical expression: ")
    lexer = Lexer(user_input)
    tokens = list(lexer.tokenize())
    print("Tokens:", tokens)

    grammar_file = 'C:\\Users\\hadar\\PythonCourrse\\LPproject2\\grammar\\grammar.bnf'
    parser = Parser(tokens, grammar_file)

    try:
        result = parser.parse()
        print("Parse Tree:")
        print(parser.prettify_parse_tree(result))
    except SyntaxError as e:
        print(f"Parsing failed: {e}")

if __name__ == '__main__':
    main()