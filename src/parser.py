def read_bnf(filename):
    grammar = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                head, body = line.split('::=')
                head = head.strip()
                productions = [prod.strip().split() for prod in body.split('|')]
                grammar[head] = productions
    return grammar


class Parser:
    def __init__(self, tokens, grammar_file):
        self.tokens = tokens
        self.grammar = read_bnf(grammar_file)
        self.current_token = None
        self.token_index = 0
        self.advance()

    def advance(self):
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
            self.token_index += 1
        else:
            self.current_token = ('EOF', None, None)

    def parse(self):
        result = self.parse_expr()
        return self.prettify_parse_tree(result)

    def parse_expr(self):
        left = self.parse_term()
        while self.current_token[1] in ('+', '-'):
            op = self.current_token[1]
            self.advance()
            right = self.parse_term()
            left = ('<expr>', [left, (op, op), right])
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token[1] in ('*', '/'):
            op = self.current_token[1]
            self.advance()
            right = self.parse_factor()
            left = ('<term>', [left, (op, op), right])
        return left

    def parse_factor(self):
        if self.current_token[0] == 'NUMBER':
            node = ('<number>', self.current_token[1])
            self.advance()
            return node
        elif self.current_token[1] == '(':
            self.advance()
            expr = self.parse_expr()
            if self.current_token[1] == ')':
                self.advance()
                return ('<factor>', [('(', '('), expr, (')', ')')])
            else:
                raise SyntaxError("Expected closing parenthesis")
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def prettify_parse_tree(self, tree, indent=0):
        if not isinstance(tree, tuple):
            return "  " * indent + str(tree) + "\n"

        rule_name, contents = tree
        result = "  " * indent + f"{rule_name}:\n"

        if isinstance(contents, list):
            for item in contents:
                result += self.prettify_parse_tree(item, indent + 1)
        else:
            result += "  " * (indent + 1) + f"{contents}\n"

        return result

# Example usage
if __name__ == '__main__':
    from lexer import Lexer

    code = "3 + 4 * (2 - 1)"
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())

    grammar_file = 'C:\\Users\\hadar\\PythonCourrse\\LPproject2\\grammar\\grammar.bnf'
    parser = Parser(tokens, grammar_file)

    result = parser.parse()
    print(result)