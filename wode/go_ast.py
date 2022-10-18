from dataclasses import dataclass
from enum import Enum


class GoOperator(Enum):
    PLUS = "plus"
    MINUS = "minus"
    STAR = "star"
    SLASH = "slash"
    AND = "and"
    OR = "or"


@dataclass
class GoStatement:
    pass


@dataclass
class GoImportStatement(GoStatement):
    module: str


@dataclass
class GoExpression:
    pass


@dataclass
class GoLetStatement(GoStatement):
    variable_name: str
    value: GoExpression


@dataclass
class GoConstantStatement(GoStatement):
    variable_name: str
    value: GoExpression


@dataclass
class GoPrintlnStatement(GoStatement):
    value: GoExpression


@dataclass
class GoCommentExpression(GoExpression):
    text: str


@dataclass
class GoStringExpression(GoExpression):
    text: str


@dataclass
class GoIntegerExpression(GoExpression):
    value: str


@dataclass
class GoLiteralExpression(GoExpression):
    value: str


@dataclass
class GoUnaryExpression(GoExpression):
    operator: GoOperator
    x: GoExpression


@dataclass
class GoBinaryExpression(GoExpression):
    left: GoExpression
    operator: GoOperator
    right: GoExpression
