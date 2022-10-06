# from dataclasses import dataclass
# from enum import Enum
# from typing import List

# from koda import Err, Ok, Result, mapping_get

# from wode.utils import flatten, get_errs


# class GoOperator(Enum):
#     PLUS = "+"
#     MINUS = "-"
#     STAR = "*"
#     SLASH = "/"


# @dataclass
# class GoExpr:
#     pass


# @dataclass
# class GoCommentExpr(GoExpr):
#     text: str


# @dataclass
# class GoStringExpr(GoExpr):
#     text: str


# @dataclass
# class GoIntegerExpr(GoExpr):
#     value: str


# @dataclass
# class GoUnaryExpr(GoExpr):
#     operator: GoOperator
#     x: GoExpr


# @dataclass
# class GoBinaryExpr(GoExpr):
#     left: GoExpr
#     operator: GoOperator
#     right: GoExpr


# def unparse_go_operator(go_operator: GoOperator) -> Result[str, str]:
#     operator_mapping = {GoOperator.PLUS: "+"}
#     return mapping_get(operator_mapping, go_operator).to_result(
#         f"Unknown Go operator `{go_operator}`."
#     )


# def unparse_go_expression(go_expr: GoExpr) -> Result[str, List[str]]:
#     match go_expr:
#         case GoCommentExpr():
#             return Ok(f"// {go_expr.text}")
#         case GoStringExpr():
#             return Ok(f'"{go_expr.text}"')
#         case GoUnaryExpr():
#             return Ok(f"{go_expr.operator}{go_expr.x}")
#         case GoBinaryExpr():
#             match (
#                 unparse_go_expression(go_expr.left),
#                 unparse_go_operator(go_expr.operator),
#                 unparse_go_expression(go_expr.right),
#             ):
#                 case Ok(left), Ok(operator), Ok(right):
#                     return Ok(f"{left} {operator} {right}")
#                 case left, operator, right:
#                     return Err(flatten(get_errs(left, operator, right)))
#         case GoIntegerExpr():
#             return Ok(go_expr.value)
#         case _:
#             return Err([f"Unknown expression type `{type(go_expr)}`."])
