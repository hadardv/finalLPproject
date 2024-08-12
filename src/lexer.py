import re


class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code

    def tokenize(self):
        # Tokens defined with regex patterns
        token_specifications = [
            ('NUMBER', r'\d+'),  # Integer literals
            ('BOOLEAN', r'True|False'),  # Boolean literals
            ('PLUS', r'\+'),  # Arithmetic operators
            ('MINUS', r'-'),
            ('MULTIPLY', r'\*'),
            ('DIVIDE', r'\/'),
            ('MODULO', r'%'),
            ('AND', r'&&'),  # Boolean operators
            ('OR', r'\|\|'),
            ('NOT', r'!'),
            ('EQUAL', r'=='),  # Comparison operators
            ('NOT_EQUAL', r'!='),
            ('GREATER', r'>'),
            ('LESS', r'<'),
            ('GREATER_EQUAL', r'>='),
            ('LESS_EQUAL', r'<='),
            ('LPAREN', r'\('),  # Parentheses for grouping expressions
            ('RPAREN', r'\)'),
            ('WHITESPACE', r'[ \t]+'),  # Skip whitespace
            ('NEWLINE', r'\n'),  # Newline
            ('MISMATCH', r'.'),  # Any other character
        ]

        # Compile a regex that matches any of the specified tokens
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specifications)
        get_token = re.compile(tok_regex).match

        line_number = 1
        position = line_start = 0
        while position < len(self.source_code):
            match = get_token(self.source_code, position)
            if match is None:
                raise RuntimeError(f'Unexpected character {self.source_code[position]} at position {position}')

            type_ = match.lastgroup
            value = match.group()

            if type_ == 'NUMBER':
                value = int(value)
                yield (type_, value, line_number)
            elif type_ not in ['WHITESPACE', 'NEWLINE']:
                yield (type_, value, line_number)

            if type_ == 'NEWLINE':
                line_start = position
                line_number += 1

            position = match.end()

        yield 'EOF', None, line_number
# Example usage
if __name__ == "__main__":
    code = "if (3 > 2) && True { x = 5 + 4; }"
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())
    for token in tokens:
        print(token)
