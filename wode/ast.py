from dataclasses import dataclass
from typing import List

from koda import Err, Ok, Result

from wode.token import Token
from wode.token_type import TokenType


@dataclass
class Expr:
    pass


@dataclass
class UnaryExpr(Expr):
    operator: Token
    right: Expr


@dataclass
class BinaryExpr(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass
class LiteralExpr(Expr):
    literal: Token


@dataclass
class GroupingExpr(Expr):
    expression: Expr


@dataclass
class VariableExpr(Expr):
    token: Token
