from typing import List, Tuple

from koda import Err, Just, Maybe, Ok, Result, mapping_get

from wode.ast import BinaryExpression, Expression, LiteralExpression, UnaryExpression
from wode.errors import WodeError, WodeErrorType
from wode.token import Token
from wode.token_type import TokenType


class Parser:
    def __init__(self, tokens: List[Token], source: str) -> None:
        self.tokens = tokens
        self.source = source
        self.current_position: int = 0

    def peek(self) -> Token:
        try:
            return self.tokens[self.current_position]
        except IndexError:
            return Token(TokenType.EOF, "", -1)

    def advance(self) -> Token:
        token = self.peek()
        self.current_position += 1
        return token

    def parse_all(self) -> Tuple[List[Expression], List[WodeError]]:
        expressions: List[Expression] = []
        errors: List[WodeError] = []

        token = self.peek()
        while token.token_type != TokenType.EOF:
            expression_result = self.parse_expression(minimum_binding_power=0)
            match expression_result:
                case Ok(expression):
                    expressions.append(expression)
                case Err(err):
                    errors.append(err)
            token = self.peek()
        return expressions, errors

    def parse_expression(
        self, minimum_binding_power: float
    ) -> Result[Expression, WodeError]:
        token = self.advance()
        match token.token_type:
            case (
                TokenType.INTEGER
                | TokenType.FLOAT
                | TokenType.STRING
                | TokenType.IDENTIFIER
                | TokenType.TRUE
                | TokenType.FALSE
                | TokenType.NOTHING
            ):
                lhs = LiteralExpression(token)
            case TokenType.PLUS | TokenType.MINUS:
                binding_power_left, binding_power_right = self.get_prefix_binding_power(
                    token.token_type
                )
                rhs_result = self.parse_expression(binding_power_right)
                match rhs_result:
                    case Ok(rhs):
                        lhs = UnaryExpression(token, rhs)
                    case Err(err):
                        return Err(err)
            case TokenType.SEMICOLON:
                return Err(
                    WodeError(
                        WodeErrorType.UnexpectedEndOfExpressionError,
                        self.source,
                        token.position,
                    )
                )
            case _:
                return Err(
                    WodeError(
                        WodeErrorType.UnexpectedTokenType,
                        self.source,
                        token.position,
                    )
                )

        while True:
            token = self.peek()
            match token.token_type:
                case TokenType.EOF:
                    break
                case TokenType.SEMICOLON:
                    # Consume the semicolon
                    self.advance()
                    # Finish parsing this expression
                    break
                case (
                    TokenType.PLUS
                    | TokenType.MINUS
                    | TokenType.STAR
                    | TokenType.SLASH
                    | TokenType.AND
                    | TokenType.OR
                ):
                    operator = token
                case _:
                    return Err(
                        WodeError(
                            WodeErrorType.UnexpectedTokenType,
                            self.source,
                            token.position,
                        )
                    )

            maybe_infix_binding_powers = self.get_infix_binding_power(
                operator.token_type
            )
            # Check if we found an infix operator
            match maybe_infix_binding_powers:
                case Just((binding_power_left, binding_power_right)):
                    # Stop iterating if we have found an operator with lower binding power than the minimum
                    if binding_power_left < minimum_binding_power:
                        break

                    # We peeked at the operator earlier, now we consume it
                    self.advance()
                    # If we found an infix operator, try to parse the right hand side
                    rhs_result = self.parse_expression(binding_power_right)
                    match rhs_result:
                        case Ok(rhs):
                            lhs = BinaryExpression(lhs, operator, rhs)
                            continue
                        case Err(err):
                            return Err(err)
                # If we didn't find an infix operator, keep parsing
                case _:
                    pass

        return Ok(lhs)

    def get_infix_binding_power(
        self, operator: TokenType
    ) -> Maybe[Tuple[float, float]]:
        operator_binding_power_mapping = {
            TokenType.STAR: (8, 8.1),
            TokenType.SLASH: (8, 8.1),
            TokenType.PLUS: (7, 7.1),
            TokenType.MINUS: (7, 7.1),
            TokenType.AND: (6.1, 6),
            TokenType.OR: (5.1, 5),
        }
        return mapping_get(operator_binding_power_mapping, operator)

    def get_prefix_binding_power(self, operator: TokenType) -> Tuple[None, float]:
        match operator:
            case TokenType.PLUS | TokenType.MINUS:
                return (None, 7.1)
            case TokenType.BANG:
                return (None, 5.1)
            case _:
                raise ValueError(
                    f"Unknown binding power for prefix operator `{operator}`."
                )
