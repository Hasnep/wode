from pathlib import Path
from textwrap import dedent

from wode.ast_to_s_expression import SExpression
from wode.errors import (
    ExpectedSemicolonError,
    NoLeadingZeroOnFloatError,
    TooManyDecimalPointsError,
    UnexpectedEndOfExpressionError,
    UnexpectedEndOfFileError,
    UnexpectedTokenTypeError,
    UnknownCharacterError,
    UnterminatedFloatError,
    WodeError,
)
from wode.token_type import TokenType
from wode.types import Bool, List, NamedTuple, Str, Type

DATA_FOLDER = Path(".") / "data"


class SimplifiedToken(NamedTuple):
    token_type: TokenType
    lexeme: Str

    def __str__(self) -> Str:
        return f'({self.token_type}: "{self.lexeme}")'


class WodeTestCase:
    def __init__(
        self,
        test_case_id: Str,
        source: Str,
        expected_tokens: List[SimplifiedToken],
        expected_scanner_error_types: List[Type[WodeError]],
        expected_s_expressions: List[SExpression],
        expected_parser_error_types: List[Type[WodeError]],
        broken: Bool = False,
    ) -> None:
        self.test_case_id = test_case_id
        self.source = dedent(source)
        self.expected_tokens = expected_tokens + [SimplifiedToken(TokenType.EOF, "")]
        self.expected_scanner_error_types = expected_scanner_error_types
        self.expected_s_expressions = expected_s_expressions
        self.expected_parser_error_types = expected_parser_error_types
        self.broken = broken


test_cases = [
    # Null case
    WodeTestCase(
        "null case",
        source="",
        expected_tokens=[],
        expected_scanner_error_types=[],
        expected_s_expressions=[],
        expected_parser_error_types=[],
    ),
    # Comments
    WodeTestCase(
        "a comment",
        source="""
        # This is a comment
        """,
        expected_tokens=[],
        expected_scanner_error_types=[],
        expected_s_expressions=[],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "multiple comments",
        source="""
        # Comment spanning
        # Multiple lines
        """,
        expected_tokens=[],
        expected_scanner_error_types=[],
        expected_s_expressions=[],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "a comment without a terminating new line",
        source="""
        # Comment without a terminating new line
        """.rstrip(),
        expected_tokens=[],
        expected_scanner_error_types=[],
        expected_s_expressions=[],
        expected_parser_error_types=[],
    ),
    # Numbers
    WodeTestCase(
        "an integer",
        source="""
        123;
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.INTEGER, "123"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=["123"],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "a float",
        source="""
        123.456;
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.FLOAT, "123.456"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=["123.456"],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "an integer terminated by the end of the file",
        source="""
        123
        """.rstrip(),
        expected_tokens=[
            SimplifiedToken(TokenType.INTEGER, "123"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=[],
        expected_parser_error_types=[ExpectedSemicolonError],
    ),
    WodeTestCase(
        "a float terminated by the end of the file",
        source="""
        123.456
        """.rstrip(),
        expected_tokens=[
            SimplifiedToken(TokenType.FLOAT, "123.456"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=[],
        expected_parser_error_types=[ExpectedSemicolonError],
    ),
    WodeTestCase(
        "float with no leading zero",
        source="""
        .456;
        """,
        expected_scanner_error_types=[NoLeadingZeroOnFloatError],
        expected_tokens=[],
        expected_s_expressions=[],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "unterminated float",
        source="""
        123.;
        """,
        expected_tokens=[SimplifiedToken(TokenType.SEMICOLON, ";")],
        expected_scanner_error_types=[UnterminatedFloatError],
        expected_s_expressions=[],
        expected_parser_error_types=[UnexpectedEndOfExpressionError],
    ),
    WodeTestCase(
        "too many decimal points",
        source="""
        123.456.789;
        """,
        expected_tokens=[SimplifiedToken(TokenType.SEMICOLON, ";")],
        expected_scanner_error_types=[TooManyDecimalPointsError],
        expected_s_expressions=[],
        expected_parser_error_types=[UnexpectedEndOfExpressionError],
    ),
    # Identifiers
    WodeTestCase(
        "an identifier",
        source="""
        foo;
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.IDENTIFIER, "foo"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=["foo"],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "a keyword",
        source="""
        nothing;
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.NOTHING, "nothing"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=["nothing"],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "a boolean",
        source="""
        true;
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.TRUE, "true"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=["true"],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "an identifier without a terminating newline",
        source="""
        foo
        """.rstrip(),
        expected_tokens=[SimplifiedToken(TokenType.IDENTIFIER, "foo")],
        expected_scanner_error_types=[],
        expected_s_expressions=[],
        expected_parser_error_types=[ExpectedSemicolonError],
    ),
    # String
    WodeTestCase(
        "a string",
        source="""
        "This is a string";
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.STRING, "This is a string"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=['"This is a string"'],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "unexpected end of string",
        source="""
        "This is an un-terminated string
        """,
        expected_tokens=[],
        expected_scanner_error_types=[UnexpectedEndOfFileError],
        expected_s_expressions=[],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "a multiline string",
        source="""
        "This is a
        multiline string.";
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.STRING, "This is a\nmultiline string."),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=['"This is a\nmultiline string."'],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "unexpected end of multiline string",
        source="""
        "This is an
        un-terminated multiline-string.
        """,
        expected_tokens=[],
        expected_scanner_error_types=[UnexpectedEndOfFileError],
        expected_s_expressions=[],
        expected_parser_error_types=[],
    ),
    # Expressions
    WodeTestCase(
        "a single expression",
        source="""
        123;
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.INTEGER, "123"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=["123"],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "multiple expressions",
        source="""
        # On multiple lines
        123;
        456;
        # On the same line
        123; 456;
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.INTEGER, "123"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
            SimplifiedToken(TokenType.INTEGER, "456"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
            SimplifiedToken(TokenType.INTEGER, "123"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
            SimplifiedToken(TokenType.INTEGER, "456"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=["123", "456", "123", "456"],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "multiple expressions again",
        source="""
        "a string";
        123;
        123.456;
        true;
        false;
        nothing;
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.STRING, "a string"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
            SimplifiedToken(TokenType.INTEGER, "123"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
            SimplifiedToken(TokenType.FLOAT, "123.456"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
            SimplifiedToken(TokenType.TRUE, "true"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
            SimplifiedToken(TokenType.FALSE, "false"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
            SimplifiedToken(TokenType.NOTHING, "nothing"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=[
            '"a string"',
            "123",
            "123.456",
            "true",
            "false",
            "nothing",
        ],
        expected_parser_error_types=[],
    ),
    # Operators
    WodeTestCase(
        "just a plus",
        source="""
        +
        """,
        expected_tokens=[SimplifiedToken(TokenType.PLUS, "+")],
        expected_scanner_error_types=[],
        expected_s_expressions=[],
        expected_parser_error_types=[UnexpectedTokenTypeError],
    ),
    WodeTestCase(
        "two plusses",
        source="""
        ++
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.PLUS, "+"),
            SimplifiedToken(TokenType.PLUS, "+"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=[],
        expected_parser_error_types=[],
        broken=True,
    ),
    WodeTestCase(
        "double character operator",
        source="""
        !=
        """,
        expected_tokens=[SimplifiedToken(TokenType.BANG_EQUAL, "!=")],
        expected_scanner_error_types=[],
        expected_s_expressions=[],
        expected_parser_error_types=[UnexpectedTokenTypeError],
    ),
    WodeTestCase(
        "possibly ambiguous operators",
        source="""
        !=!
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.BANG_EQUAL, "!="),
            SimplifiedToken(TokenType.BANG, "!"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=[],
        expected_parser_error_types=[],
        broken=True,
    ),
    WodeTestCase(
        "triple character operator",
        source="""
        ...
        """,
        expected_tokens=[SimplifiedToken(TokenType.ELLIPSIS, "...")],
        expected_scanner_error_types=[],
        expected_s_expressions=[],
        expected_parser_error_types=[],
        broken=True,
    ),
    WodeTestCase(
        "lots of operators",
        source="""
        !*+-/
        =<><=>===!=->=>
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.BANG, "!"),
            SimplifiedToken(TokenType.STAR, "*"),
            SimplifiedToken(TokenType.PLUS, "+"),
            SimplifiedToken(TokenType.MINUS, "-"),
            SimplifiedToken(TokenType.SLASH, "/"),
            SimplifiedToken(TokenType.EQUAL, "="),
            SimplifiedToken(TokenType.LESS, "<"),
            SimplifiedToken(TokenType.GREATER, ">"),
            SimplifiedToken(TokenType.LESS_EQUAL, "<="),
            SimplifiedToken(TokenType.GREATER_EQUAL, ">="),
            SimplifiedToken(TokenType.EQUAL_EQUAL, "=="),
            SimplifiedToken(TokenType.BANG_EQUAL, "!="),
            SimplifiedToken(TokenType.SINGLE_ARROW, "->"),
            SimplifiedToken(TokenType.DOUBLE_ARROW, "=>"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=[],
        expected_parser_error_types=[],
        broken=True,
    ),
    WodeTestCase(
        "some brackets",
        source="""
        ()
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.LEFT_BRACKET, "("),
            SimplifiedToken(TokenType.RIGHT_BRACKET, ")"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=[],
        expected_parser_error_types=[
            UnexpectedTokenTypeError,
            UnexpectedTokenTypeError,
        ],
    ),
    WodeTestCase(
        "nested brackets",
        source="""
        [{()}]
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.LEFT_SQUARE_BRACKET, "["),
            SimplifiedToken(TokenType.LEFT_CURLY_BRACKET, "{"),
            SimplifiedToken(TokenType.LEFT_BRACKET, "("),
            SimplifiedToken(TokenType.RIGHT_BRACKET, ")"),
            SimplifiedToken(TokenType.RIGHT_CURLY_BRACKET, "}"),
            SimplifiedToken(TokenType.RIGHT_SQUARE_BRACKET, "]"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=[],
        expected_parser_error_types=[
            UnexpectedTokenTypeError,
            UnexpectedTokenTypeError,
            UnexpectedTokenTypeError,
            UnexpectedTokenTypeError,
            UnexpectedTokenTypeError,
            UnexpectedTokenTypeError,
        ],
    ),
    WodeTestCase(
        "unary plus",
        source="""
        +1;
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.PLUS, "+"),
            SimplifiedToken(TokenType.INTEGER, "1"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=[
            ["+", "1"],
        ],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "unary minus",
        source="""
        -1;
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.MINUS, "-"),
            SimplifiedToken(TokenType.INTEGER, "1"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=[
            ["-", "1"],
        ],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "string concatenation",
        source="""
        "A string" + "Another string";
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.STRING, "A string"),
            SimplifiedToken(TokenType.PLUS, "+"),
            SimplifiedToken(TokenType.STRING, "Another string"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=[
            ["+", '"A string"', '"Another string"'],
        ],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "both unary and binary operators",
        source="""
        -5--1;
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.MINUS, "-"),
            SimplifiedToken(TokenType.INTEGER, "5"),
            SimplifiedToken(TokenType.MINUS, "-"),
            SimplifiedToken(TokenType.MINUS, "-"),
            SimplifiedToken(TokenType.INTEGER, "1"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=[
            ["-", ["-", "5"], ["-", "1"]],
        ],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "operator precedence",
        source="""
        1 + 2 * 3 - 4 / 5 ^ 6;
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.INTEGER, "1"),
            SimplifiedToken(TokenType.PLUS, "+"),
            SimplifiedToken(TokenType.INTEGER, "2"),
            SimplifiedToken(TokenType.STAR, "*"),
            SimplifiedToken(TokenType.INTEGER, "3"),
            SimplifiedToken(TokenType.MINUS, "-"),
            SimplifiedToken(TokenType.INTEGER, "4"),
            SimplifiedToken(TokenType.SLASH, "/"),
            SimplifiedToken(TokenType.INTEGER, "5"),
            SimplifiedToken(TokenType.CARET, "^"),
            SimplifiedToken(TokenType.INTEGER, "6"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=[
            ["-", ["+", "1", ["*", "2", "3"]], ["/", "4", ["^", "5", "6"]]],
        ],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "boolean operator precedence",
        source="""
        true && false || true;
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.TRUE, "true"),
            SimplifiedToken(TokenType.AMPERSAND_AMPERSAND, "&&"),
            SimplifiedToken(TokenType.FALSE, "false"),
            SimplifiedToken(TokenType.BAR_BAR, "||"),
            SimplifiedToken(TokenType.TRUE, "true"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=[
            ["||", ["&&", "true", "false"], "true"],
        ],
        expected_parser_error_types=[],
    ),
    WodeTestCase(
        "operator precedence with brackets",
        source="""
        -1*2+3/(4+5)^6;
        """,
        expected_tokens=[
            SimplifiedToken(TokenType.MINUS, "-"),
            SimplifiedToken(TokenType.INTEGER, "1"),
            SimplifiedToken(TokenType.STAR, "*"),
            SimplifiedToken(TokenType.INTEGER, "2"),
            SimplifiedToken(TokenType.PLUS, "+"),
            SimplifiedToken(TokenType.INTEGER, "3"),
            SimplifiedToken(TokenType.SLASH, "/"),
            SimplifiedToken(TokenType.LEFT_BRACKET, "("),
            SimplifiedToken(TokenType.INTEGER, "4"),
            SimplifiedToken(TokenType.PLUS, "+"),
            SimplifiedToken(TokenType.INTEGER, "5"),
            SimplifiedToken(TokenType.RIGHT_BRACKET, ")"),
            SimplifiedToken(TokenType.CARET, "^"),
            SimplifiedToken(TokenType.INTEGER, "6"),
            SimplifiedToken(TokenType.SEMICOLON, ";"),
        ],
        expected_scanner_error_types=[],
        expected_s_expressions=[
            [
                "+",
                ["*", ["-", "1"], "2"],
                ["/", "3", ["^", ["group", ["+", "4", "5"]], "6"]],
            ],
        ],
        expected_parser_error_types=[],
        broken=True,
    ),
    # Erroring
    WodeTestCase(
        "an emoji",
        source="""
        😅;
        """,
        expected_tokens=[SimplifiedToken(TokenType.SEMICOLON, ";")],
        expected_scanner_error_types=[UnknownCharacterError],
        expected_s_expressions=[],
        expected_parser_error_types=[UnexpectedEndOfExpressionError],
    ),
]
