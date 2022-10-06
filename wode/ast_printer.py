from typing import List

from koda import Err, Ok, Result

from wode.parser import BinaryExpr, Expr, GroupingExpr, LiteralExpr, UnaryExpr
from wode.token_type import TokenType
from wode.utils import combine_errs, get_errs, get_oks


class AstPrinter:
    def convert_to_s_expression(self, expr: Expr) -> Result[str, List[str]]:
        match expr:
            case BinaryExpr():
                return self.parenthise(expr.operator.lexeme, expr.left, expr.right)
            case GroupingExpr():
                return self.parenthise("group", expr.expression)
            case LiteralExpr():
                match expr.literal.token_type:
                    case TokenType.FALSE:
                        return Ok("false")
                    case TokenType.TRUE:
                        return Ok("true")
                    case TokenType.NOTHING:
                        return Ok("nothing")
                    case TokenType.INTEGER | TokenType.FLOAT:
                        value = expr.literal.lexeme
                        if value is None:
                            return Err(
                                [
                                    f"Unknown value for token type `{expr.literal.token_type}`."
                                ]
                            )
                        return Ok(value)
                    case _:
                        return Err([f"Unknown token type `{expr.literal.token_type}`."])
            case UnaryExpr():
                return self.parenthise(expr.operator.lexeme, expr.right)
            case _:
                return Err([f"Unknown expression type `{type(expr)}`."])

    def parenthise(self, name: str, *expressions: Expr) -> Result[str, List[str]]:
        sub_expressions_results = [self.convert_to_s_expression(e) for e in expressions]
        sub_expression_errs = get_errs(sub_expressions_results)
        if len(sub_expression_errs) > 0:
            return combine_errs(*sub_expression_errs)
        sub_expression_oks = get_oks(sub_expressions_results)
        sub_expression_values = [r.val for r in sub_expression_oks]
        values_joined = " ".join(sub_expression_values)
        return Ok(f"({name} {values_joined})")
