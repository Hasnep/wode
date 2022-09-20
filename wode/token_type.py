from enum import Enum


class TokenType(Enum):
    #  Single-character tokens
    LEFT_PAREN = "left_paren"
    RIGHT_PAREN = "right_paren"
    LEFT_BRACE = "left_brace"
    RIGHT_BRACE = "right_brace"
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
    NUMBER = "number"
    # Keywords
    AND = "and"
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FUN = "fun"
    FOR = "for"
    IF = "if"
    NIL = "nil"
    OR = "or"
    PRINT = "print"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    VAR = "var"
    WHILE = "while"
    # Comments
    COMMENT = "comment"
    # Other
    EOF = "eof"
