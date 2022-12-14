from enum import Enum


class TokenType(Enum):
    # Single-character tokens
    CARET = "caret"
    COLON = "colon"
    COMMA = "comma"
    LEFT_BRACKET = "left_bracket"
    LEFT_CURLY_BRACKET = "left_curly_bracket"
    LEFT_SQUARE_BRACKET = "left_square_bracket"
    PLUS = "plus"
    RIGHT_BRACKET = "right_bracket"
    RIGHT_CURLY_BRACKET = "right_curly_bracket"
    RIGHT_SQUARE_BRACKET = "right_square_bracket"
    SEMICOLON = "semicolon"
    SLASH = "slash"
    STAR = "star"
    # Multi-character tokens
    AMPERSAND_AMPERSAND = "ampersand_ampersand"
    BANG = "bang"
    BAR_BAR = "bar_bar"
    DOUBLE_ARROW = "double_arrow"
    ELLIPSIS = "ellipsis"
    EQUAL_EQUAL = "equal_equal"
    GREATER_EQUAL = "greater_equal"
    LESS_EQUAL = "less_equal"
    PIPE = "pipe"
    SINGLE_ARROW = "single_arrow"
    # Ambiguous single character tokens
    BANG_EQUAL = "bang_equal"
    DOT = "dot"
    EQUAL = "equal"
    GREATER = "greater"
    LESS = "less"
    MINUS = "minus"
    # Literals
    FLOAT = "float"
    IDENTIFIER = "identifier"
    INTEGER = "integer"
    STRING = "string"
    # Keywords
    ELIF = "elif"
    ELSE = "else"
    FALSE = "false"
    FOR = "for"
    IF = "if"
    IN = "in"
    LET = "let"
    MATCH = "match"
    NOTHING = "nothing"
    RETURN = "return"
    STRUCT = "struct"
    TRUE = "true"
    WHILE = "while"
    YIELD = "yield"
    # Comments
    COMMENT = "comment"
    # Other
    EOF = "eof"
