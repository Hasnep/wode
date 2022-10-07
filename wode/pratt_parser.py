from typing import List, Tuple

from koda import Just, Maybe, nothing

from wode.ast import (  # GroupingExpr,; VariableExpr,
    BinaryExpr,
    Expr,
    LiteralExpr,
    UnaryExpr,
)
from wode.token import Token
from wode.token_type import TokenType


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.current_position: int = 0

    def peek(self) -> Token:
        print("peeking")
        try:
            return self.tokens[self.current_position]
        except IndexError:
            return Token(TokenType.EOF, "")

    # def look_ahead(self) -> Token:
    #     return self.tokens[self.current_position + 1]

    def advance(self) -> Token:
        token = self.peek()
        self.current_position += 1
        print(f"advancing to {self.current_position}")
        return token

    def expr(self) -> Expr:
        return self.expr_binding_power(0)

    def expr_binding_power(self, minimum_binding_power: float) -> Expr:
        print(f"another call with bp {minimum_binding_power}")
        token = self.advance()
        print(token)
        match token.token_type:
            case TokenType.INTEGER | TokenType.FLOAT:
                lhs = LiteralExpr(token)
            case TokenType.PLUS | TokenType.MINUS:
                binding_power_left, binding_power_right = self.get_prefix_binding_power(
                    token.token_type
                )
                rhs = self.expr_binding_power(binding_power_right)
                lhs = UnaryExpr(token, rhs)
            case _:
                raise ValueError(f"Unknown token type `{token.token_type}`.")

        while True:
            token = self.peek()
            print(token)
            match token.token_type:
                case TokenType.EOF:
                    break
                case TokenType.PLUS | TokenType.MINUS | TokenType.STAR | TokenType.SLASH:
                    operator = token
                case _:
                    raise ValueError(f"Unknown token type `{token.token_type}`.")

            maybe_binding_powers = self.get_infix_binding_power(operator.token_type)
            # Check if we found an infix operator
            match maybe_binding_powers:
                case Just((binding_power_left, binding_power_right)):
                    # Stop iterating if we have found an operator with lower binding power than the minimum
                    if binding_power_left < minimum_binding_power:
                        break

                    self.advance()  # We peeked at the operator, now we consume it
                    rhs = self.expr_binding_power(binding_power_right)
                    lhs = BinaryExpr(lhs, operator, rhs)
                    continue
                case _:
                    break

        print(f"returning {lhs}")
        return lhs

    def get_infix_binding_power(
        self, operator: TokenType
    ) -> Maybe[Tuple[float, float]]:
        match operator:
            case TokenType.PLUS | TokenType.MINUS:
                return Just((1, 1.1))
            case TokenType.STAR | TokenType.SLASH:
                return Just((3, 3.1))
            case _:
                return nothing

    def get_prefix_binding_power(self, operator: TokenType) -> Tuple[None, float]:
        match operator:
            case TokenType.PLUS | TokenType.MINUS:
                return (None, 5)
            case _:
                raise ValueError(
                    f"Unknown binding power for prefix operator `{operator}`."
                )
