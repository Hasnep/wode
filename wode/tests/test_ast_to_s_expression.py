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
        (LiteralExpression(Token(TokenType.INTEGER, "123", -1)), "123"),
        (LiteralExpression(Token(TokenType.FLOAT, "456.789", -1)), "456.789"),
        (
            GroupingExpression(
                LiteralExpression(Token(TokenType.FLOAT, "456.789", -1))
            ),
            ["group", "456.789"],
        ),
        (
            UnaryExpression(
                Token(TokenType.MINUS, "-", -1),
                LiteralExpression(Token(TokenType.INTEGER, "123", -1)),
            ),
            ["-", "123"],
        ),
        (
            BinaryExpression(
                UnaryExpression(
                    Token(TokenType.MINUS, "-", -1),
                    LiteralExpression(Token(TokenType.INTEGER, "123", -1)),
                ),
                Token(TokenType.STAR, "*", -1),
                GroupingExpression(
                    LiteralExpression(Token(TokenType.FLOAT, "456.789", -1))
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
