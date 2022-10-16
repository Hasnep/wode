import pytest

from wode.ast import (
    BinaryExpression,
    Expression,
    GroupingExpression,
    LiteralExpression,
    UnaryExpression,
)
from wode.ast_printer import AstPrinter
from wode.token import Token
from wode.token_type import TokenType


@pytest.mark.parametrize(
    ",".join(["expression", "expected_rendered_expression"]),
    [
        (LiteralExpression(Token(TokenType.INTEGER, "123", -1)), "123"),
        (LiteralExpression(Token(TokenType.FLOAT, "456.789", -1)), "456.789"),
        (
            GroupingExpression(
                LiteralExpression(Token(TokenType.FLOAT, "456.789", -1))
            ),
            "(group 456.789)",
        ),
        (
            UnaryExpression(
                Token(TokenType.MINUS, "-", -1),
                LiteralExpression(Token(TokenType.INTEGER, "123", -1)),
            ),
            "(- 123)",
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
            "(* (- 123) (group 456.789))",
        ),
    ],
)
def test_ast_printer_prints_expressions_correctly(
    expression: Expression, expected_rendered_expression: str
):
    assert (
        AstPrinter().convert_to_s_expression(expression) == expected_rendered_expression
    )
