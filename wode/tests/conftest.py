from pathlib import Path
from textwrap import dedent
from typing import Dict, List, Optional

from wode.ast_to_s_expression import SExpression
from wode.errors import WodeErrorType
from wode.token import Token
from wode.token_type import TokenType

DATA_FOLDER = Path(".") / "data"


class WodeTestCase:
    def __init__(
        self,
        source: str,
        expected_tokens: List[Token] = [],
        expected_scanner_errors: List[WodeErrorType] = [],
        expected_ast: Optional[List[SExpression]] = None,
        broken: bool = False,
    ) -> None:
        self.source = dedent(source)
        self.expected_tokens = expected_tokens
        self.expected_errors = expected_scanner_errors
        self.expected_ast = expected_ast
        self.broken = broken


test_cases: Dict[str, Dict[str, WodeTestCase]] = {
    "null case": {
        # TODO: Allow parsing empty programs
        "null case": WodeTestCase(
            source="",
            expected_tokens=[],
            expected_ast=None,
        )
    },
    "comments": {
        "a comment": WodeTestCase(
            source="""
            # This is a comment
            """,
            expected_tokens=[],
            expected_ast=None,  # TODO: Allow parsing empty programs
        ),
        "multiple comments": WodeTestCase(
            source="""
            # Comment spanning
            # Multiple lines
            """,
            expected_tokens=[],
            expected_ast=None,
        ),
    },
    "numbers": {
        "an integer": WodeTestCase(
            source="""
            123;
            """,
            expected_tokens=[
                Token(TokenType.INTEGER, "123", -1),
                Token(TokenType.SEMICOLON, ";", -1),
            ],
            expected_ast=["123"],
        ),
        "a float": WodeTestCase(
            source="""
            123.456;
            """,
            expected_tokens=[
                Token(TokenType.FLOAT, "123.456", -1),
                Token(TokenType.SEMICOLON, ";", -1),
            ],
            expected_ast=["123.456"],
        ),
        "no leading zero": WodeTestCase(
            source="""
            .456;
            """,
            expected_scanner_errors=[WodeErrorType.NoLeadingZeroOnFloatError],
        ),
        "unterminated float": WodeTestCase(
            source="""
            123.;
            """,
            expected_scanner_errors=[WodeErrorType.UnterminatedFloatError],
        ),
        "too many decimal points": WodeTestCase(
            source="""
            123.456.789;
            """,
            expected_scanner_errors=[WodeErrorType.NoLeadingZeroOnFloatError],
        ),
    },
    "identifiers": {
        "an identifier": WodeTestCase(
            source="""
            foo;
            """,
            expected_tokens=[
                Token(TokenType.IDENTIFIER, "foo", -1),
                Token(TokenType.SEMICOLON, ";", -1),
            ],
            expected_ast=None,
        ),
        "a keyword": WodeTestCase(
            source="""
            nothing;
            """,
            expected_tokens=[
                Token(TokenType.NOTHING, "nothing", -1),
                Token(TokenType.SEMICOLON, ";", -1),
            ],
            expected_ast=["nothing"],
        ),
        "a boolean": WodeTestCase(
            source="""
            true;
            """,
            expected_tokens=[
                Token(TokenType.TRUE, "true", 0),
                Token(TokenType.SEMICOLON, ";", 5),
            ],
            expected_ast=["true"],
        ),
    },
    "string": {
        "a string": WodeTestCase(
            source="""
            "this is a string";
            """,
            expected_tokens=[
                Token(TokenType.STRING, "this is a string", -1),
                Token(TokenType.SEMICOLON, ";", -1),
            ],
            expected_ast=['"this is a string"'],
        ),
        "unexpected end of string": WodeTestCase(
            source="""
            "This is an un-terminated string
            """,
            expected_scanner_errors=[WodeErrorType.UnexpectedEndOfFileError],
            expected_ast=None,
        ),
        "a multiline string": WodeTestCase(
            source="""
            "This is a
            multiline string";
            """,
            expected_tokens=[
                Token(TokenType.STRING, "This is a\nmultiline string", -1),
                Token(TokenType.SEMICOLON, ";", -1),
            ],
            expected_ast=['"This is a\nmultiline string"'],
        ),
        "unexpected end of multiline string": WodeTestCase(
            source="""
            "This is an
            un-terminated multiline-string
            """,
            expected_scanner_errors=[WodeErrorType.UnexpectedEndOfFileError],
            expected_ast=None,
        ),
    },
    "expressions": {
        "a single expression": WodeTestCase(
            source="""
            123;
            """,
            expected_tokens=[
                Token(TokenType.INTEGER, "123", -1),
                Token(TokenType.SEMICOLON, ";", -1),
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
                Token(TokenType.INTEGER, "123", -1),
                Token(TokenType.SEMICOLON, ";", -1),
                Token(TokenType.INTEGER, "456", -1),
                Token(TokenType.SEMICOLON, ";", -1),
                Token(TokenType.INTEGER, "123", -1),
                Token(TokenType.SEMICOLON, ";", -1),
                Token(TokenType.INTEGER, "456", -1),
                Token(TokenType.SEMICOLON, ";", -1),
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
                Token(TokenType.STRING, "a string", -1),
                Token(TokenType.SEMICOLON, ";", -1),
                Token(TokenType.INTEGER, "123", -1),
                Token(TokenType.SEMICOLON, ";", -1),
                Token(TokenType.FLOAT, "123.456", -1),
                Token(TokenType.SEMICOLON, ";", -1),
                Token(TokenType.TRUE, "true", -1),
                Token(TokenType.SEMICOLON, ";", -1),
                Token(TokenType.FALSE, "false", -1),
                Token(TokenType.SEMICOLON, ";", -1),
                Token(TokenType.NOTHING, "nothing", -1),
                Token(TokenType.SEMICOLON, ";", -1),
            ],
            expected_ast=['"a string"', "123", "123.456", "true", "false", "nothing"],
        ),
    },
    "operators": {
        "just a plus": WodeTestCase(
            source="""
            +
            """,
            expected_tokens=[Token(TokenType.PLUS, "+", -1)],
            expected_ast=None,
        ),
        "two plusses": WodeTestCase(
            source="""
            ++
            """,
            expected_tokens=[
                Token(TokenType.PLUS, "+", -1),
                Token(TokenType.PLUS, "+", -1),
            ],
            expected_ast=None,
        ),
        "back to back single character operators": WodeTestCase(
            source="""
            */
            """,
            expected_tokens=[
                Token(TokenType.STAR, "*", -1),
                Token(TokenType.SLASH, "/", -1),
            ],
            expected_ast=None,
        ),
        "double character operator": WodeTestCase(
            source="""
            !=
            """,
            expected_tokens=[
                Token(TokenType.BANG_EQUAL, "!=", -1),
            ],
            expected_ast=None,
        ),
        "possibly ambiguous operators": WodeTestCase(
            source="""
            !=!
            """,
            expected_tokens=[
                Token(TokenType.BANG_EQUAL, "!=", -1),
                Token(TokenType.BANG, "!", -1),
            ],
            expected_ast=None,
        ),
        "triple character operator": WodeTestCase(
            source="""
            ...
            """,
            expected_tokens=[
                Token(TokenType.ELLIPSIS, "...", -1),
            ],
            expected_ast=None,
        ),
        "lots of operators": WodeTestCase(
            source="""
            !*+-/
            =<><=>===!=->=>
            """,
            expected_tokens=[
                Token(TokenType.BANG, "!", -1),
                Token(TokenType.STAR, "*", -1),
                Token(TokenType.PLUS, "+", -1),
                Token(TokenType.MINUS, "-", -1),
                Token(TokenType.SLASH, "/", -1),
                Token(TokenType.EQUAL, "=", -1),
                Token(TokenType.LESS, "<", -1),
                Token(TokenType.GREATER, ">", -1),
                Token(TokenType.LESS_EQUAL, "<=", -1),
                Token(TokenType.GREATER_EQUAL, ">=", -1),
                Token(TokenType.EQUAL_EQUAL, "==", -1),
                Token(TokenType.BANG_EQUAL, "!=", -1),
                Token(TokenType.SINGLE_ARROW, "->", -1),
                Token(TokenType.DOUBLE_ARROW, "=>", -1),
            ],
            expected_ast=None,
        ),
        "some brackets": WodeTestCase(
            source="""
            ()
            """,
            expected_tokens=[
                Token(TokenType.LEFT_BRACKET, "(", -1),
                Token(TokenType.RIGHT_BRACKET, ")", -1),
            ],
            expected_ast=None,
        ),
        "nested brackets": WodeTestCase(
            source="""
            [{()}]
            """,
            expected_tokens=[
                Token(TokenType.LEFT_SQUARE_BRACKET, "[", -1),
                Token(TokenType.LEFT_CURLY_BRACKET, "{", -1),
                Token(TokenType.LEFT_BRACKET, "(", -1),
                Token(TokenType.RIGHT_BRACKET, ")", -1),
                Token(TokenType.RIGHT_CURLY_BRACKET, "}", -1),
                Token(TokenType.RIGHT_SQUARE_BRACKET, "]", -1),
            ],
            expected_ast=None,
        ),
        "unary plus": WodeTestCase(
            source="""
            +1;
            """,
            expected_tokens=[
                Token(TokenType.PLUS, "+", -1),
                Token(TokenType.INTEGER, "1", -1),
                Token(TokenType.SEMICOLON, ";", -1),
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
                Token(TokenType.MINUS, "-", -1),
                Token(TokenType.INTEGER, "1", -1),
                Token(TokenType.SEMICOLON, ";", -1),
            ],
            expected_ast=[["-", "1"]],
        ),
        "string concatenation": WodeTestCase(
            source="""
            "A string" + "Another string";
            """,
            expected_tokens=[
                Token(TokenType.STRING, "A string", -1),
                Token(TokenType.PLUS, "+", -1),
                Token(TokenType.STRING, "Another string", -1),
                Token(TokenType.SEMICOLON, ";", -1),
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
                Token(TokenType.MINUS, "-", -1),
                Token(TokenType.INTEGER, "5", -1),
                Token(TokenType.MINUS, "-", -1),
                Token(TokenType.MINUS, "-", -1),
                Token(TokenType.INTEGER, "1", -1),
                Token(TokenType.SEMICOLON, ";", -1),
            ],
            expected_ast=[
                ["-", ["-", "5"], ["-", "1"]],
            ],
        ),
        "operator precedence": WodeTestCase(
            source="""
            1 + 2 * 3 - 4 / 5;
            """,
            expected_tokens=[
                Token(TokenType.INTEGER, "1", -1),
                Token(TokenType.PLUS, "+", -1),
                Token(TokenType.INTEGER, "2", -1),
                Token(TokenType.STAR, "*", -1),
                Token(TokenType.INTEGER, "3", -1),
                Token(TokenType.MINUS, "-", -1),
                Token(TokenType.INTEGER, "4", -1),
                Token(TokenType.SLASH, "/", -1),
                Token(TokenType.INTEGER, "5", -1),
                Token(TokenType.SEMICOLON, ";", -1),
            ],
            expected_ast=[
                ["-", ["+", "1", ["*", "2", "3"]], ["/", "4", "5"]],
            ],
        ),
        "boolean operator precedence": WodeTestCase(
            source="""
            true and false or true;
            """,
            expected_tokens=[
                Token(TokenType.TRUE, "true", -1),
                Token(TokenType.AND, "and", -1),
                Token(TokenType.FALSE, "false", -1),
                Token(TokenType.OR, "or", -1),
                Token(TokenType.TRUE, "true", -1),
                Token(TokenType.SEMICOLON, ";", -1),
            ],
            expected_ast=[["or", ["and", "true", "false"], "true"]],
        ),
        "operator precedence with brackets": WodeTestCase(
            broken=True,
            source="""
            -1*2+3/(4+5);
            """,
            expected_tokens=[
                Token(TokenType.MINUS, "-", -1),
                Token(TokenType.INTEGER, "1", -1),
                Token(TokenType.STAR, "*", -1),
                Token(TokenType.INTEGER, "2", -1),
                Token(TokenType.PLUS, "+", -1),
                Token(TokenType.INTEGER, "3", -1),
                Token(TokenType.SLASH, "/", -1),
                Token(TokenType.LEFT_BRACKET, "(", -1),
                Token(TokenType.INTEGER, "4", -1),
                Token(TokenType.PLUS, "+", -1),
                Token(TokenType.INTEGER, "5", -1),
                Token(TokenType.RIGHT_BRACKET, ")", -1),
                Token(TokenType.SEMICOLON, ";", -1),
            ],
            expected_ast=[
                ["+", ["*", ["-", "1"], "2"], ["/", "3", ["group", ["+", "4", "5"]]]]
            ],
        ),
    },
}


test_cases_flattened = [
    (f"{category} - {test_case_name}", test_case)
    for category, category_test_cases in test_cases.items()
    for test_case_name, test_case in category_test_cases.items()
]
