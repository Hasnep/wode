from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

from wode.ast_to_s_expression import SExpression
from wode.errors import (
    NoLeadingZeroOnFloatError,
    TooManyDecimalPointsError,
    UnexpectedEndOfFileError,
    UnknownCharacterError,
    UnterminatedFloatError,
    WodeError,
)
from wode.token_type import TokenType
from wode.types import Bool, List, Optional, Str, Type

DATA_FOLDER = Path(".") / "data"


@dataclass
class SimplifiedToken:
    token_type: TokenType
    lexeme: Str


class WodeTestCase:
    def __init__(
        self,
        source: Str,
        expected_tokens: List[SimplifiedToken] = [],
        expected_scanner_error_types: List[Type[WodeError]] = [],
        expected_ast: Optional[List[SExpression]] = None,
        broken: Bool = False,
    ) -> None:
        if len(expected_tokens) > 0 and len(expected_scanner_error_types) > 0:
            raise ValueError(
                dedent(
                    f"""
                    Test case specified both
                    expected_tokens: {expected_tokens}
                    and
                    expected_scanner_error_types: {expected_scanner_error_types}
                    """
                )
            )  # pragma: no cover
        self.source = dedent(source)
        self.expected_tokens = expected_tokens
        self.expected_scanner_error_types = expected_scanner_error_types
        self.expected_ast = expected_ast
        self.broken = broken


test_cases = {
    "null case": {
        "null case": WodeTestCase(
            source="",
            expected_tokens=[],
            expected_ast=[],
        )
    },
    "comments": {
        "a comment": WodeTestCase(
            source="""
            # This is a comment
            """,
            expected_tokens=[],
            expected_ast=[],
        ),
        "multiple comments": WodeTestCase(
            source="""
            # Comment spanning
            # Multiple lines
            """,
            expected_tokens=[],
            expected_ast=[],
        ),
        "a comment without a terminating new line": WodeTestCase(
            source="""
            # Comment without a terminating new line
            """.rstrip(),
            expected_tokens=[],
            expected_ast=[],
        ),
    },
    "numbers": {
        "an integer": WodeTestCase(
            source="""
            123;
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.INTEGER, "123"),
                SimplifiedToken(TokenType.SEMICOLON, ";"),
            ],
            expected_ast=["123"],
        ),
        "a float": WodeTestCase(
            source="""
            123.456;
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.FLOAT, "123.456"),
                SimplifiedToken(TokenType.SEMICOLON, ";"),
            ],
            expected_ast=["123.456"],
        ),
        "an integer terminated by the end of the file": WodeTestCase(
            source="""
            123
            """.rstrip(),
            expected_tokens=[
                SimplifiedToken(TokenType.INTEGER, "123"),
            ],
        ),
        "a float terminated by the end of the file": WodeTestCase(
            source="""
            123.456
            """.rstrip(),
            expected_tokens=[
                SimplifiedToken(TokenType.FLOAT, "123.456"),
            ],
        ),
        "float with no leading zero": WodeTestCase(
            source="""
            .456;
            """,
            expected_scanner_error_types=[
                NoLeadingZeroOnFloatError,
            ],
        ),
        "unterminated float": WodeTestCase(
            source="""
            123.;
            """,
            expected_scanner_error_types=[
                UnterminatedFloatError,
            ],
        ),
        "too many decimal points": WodeTestCase(
            source="""
            123.456.789;
            """,
            expected_scanner_error_types=[
                TooManyDecimalPointsError,
            ],
        ),
    },
    "identifiers": {
        "an identifier": WodeTestCase(
            source="""
            foo;
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.IDENTIFIER, "foo"),
                SimplifiedToken(TokenType.SEMICOLON, ";"),
            ],
            expected_ast=[
                "foo",
            ],
        ),
        "a keyword": WodeTestCase(
            source="""
            nothing;
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.NOTHING, "nothing"),
                SimplifiedToken(TokenType.SEMICOLON, ";"),
            ],
            expected_ast=["nothing"],
        ),
        "a boolean": WodeTestCase(
            source="""
            true;
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.TRUE, "true"),
                SimplifiedToken(TokenType.SEMICOLON, ";"),
            ],
            expected_ast=["true"],
        ),
        "an identifier without a terminating newline": WodeTestCase(
            source="""
            foo
            """.rstrip(),
            expected_tokens=[
                SimplifiedToken(TokenType.IDENTIFIER, "foo"),
            ],
            expected_ast=None,
        ),
    },
    "string": {
        "a string": WodeTestCase(
            source="""
            "this is a string";
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.STRING, "this is a string"),
                SimplifiedToken(TokenType.SEMICOLON, ";"),
            ],
            expected_ast=['"this is a string"'],
        ),
        "unexpected end of string": WodeTestCase(
            source="""
            "This is an un-terminated string
            """,
            expected_scanner_error_types=[
                UnexpectedEndOfFileError,
            ],
            expected_ast=None,
        ),
        "a multiline string": WodeTestCase(
            source="""
            "This is a
            multiline string";
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.STRING, "This is a\nmultiline string"),
                SimplifiedToken(TokenType.SEMICOLON, ";"),
            ],
            expected_ast=['"This is a\nmultiline string"'],
        ),
        "unexpected end of multiline string": WodeTestCase(
            source="""
            "This is an
            un-terminated multiline-string
            """,
            expected_scanner_error_types=[
                UnexpectedEndOfFileError,
            ],
            expected_ast=None,
        ),
    },
    "expressions": {
        "a single expression": WodeTestCase(
            source="""
            123;
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.INTEGER, "123"),
                SimplifiedToken(TokenType.SEMICOLON, ";"),
            ],
            expected_ast=["123"],
        ),
        "multiple expressions": WodeTestCase(
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
            expected_ast=["123", "456", "123", "456"],
        ),
        "multiple expressions again": WodeTestCase(
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
            expected_ast=['"a string"', "123", "123.456", "true", "false", "nothing"],
        ),
    },
    "operators": {
        "just a plus": WodeTestCase(
            source="""
            +
            """,
            expected_tokens=[SimplifiedToken(TokenType.PLUS, "+")],
            expected_ast=None,
        ),
        "two plusses": WodeTestCase(
            source="""
            ++
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.PLUS, "+"),
                SimplifiedToken(TokenType.PLUS, "+"),
            ],
            expected_ast=None,
        ),
        "back to back single character operators": WodeTestCase(
            source="""
            */
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.STAR, "*"),
                SimplifiedToken(TokenType.SLASH, "/"),
            ],
            expected_ast=None,
        ),
        "double character operator": WodeTestCase(
            source="""
            !=
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.BANG_EQUAL, "!="),
            ],
            expected_ast=None,
        ),
        "possibly ambiguous operators": WodeTestCase(
            source="""
            !=!
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.BANG_EQUAL, "!="),
                SimplifiedToken(TokenType.BANG, "!"),
            ],
            expected_ast=None,
        ),
        "triple character operator": WodeTestCase(
            source="""
            ...
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.ELLIPSIS, "..."),
            ],
            expected_ast=None,
        ),
        "lots of operators": WodeTestCase(
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
            expected_ast=None,
        ),
        "some brackets": WodeTestCase(
            source="""
            ()
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.LEFT_BRACKET, "("),
                SimplifiedToken(TokenType.RIGHT_BRACKET, ")"),
            ],
            expected_ast=None,
        ),
        "nested brackets": WodeTestCase(
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
            expected_ast=None,
        ),
        "unary plus": WodeTestCase(
            source="""
            +1;
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.PLUS, "+"),
                SimplifiedToken(TokenType.INTEGER, "1"),
                SimplifiedToken(TokenType.SEMICOLON, ";"),
            ],
            expected_ast=[
                ["+", "1"],
            ],
        ),
        "unary minus": WodeTestCase(
            source="""
            -1;
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.MINUS, "-"),
                SimplifiedToken(TokenType.INTEGER, "1"),
                SimplifiedToken(TokenType.SEMICOLON, ";"),
            ],
            expected_ast=[["-", "1"]],
        ),
        "string concatenation": WodeTestCase(
            source="""
            "A string" + "Another string";
            """,
            expected_tokens=[
                SimplifiedToken(TokenType.STRING, "A string"),
                SimplifiedToken(TokenType.PLUS, "+"),
                SimplifiedToken(TokenType.STRING, "Another string"),
                SimplifiedToken(TokenType.SEMICOLON, ";"),
            ],
            expected_ast=[
                ["+", '"A string"', '"Another string"'],
            ],
        ),
        "both unary and binary operators": WodeTestCase(
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
            expected_ast=[
                ["-", ["-", "5"], ["-", "1"]],
            ],
        ),
        "operator precedence": WodeTestCase(
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
            expected_ast=[
                ["-", ["+", "1", ["*", "2", "3"]], ["/", "4", ["^", "5", "6"]]],
            ],
        ),
        "boolean operator precedence": WodeTestCase(
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
            expected_ast=[["||", ["&&", "true", "false"], "true"]],
        ),
        "operator precedence with brackets": WodeTestCase(
            broken=True,
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
            expected_ast=[
                [
                    "+",
                    ["*", ["-", "1"], "2"],
                    ["/", "3", ["^", ["group", ["+", "4", "5"]], "6"]],
                ]
            ],
        ),
    },
    "erroring": {
        "an emoji": WodeTestCase(
            broken=False,
            source="""
            😅;
            """,
            expected_scanner_error_types=[
                UnknownCharacterError,
            ],
        )
    },
}


test_cases_flattened = {
    f"{category} - {test_case_name}": test_case
    for category, category_test_cases in test_cases.items()
    for test_case_name, test_case in category_test_cases.items()
}
