class Parser:
    def __init__(self, tokens, grammar_file):
        self.tokens = tokens
        self.grammar = self.read_bnf(grammar_file)
        self.current_token = None
        self.token_index = 0
        self.advance()

    def read_bnf(self, filename):
        grammar = {}
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip() #removes trialing e.g whitespaces
                if line and not line.startswith('#'):
                    head, body = line.split('::=')
                    head = head.strip()
                    productions = [prod.strip().split() for prod in body.split('|')] #split creates an array of the grammar in each line
                    grammar[head] = productions
        return grammar

    def advance(self):
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
            self.token_index += 1
        else:
            self.current_token = ('EOF', None, None)

    def parse(self):
        result = self.parse_rule('<program>')
        if result is None:
            raise SyntaxError("Failed to parse the input")
        return result

    def prettify_parse_tree(self, tree, indent=0):
        if isinstance(tree, str):
            return "  " * indent + tree

        if isinstance(tree, tuple):
            if len(tree) == 2:
                rule_name, contents = tree
            elif len(tree) == 3:
                rule_name, contents, _ = tree
            else:
                return "  " * indent + str(tree)
        else:
            return "  " * indent + str(tree)

        result = "  " * indent + rule_name + "\n"

        if isinstance(contents, list):
            for item in contents:
                result += self.prettify_parse_tree(item, indent + 1)
        else:
            result += "  " * (indent + 1) + str(contents) + "\n"

        return result

    ########
    # parse_rule function takes a rule_name from the top grammar rule, if it isn't in there it goes down
    # until it finds the right grammar rule
    ########
    def parse_rule(self, rule_name):
        print(f"Attempting to parse rule: {rule_name}")
        if rule_name not in self.grammar:
            result = self.match_token(rule_name)
            print(f"Matching token {rule_name}: {'Success' if result else 'Fail'}")
            return result

        for production in self.grammar[rule_name]:
            print(f"Trying production: {production}")
            result = self.try_production(rule_name, production)
            if result is not None:
                if rule_name in ['<expression>', '<term>']:
                    while self.current_token[0] in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE']:
                        op = self.current_token
                        self.advance()
                        right = self.parse_rule('<factor>' if rule_name == '<term>' else '<term>')
                        if right is None:
                            break
                        result = (rule_name, [result, (op[0], op[1]), right])
                elif rule_name == '<factor>' and len(production) == 2 and production[0] == '<unary_op>':
                    # Handle unary operations
                    op, factor = result[1]
                    result = (rule_name, [(op[0], op[1]), factor])
                print(f"Production succeeded: {production}")
                return result
            print(f"Production failed: {production}")

        print(f"All productions failed for rule: {rule_name}")
        return None

    def match_token(self, expected_type):
        if self.current_token[0] == expected_type:
            token = self.current_token
            print(f"Matched token: {token}")
            self.advance()
            return (token[0], token[1])
        print(f"Failed to match token. Expected {expected_type}, got {self.current_token[0]}")
        return None

    def try_production(self, rule_name, production):
        print(f"Trying production: {production}")
        saved_index = self.token_index
        result = []
        for term in production:
            if term.startswith('<'):
                node = self.parse_rule(term)
            else:
                node = self.match_token(term)
            if node is None:
                self.token_index = saved_index
                return None
            result.append(node)
        print(f"Production succeeded: {production}")
        return (rule_name, result)

# Example usage
if __name__ == '__main__':
    from lexer import Lexer

    code = "3 + 4 * (2 - 1)"
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())

    grammar_file = 'C:\\Users\\hadar\\PythonCourrse\\LPproject2\\grammar\\grammar.bnf'
    parser = Parser(tokens, grammar_file)
    result = parser.parse()
    print(parser.prettify_parse_tree(result))