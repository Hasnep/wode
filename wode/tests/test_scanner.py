from typing import List, Tuple

import pytest
from koda import Err, Ok

from wode.scanner import Scanner
from wode.token import Token
from wode.token_type import TokenType

test_cases: List[Tuple[str, str, List[Token]]] = [
    ("null_case", "", []),
    ("just_a_plus", "+", [Token(TokenType.PLUS, "+")]),
    ("two_plusses", "++", [Token(TokenType.PLUS, "+"), Token(TokenType.PLUS, "+")]),
    (
        "some_brackets",
        "()",
        [Token(TokenType.LEFT_PAREN, "("), Token(TokenType.RIGHT_PAREN, ")")],
    ),
    (
        "brackets_inside_curly_bois",
        "{()}",
        [
            Token(TokenType.LEFT_BRACE, "{"),
            Token(TokenType.LEFT_PAREN, "("),
            Token(TokenType.RIGHT_PAREN, ")"),
            Token(TokenType.RIGHT_BRACE, "}"),
        ],
    ),
    (
        "back_to_back_single_character_operators",
        "*/",
        [Token(TokenType.STAR, "*"), Token(TokenType.SLASH, "/")],
    ),
    (
        "two_character_operator",
        "!=",
        [Token(TokenType.BANG_EQUAL, "!=")],
    ),
    (
        "possibly_ambiguous_operators",
        "!=!",
        [Token(TokenType.BANG_EQUAL, "!="), Token(TokenType.BANG, "!")],
    ),
    (
        "lots_of_operators",
        "!*+-/\n=<><=>===!=",
        [
            Token(TokenType.BANG, "!"),
            Token(TokenType.STAR, "*"),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.SLASH, "/"),
            Token(TokenType.EQUAL, "="),
            Token(TokenType.LESS, "<"),
            Token(TokenType.GREATER, ">"),
            Token(TokenType.LESS_EQUAL, "<="),
            Token(TokenType.GREATER_EQUAL, ">="),
            Token(TokenType.EQUAL_EQUAL, "=="),
            Token(TokenType.BANG_EQUAL, "!="),
        ],
    ),
    (
        "just_a_comment",
        "# This is a comment",
        [Token(TokenType.COMMENT, "# This is a comment")],
    ),
    (
        "multiple_comments",
        "# Comment spanning\n# Multiple lines",
        [
            Token(TokenType.COMMENT, "# Comment spanning"),
            Token(TokenType.COMMENT, "# Multiple lines"),
        ],
    ),
    ("just_a_string", '"A string"', [Token(TokenType.STRING, '"A string"')]),
    (
        "string_concatenation",
        '"A string" + "Another string"',
        [
            Token(TokenType.STRING, '"A string"'),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.STRING, '"Another string"'),
        ],
    ),
]


@pytest.mark.parametrize(
    ",".join(["test_case_name", "source", "expected_tokens"]), test_cases
)
def test_scanner_on_example_files(
    test_case_name: str, source: str, expected_tokens: List[Token]
):
    tokens_result = Scanner(source).scan()
    match tokens_result:
        case Ok(tokens):
            assert tokens == [
                *expected_tokens,
                Token(TokenType.EOF, ""),
            ], test_case_name
        case Err(wode_errors):
            for e in wode_errors:
                raise Exception(e.message)
