import pytest

from wode.ast import (
    BinaryExpression,
    Expression,
    GroupingExpression,
    LiteralExpression,
    UnaryExpression,
)
from wode.ast_to_s_expression import convert_to_s_expression
from wode.token import Token
from wode.token_type import TokenType


@pytest.mark.parametrize(
    ",".join(["expression", "expected_s_expression"]),
    [
        (LiteralExpression(Token(TokenType.INTEGER, 0, 3, "123")), "123"),
        (LiteralExpression(Token(TokenType.FLOAT, 0, 7, "456.789")), "456.789"),
        (
            GroupingExpression(
                LiteralExpression(Token(TokenType.FLOAT, 1, 7, "(456.789)"))
            ),
            ["group", "456.789"],
        ),
        (
            UnaryExpression(
                Token(TokenType.MINUS, 0, 1, "-123"),
                LiteralExpression(Token(TokenType.INTEGER, 1, 3, "-123")),
            ),
            ["-", "123"],
        ),
        (
            BinaryExpression(
                UnaryExpression(
                    Token(TokenType.MINUS, 0, 1, "-123*(456.789)"),
                    LiteralExpression(Token(TokenType.INTEGER, 1, 3, "-123*(456.789)")),
                ),
                Token(TokenType.STAR, 4, 1, "-123*(456.789)"),
                GroupingExpression(
                    LiteralExpression(Token(TokenType.FLOAT, 6, 7, "-123*(456.789)"))
                ),
            ),
            ["*", ["-", "123"], ["group", "456.789"]],
        ),
    ],
)
def test_converter_converts_expressions_to_s_expressions_correctly(
    expression: Expression, expected_s_expression: str
):
    assert convert_to_s_expression(expression) == expected_s_expression
