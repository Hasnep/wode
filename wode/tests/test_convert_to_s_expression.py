import pytest

from wode.ast import (
    BinaryExpression,
    Expression,
    GroupingExpression,
    LiteralExpression,
    UnaryExpression,
)
from wode.ast_to_s_expression import convert_to_s_expression
from wode.source import Source, SourcePosition, SourceRange
from wode.token import Token
from wode.token_type import TokenType
from wode.types import Int, Str


def construct_token(
    source_code: Str,
    start: Int,
    end: Int,
    token_type: TokenType,
) -> Token:
    source = Source(None, source_code)
    source_range = SourceRange(
        source, SourcePosition(source, start), SourcePosition(source, end)
    )
    return Token(token_type, source_range)


@pytest.mark.parametrize(
    ",".join(["expression", "expected_s_expression"]),
    [
        (LiteralExpression(construct_token("123", 0, 3, TokenType.INTEGER)), "123"),
        (
            LiteralExpression(construct_token("456.789", 0, 7, TokenType.FLOAT)),
            "456.789",
        ),
        (
            GroupingExpression(
                LiteralExpression(construct_token("(456.789)", 1, 8, TokenType.FLOAT))
            ),
            ["group", "456.789"],
        ),
        (
            UnaryExpression(
                construct_token("-123", 0, 1, TokenType.MINUS),
                LiteralExpression(construct_token("-123", 1, 4, TokenType.INTEGER)),
            ),
            ["-", "123"],
        ),
        (
            BinaryExpression(
                UnaryExpression(
                    construct_token(
                        "-123*(456.789)",
                        0,
                        1,
                        TokenType.MINUS,
                    ),
                    LiteralExpression(
                        construct_token("-123*(456.789)", 1, 4, TokenType.INTEGER)
                    ),
                ),
                construct_token("-123*(456.789)", 4, 5, TokenType.STAR),
                GroupingExpression(
                    LiteralExpression(
                        construct_token("-123*(456.789)", 6, 13, TokenType.FLOAT)
                    )
                ),
            ),
            ["*", ["-", "123"], ["group", "456.789"]],
        ),
    ],
)
def test_converter_converts_expressions_to_s_expressions_correctly(
    expression: Expression, expected_s_expression: Str
):
    assert convert_to_s_expression(expression) == expected_s_expression
