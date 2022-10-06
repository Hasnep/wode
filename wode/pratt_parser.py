from typing import List, Tuple

from koda import Err, Ok, Result

from wode.ast import (
    BinaryExpr,
    Expr,
    GroupingExpr,
    LiteralExpr,
    UnaryExpr,
    VariableExpr,
)
from wode.token import Token
from wode.token_type import TokenType


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.current_position: int = 0

    def peek(self) -> Token:
        print("peeking")
        return self.tokens[self.current_position]

    def look_ahead(self) -> Token:
        return self.tokens[self.current_position + 1]

    def advance(self) -> None:
        self.current_position += 1
        print(f"advancing to {self.current_position}")

    def expr_binding_power(self, minimum_binding_power: float) -> Expr:
        token = self.peek()
        print(token)
        match token.token_type:
            case TokenType.INTEGER | TokenType.FLOAT:
                lhs = LiteralExpr(token)
            case _:
                raise ValueError(f"Unknown token type `{token.token_type}`.")

        while True:
            self.advance()
            token = self.peek()
            print(token)
            match token.token_type:
                case TokenType.EOF:
                    break
                case TokenType.PLUS:
                    operator = token
                case _:
                    raise ValueError(f"Unknown token type `{token.token_type}`.")

            binding_power_left, binding_power_right = self.get_infix_binding_power(
                operator.token_type
            )
            if binding_power_left < minimum_binding_power:
                break

            self.advance()
            rhs = self.expr_binding_power(binding_power_right)
            lhs = BinaryExpr(lhs, operator, rhs)

        return lhs

    def get_infix_binding_power(self, operator: TokenType) -> Tuple[float, float]:
        match operator:
            case TokenType.PLUS | TokenType.MINUS:
                return (1, 1.1)
            case TokenType.STAR | TokenType.SLASH:
                return (3, 3.1)
            case _:
                raise ValueError(f"Unknown binding power for operator `{operator}`.")
