from wode.ast import (
    BinaryExpression,
    Expression,
    GroupingExpression,
    LiteralExpression,
    UnaryExpression,
)
from wode.token_type import TokenType


class AstPrinter:
    def convert_to_s_expression(self, expression: Expression) -> str:
        match expression:
            case BinaryExpression():
                return self.parenthise(
                    expression.operator.lexeme, expression.left, expression.right
                )
            case GroupingExpression():
                return self.parenthise("group", expression.expression)
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
                        return value
                    case TokenType.IDENTIFIER:
                        value = expression.literal.lexeme
                        return value
                    case _:
                        raise ValueError(
                            f"Unknown token type `{expression.literal.token_type}`."
                        )
            case UnaryExpression():
                return self.parenthise(expression.operator.lexeme, expression.right)
            case _:
                raise ValueError(f"Unknown expression type `{type(expression)}`.")

    def parenthise(self, name: str, *expressions: Expression) -> str:
        sub_expressions = [self.convert_to_s_expression(e) for e in expressions]
        values_joined = " ".join(sub_expressions)
        return f"({name} {values_joined})"
