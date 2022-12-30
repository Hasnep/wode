from abc import ABC as AbstractBaseClass
from abc import abstractmethod

from wode.token_type import TokenType
from wode.types import Float, Int, Literal, Optional, Tuple
from wode.utils import UnreachableError


class BindingPower(AbstractBaseClass):
    def __init__(
        self,
        token_type: TokenType,
        operator_type: Literal["prefix", "infix", "postfix"],
        binding_power: Int,
    ) -> None:
        self.token_type = token_type
        self.operator_type = operator_type
        self.binding_power = Float(binding_power)

    @abstractmethod
    def left_right(self) -> Tuple[Optional[Float], Optional[Float]]:
        pass


class PrefixBindingPower(BindingPower):
    def __init__(self, token_type: TokenType, binding_power: Int) -> None:
        super().__init__(token_type, "prefix", binding_power)

    def left_right(self) -> Tuple[None, Float]:
        return (None, self.binding_power)


class PostfixBindingPower(BindingPower):
    def __init__(self, token_type: TokenType, binding_power: Int) -> None:
        super().__init__(token_type, "postfix", binding_power)

    def left_right(self) -> Tuple[Float, None]:
        return (self.binding_power, None)


class InfixBindingPower(BindingPower):
    def __init__(
        self,
        token_type: TokenType,
        binding_power: Int,
        associativity: Literal["left", "right"],
    ) -> None:
        super().__init__(token_type, "infix", binding_power)
        self.associativity = associativity

    def left_right(self) -> Tuple[Float, Float]:
        match self.associativity:
            case "left":
                return (self.binding_power, self.binding_power + 0.1)
            case "right":
                return (self.binding_power + 0.1, self.binding_power)
            case _:
                raise UnreachableError(
                    "Infix operators can only be left or right associative."
                )


OPERATOR_BINDING_POWERS = [
    # Exponentiation
    InfixBindingPower(TokenType.CARET, 9, "right"),
    # Unary
    PrefixBindingPower(TokenType.PLUS, 8),
    PrefixBindingPower(TokenType.MINUS, 8),
    # Multiplication
    InfixBindingPower(TokenType.STAR, 7, "left"),
    InfixBindingPower(TokenType.SLASH, 7, "left"),
    # Addition
    InfixBindingPower(TokenType.PLUS, 6, "left"),
    InfixBindingPower(TokenType.MINUS, 6, "left"),
    # Pipe
    InfixBindingPower(TokenType.PIPE, 5, "left"),
    # Binary operators
    PrefixBindingPower(TokenType.BANG, 4),
    InfixBindingPower(TokenType.AMPERSAND_AMPERSAND, 3, "right"),
    InfixBindingPower(TokenType.BAR_BAR, 2, "right"),
    # Assignment
    InfixBindingPower(TokenType.EQUAL, 1, "right"),
]


def get_infix_binding_power(operator: TokenType) -> Tuple[Float, Float]:
    try:
        return next(
            obp
            for obp in OPERATOR_BINDING_POWERS
            if isinstance(obp, InfixBindingPower) and obp.token_type == operator
        ).left_right()
    except StopIteration:
        raise ValueError(
            f"Couldn't find binding power for infix operator `{operator}`."
        )


def get_prefix_binding_power(operator: TokenType) -> Tuple[None, Float]:
    try:
        return next(
            obp
            for obp in OPERATOR_BINDING_POWERS
            if isinstance(obp, PrefixBindingPower) and obp.token_type == operator
        ).left_right()
    except StopIteration:
        raise ValueError(
            f"Couldn't find binding power for prefix operator `{operator}`."
        )
