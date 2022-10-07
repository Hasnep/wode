from wode.ast import BinaryExpr, Expr, GroupingExpr, LiteralExpr, UnaryExpr
from wode.token_type import TokenType


class AstPrinter:
    def convert_to_s_expression(self, expr: Expr) -> str:
        match expr:
            case BinaryExpr():
                return self.parenthise(expr.operator.lexeme, expr.left, expr.right)
            case GroupingExpr():
                return self.parenthise("group", expr.expression)
            case LiteralExpr():
                match expr.literal.token_type:
                    case TokenType.FALSE:
                        return "false"
                    case TokenType.TRUE:
                        return "true"
                    case TokenType.NOTHING:
                        return "nothing"
                    case TokenType.INTEGER | TokenType.FLOAT:
                        value = expr.literal.lexeme
                        if value is None:
                            raise ValueError(
                                f"Unknown value for token type `{expr.literal.token_type}`."
                            )
                        else:
                            return value
                    case _:
                        raise ValueError(
                            f"Unknown token type `{expr.literal.token_type}`."
                        )
            case UnaryExpr():
                return self.parenthise(expr.operator.lexeme, expr.right)
            case _:
                raise ValueError(f"Unknown expression type `{type(expr)}`.")

    def parenthise(self, name: str, *expressions: Expr) -> str:
        sub_expressions = [self.convert_to_s_expression(e) for e in expressions]
        values_joined = " ".join(sub_expressions)
        return f"({name} {values_joined})"
