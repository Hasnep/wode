from typing import Any, List

from wode.ast import (
    BinaryExpression,
    Expression,
    GroupingExpression,
    LiteralExpression,
    UnaryExpression,
)
from wode.token_type import TokenType

SExpression = str | List[Any]


def convert_to_s_expression(expression: Expression) -> SExpression:
    match expression:
        case BinaryExpression():
            return [
                expression.operator.lexeme,
                convert_to_s_expression(expression.left),
                convert_to_s_expression(expression.right),
            ]
        case GroupingExpression():
            return ["group", convert_to_s_expression(expression.expression)]
        case LiteralExpression():
            match expression.literal.token_type:
                case TokenType.FALSE:
                    return "false"
                case TokenType.TRUE:
                    return "true"
                case TokenType.NOTHING:
                    return "nothing"
                case TokenType.INTEGER | TokenType.FLOAT:
                    value = expression.literal.lexeme
                    return value
                case TokenType.STRING:
                    value = expression.literal.lexeme
                    return '"' + value + '"'
                case TokenType.IDENTIFIER:
                    value = expression.literal.lexeme
                    return value
                case _:
                    raise ValueError(
                        f"Unknown token type `{expression.literal.token_type}`."
                    )
        case UnaryExpression():
            return [
                expression.operator.lexeme,
                convert_to_s_expression(expression.right),
            ]
        case _:
            raise ValueError(f"Unknown expression type `{type(expression)}`.")
