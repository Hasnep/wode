from wode.ast import BinaryExpression, Expression, LiteralExpression
from wode.go_ast import (
    GoBinaryExpression,
    GoExpression,
    GoIntegerExpression,
    GoLiteralExpression,
    GoOperator,
    GoStringExpression,
)
from wode.token_type import TokenType


def transpile_operator(operator: TokenType) -> GoOperator:
    return {
        TokenType.PLUS: GoOperator.PLUS,
        TokenType.MINUS: GoOperator.MINUS,
        TokenType.SLASH: GoOperator.SLASH,
        TokenType.STAR: GoOperator.STAR,
        TokenType.AND: GoOperator.AND,
        TokenType.OR: GoOperator.OR,
    }[operator]


def transpile_expression(expression: Expression) -> GoExpression:
    match expression:
        case BinaryExpression(left, operator, right):
            return GoBinaryExpression(
                transpile_expression(left),
                transpile_operator(operator.token_type),
                transpile_expression(right),
            )
        case LiteralExpression(literal):
            match literal.token_type:
                case TokenType.INTEGER | TokenType.FLOAT:
                    return GoIntegerExpression(literal.lexeme)
                case TokenType.STRING:
                    return GoStringExpression(literal.lexeme)
                case TokenType.TRUE:
                    return GoLiteralExpression("true")
                case TokenType.FALSE:
                    return GoLiteralExpression("false")
                case TokenType.NOTHING:
                    return GoLiteralExpression("nil")
                case _:
                    raise Exception(
                        f"Unknown literal type `{expression.literal.token_type}`."
                    )
        case _:
            raise Exception(f"Unknown expression type `{type(expression)}`.")
