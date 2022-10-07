from dataclasses import dataclass

from wode.token import Token


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


@dataclass
class CommentExpr(Expr):
    token: Token
