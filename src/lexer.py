import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code

    def tokenize(self):
        token_specifications = [
            ('NUMBER', r'\d+'),
            ('BOOLEAN', r'True|False'),
            ('DEFUN', r'Defun'),
            ('LAMBDA', r'Lambd'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MULTIPLY', r'\*'),
            ('DIVIDE', r'\/'),
            ('MODULO', r'%'),
            ('AND', r'&&'),
            ('OR', r'\|\|'),
            ('NOT', r'!'),
            ('EQUAL', r'=='),
            ('NOT_EQUAL', r'!='),
            ('GREATER', r'>'),
            ('LESS', r'<'),
            ('GREATER_EQUAL', r'>='),
            ('LESS_EQUAL', r'<='),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('COMMA', r','),
            ('COLON', r':'),
            ('DOT', r'\.'),
            ('WHITESPACE', r'[ \t]+'),
            ('NEWLINE', r'\n'),
            ('MISMATCH', r'.'),
        ]

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
