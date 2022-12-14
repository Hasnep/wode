from dataclasses import dataclass
from typing import List, Tuple

from koda import Err, Ok, Result

from wode.ast import BinaryExpression, Expression, LiteralExpression, UnaryExpression
from wode.errors import WodeError, WodeErrorType
from wode.token import Token
from wode.token_type import TokenType


@dataclass
class ParserState:
    _all_tokens: List[Token]
    source: str
    position: int = 0

    def chomp(self) -> Tuple[Token, "ParserState"]:
        try:
            return self._all_tokens[self.position], ParserState(
                self._all_tokens, self.source, self.position + 1
            )
        except IndexError:
            return Token(TokenType.EOF, "", -1), ParserState(
                self._all_tokens, self.source, self.position + 1
            )

    def debug_dump(self) -> None:
        for i, token in enumerate(self._all_tokens):
            print(
                f"{i} {token.token_type}: {token.lexeme}{' <--' if i == self.position else ''}"
            )


def get_infix_binding_power(operator: TokenType) -> Tuple[float, float]:
    operator_binding_power_mapping = {
        TokenType.STAR: (8, 8.1),
        TokenType.SLASH: (8, 8.1),
        TokenType.PLUS: (7, 7.1),
        TokenType.MINUS: (7, 7.1),
        TokenType.AND: (6.1, 6),
        TokenType.OR: (5.1, 5),
    }
    try:
        return operator_binding_power_mapping[operator]
    except KeyError as err:
        raise KeyError(
            f"Couldn't find infix binding power for infix operator `{operator}`."
        ) from err


def get_prefix_binding_power(operator: TokenType) -> Tuple[None, float]:
    match operator:
        case TokenType.PLUS | TokenType.MINUS:
            return (None, 7.1)
        case TokenType.BANG:
            return (None, 5.1)
        case _:
            raise ValueError(f"Unknown binding power for prefix operator `{operator}`.")


def parse_expression(
    state: ParserState, minimum_binding_power: float
) -> Tuple[Result[Expression, WodeError], ParserState]:
    token, state = state.chomp()
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
            # Prefix plus or minus
            binding_power_left, binding_power_right = get_prefix_binding_power(
                token.token_type
            )
            rhs_result = parse_expression(state, binding_power_right)
            match rhs_result:
                case Ok(rhs), new_state:
                    lhs = UnaryExpression(token, rhs)
                    state = new_state
                case Err(err), new_state:
                    return Err(err), new_state
                case _:
                    raise ValueError("?????")
        case TokenType.SEMICOLON:
            return (
                Err(
                    WodeError(
                        WodeErrorType.UnexpectedEndOfExpressionError,
                        state.source,
                        token.position,
                    )
                ),
                state,
            )
        case _:
            return (
                Err(
                    WodeError(
                        WodeErrorType.UnexpectedTokenType,
                        state.source,
                        token.position - 1,
                    )
                ),
                state,
            )

    while True:
        token, new_state = state.chomp()
        match token.token_type:
            case TokenType.EOF:
                break
            case TokenType.SEMICOLON:
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
                # Don't consume the token yet, we don't know its binding power yet
                operator = token
                binding_power_left, binding_power_right = get_infix_binding_power(
                    operator.token_type
                )
                if binding_power_left < minimum_binding_power:
                    # Stop iterating if we have found an operator with lower binding power than the minimum
                    # We didn't consume the token yet in case this happened
                    break
                # Now we can consume the token
                state = new_state
                # If we found an infix operator, try to parse the right hand side
                rhs_result, state = parse_expression(state, binding_power_right)
                match rhs_result:
                    case Ok(rhs):
                        lhs = BinaryExpression(lhs, operator, rhs)
                    case Err(err):
                        return Err(err), state
            case _:
                state = new_state
                return (
                    Err(
                        WodeError(
                            WodeErrorType.UnexpectedTokenType,
                            state.source,
                            token.position,
                        )
                    ),
                    state,
                )

    return Ok(lhs), state


def parse_all(state: ParserState) -> Tuple[List[Expression], List[WodeError]]:
    expressions: List[Expression] = []
    errors: List[WodeError] = []

    while True:
        # If we see an EOF, stop parsing
        if state.chomp()[0].token_type == TokenType.EOF:
            return expressions, errors

        expression_result, state = parse_expression(state, minimum_binding_power=0)
        match expression_result:
            case Ok(expression):
                token, new_state = state.chomp()
                if token.token_type == TokenType.SEMICOLON:
                    state = new_state
                    expressions.append(expression)
                else:
                    # If we don't see a semicolon, raise an error
                    errors.append(
                        WodeError(
                            WodeErrorType.ExpectedSemicolonError,
                            state.source,
                            token.position - 1,
                        )
                    )
            case Err(err):
                errors.append(err)


class Parser:
    def __init__(self, tokens: List[Token], source: str):
        self.state = ParserState(tokens, source)

    def parse(self) -> Tuple[List[Expression], List[WodeError]]:
        return parse_all(self.state)
