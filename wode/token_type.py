from enum import Enum


class TokenType(Enum):
    #  Single-character tokens
    LEFT_BRACKET = "left_bracket"
    RIGHT_BRACKET = "right_bracket"
    LEFT_CURLY_BRACKET = "left_curly_bracket"
    RIGHT_CURLY_BRACKET = "right_curly_bracket"
    LEFT_SQUARE_BRACKET = "left_square_bracket"
    RIGHT_SQUARE_BRACKET = "right_square_bracket"
    COMMA = "comma"
    DOT = "dot"
    MINUS = "minus"
    PLUS = "plus"
    SEMICOLON = "semicolon"
    SLASH = "slash"
    STAR = "star"
    # One or two character tokens
    BANG = "bang"
    BANG_EQUAL = "bang_equal"
    EQUAL = "equal"
    EQUAL_EQUAL = "equal_equal"
    GREATER = "greater"
    GREATER_EQUAL = "greater_equal"
    LESS = "less"
    LESS_EQUAL = "less_equal"
    # Literals
    IDENTIFIER = "identifier"
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    # Keywords
    AND = "and"
    ELIF = "elif"
    ELSE = "else"
    FALSE = "false"
    FOR = "for"
    IF = "if"
    IN = "in"
    LET = "let"
    MATCH = "match"
    NOTHING = "nothing"
    OR = "or"
    RETURN = "return"
    STRUCT = "struct"
    TRUE = "true"
    WHILE = "while"
    YIELD = "yield"
    # Comments
    COMMENT = "comment"
    # Other
    EOF = "eof"
