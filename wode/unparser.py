from typing import List

from koda import Err, Ok, Result

from wode.go_ast import (
    GoBinaryExpression,
    GoExpression,
    GoIntegerExpression,
    GoLiteralExpression,
    GoOperator,
    GoStringExpression,
    GoUnaryExpression,
)

OPERATOR_MAPPING = {GoOperator.PLUS: "+", GoOperator.AND: "&&", GoOperator.OR: "||"}


def unparse_go_operator(go_operator: GoOperator) -> Result[str, str]:
    try:
        return Ok(OPERATOR_MAPPING[go_operator])
    except KeyError:
        return Err(f"Unable to convert Go operator `{go_operator}`.")


def unparse_go_expression(
    expression: GoExpression, is_top_level: bool
) -> Result[str, str]:
    match expression:
        case GoStringExpression():
            return Ok(("var _ = " if is_top_level else "") + f'"{expression.text}"')
        case GoUnaryExpression():
            return Ok(
                ("var _ = " if is_top_level else "")
                + f"({expression.operator}{expression.x})"
            )
        case GoBinaryExpression():
            match (
                unparse_go_expression(expression.left, False),
                unparse_go_operator(expression.operator),
                unparse_go_expression(expression.right, False),
            ):
                case Ok(left), Ok(operator), Ok(right):
                    return Ok(
                        ("var _ = " if is_top_level else "")
                        + f"({left} {operator} {right})"
                    )
                case left, operator, right:
                    abc = [x.val for x in [left, operator, right] if isinstance(x, Err)]
                    return Err("Unable to convert:\n" + "\n".join(abc))
        case GoIntegerExpression(value):
            return Ok(("var _ = " if is_top_level else "") + value)
        case GoLiteralExpression(value):
            return Ok(("var _ = " if is_top_level else "") + value)
        case _:
            return Err(f"Unknown expression type `{type(expression)}`.")


def unparse_all(expressions: List[GoExpression]) -> str:
    unparsed_expressions = [
        unparse_go_expression(e, is_top_level=True) for e in expressions
    ]
    if any(isinstance(e, Err) for e in unparsed_expressions):
        raise Exception()
    else:
        unparsed_expressions_str = [e.val for e in unparsed_expressions]
        return "\n".join(
            ["package main", "func main() {", *unparsed_expressions_str, "}"]
        )
