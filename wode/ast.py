from dataclasses import dataclass

from wode.token import Token


@dataclass
class Expression:
    pass


@dataclass
class UnaryExpression(Expression):
    operator: Token
    right: Expression


@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: Token
    right: Expression


@dataclass
class LiteralExpression(Expression):
    literal: Token


@dataclass
class GroupingExpression(Expression):
    expression: Expression


@dataclass
class VariableExpression(Expression):
    token: Token


@dataclass
class CommentExpression(Expression):
    token: Token
