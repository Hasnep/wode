# from koda import Err, Ok, Result

# from wode.go_ast import GoBinaryExpr, GoExpr, GoIntegerExpr, GoOperator
# from wode.parser import BinaryExpr, Expr, LiteralExpr
# from wode.token_type import TokenType


# def convert_operator(operator: TokenType) -> Result[GoOperator, str]:
#     match operator:
#         case TokenType.PLUS:
#             return Ok(GoOperator.PLUS)
#         case _:
#             return Err(f"Unknown operator type `{operator}`.")


# def convert_ast(expr: Expr) -> Result[GoExpr, str]:
#     match expr:
#         case BinaryExpr():
#             match convert_ast(expr.left), convert_operator(
#                 expr.operator.token_type
#             ), convert_ast(expr.right):
#                 case Ok(left), Ok(go_operator), Ok(right):
#                     return Ok(GoBinaryExpr(left, go_operator, right))
#                 case _, _, _:
#                     return Err("oh no")
#         case LiteralExpr():
#             match expr.literal.token_type:
#                 case TokenType.INTEGER:
#                     return Ok(GoIntegerExpr(expr.literal.lexeme))
#                 case _:
#                     return Err(f"Unknown literal type `{expr.literal.token_type}`.")
#         case _:
#             return Err(f"Unknown expression type `{type(expr)}`.")
