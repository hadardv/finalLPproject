from src.lexer import Lexer

def test_lexer():
    print("Testing lexer...")  # This should print regardless of what happens next.
    code = "400 * 500"
    expected_tokens = [
        ('NUMBER', 400, 1),
        ('MULTIPLY', '*', 1),
        ('NUMBER', 500, 1)
    ]

    lexer = Lexer(code)
    actual_tokens = list(lexer.tokenize())
    print("Tokens generated:", actual_tokens)  # Check what tokens are generated

    for expected, actual in zip(expected_tokens, actual_tokens):
        print(f"Comparing {expected} to {actual}")  # See comparisons
        assert expected == actual, f"Expected {expected}, got {actual}"

    print("Lexer test passed!")

if __name__ == "__main__":
    test_lexer()
