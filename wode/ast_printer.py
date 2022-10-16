from wode.ast import (
    BinaryExpression,
    Expression,
    GroupingExpression,
    LiteralExpression,
    UnaryExpression,
)
from wode.token_type import TokenType


def convert_to_s_expression(expression: Expression) -> str:
    match expression:
        case BinaryExpression():
            return add_brackets(
                expression.operator.lexeme, expression.left, expression.right
            )
        case GroupingExpression():
            return add_brackets("group", expression.expression)
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
            return add_brackets(expression.operator.lexeme, expression.right)
        case _:
            raise ValueError(f"Unknown expression type `{type(expression)}`.")


def add_brackets(name: str, *expressions: Expression) -> str:
    sub_expressions = [convert_to_s_expression(e) for e in expressions]
    values_joined = " ".join(sub_expressions)
    return f"({name} {values_joined})"
