import pytest

from wode.ast import BinaryExpr, Expr, GroupingExpr, LiteralExpr, UnaryExpr
from wode.ast_printer import AstPrinter
from wode.token import Token
from wode.token_type import TokenType


@pytest.mark.parametrize(
    ",".join(["expression", "expected_rendered_expression"]),
    [
        (LiteralExpr(Token(TokenType.INTEGER, "123")), "123"),
        (LiteralExpr(Token(TokenType.FLOAT, "456.789")), "456.789"),
        (
            GroupingExpr(LiteralExpr(Token(TokenType.FLOAT, "456.789"))),
            "(group 456.789)",
        ),
        (
            UnaryExpr(
                Token(TokenType.MINUS, "-"),
                LiteralExpr(Token(TokenType.INTEGER, "123")),
            ),
            "(- 123)",
        ),
        (
            BinaryExpr(
                UnaryExpr(
                    Token(TokenType.MINUS, "-"),
                    LiteralExpr(Token(TokenType.INTEGER, "123")),
                ),
                Token(TokenType.STAR, "*"),
                GroupingExpr(LiteralExpr(Token(TokenType.FLOAT, "456.789"))),
            ),
            "(* (- 123) (group 456.789))",
        ),
    ],
)
def test_ast_printer_prints_expressions_correctly(
    expression: Expr, expected_rendered_expression: str
):
    ast_printer = AstPrinter()
    assert (
        ast_printer.convert_to_s_expression(expression) == expected_rendered_expression
    )
