# from typing import List

# from koda import Err, Ok, Result

# from wode.ast import (
#     BinaryExpr,
#     Expr,
#     GroupingExpr,
#     LiteralExpr,
#     UnaryExpr,
#     VariableExpr,
# )
# from wode.token import Token
# from wode.token_type import TokenType


# class Parser:
#     def __init__(self, tokens: List[Token]) -> None:
#         self.tokens = tokens
#         self.current = 0

#     def consume(self, token_type: TokenType, message: str) -> Result[Token, str]:
#         if self.check(token_type):
#             return Ok(self.advance())
#         else:
#             return Err(message + repr(self.peek()))

#     def match(self, token_types: List[TokenType]) -> bool:
#         for token_type in token_types:
#             if self.check(token_type):
#                 self.advance()
#                 return True
#         return False

#     def check(self, token_type: TokenType) -> bool:
#         if self.is_at_end():
#             return False
#         return self.peek().token_type == token_type

#     def advance(self) -> Token:
#         if not self.is_at_end():
#             self.current += 1
#         return self.previous()

#     def is_at_end(self) -> bool:
#         return self.peek().token_type == TokenType.EOF

#     def peek(self) -> Token:
#         return self.tokens[self.current]

#     def previous(self) -> Token:
#         return self.tokens[self.current - 1]

#     def expression(self) -> Expr:
#         return self.equality()

#     def equality(self) -> Expr:
#         expr = self.comparison()

#         while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
#             operator = self.previous()
#             right = self.comparison()
#             expr = BinaryExpr(expr, operator, right)

#         return expr

#     def comparison(self) -> Expr:
#         expr = self.term()

#         while self.match(
#             [
#                 TokenType.GREATER,
#                 TokenType.GREATER_EQUAL,
#                 TokenType.LESS,
#                 TokenType.LESS_EQUAL,
#             ]
#         ):
#             operator = self.previous()
#             right = self.term()
#             expr = BinaryExpr(expr, operator, right)

#         return expr

#     def term(self) -> Expr:
#         expr = self.factor()

#         while self.match([TokenType.MINUS, TokenType.PLUS]):
#             operator = self.previous()
#             right = self.factor()
#             expr = BinaryExpr(expr, operator, right)

#         return expr

#     def factor(self) -> Expr:
#         expr = self.unary()

#         while self.match([TokenType.SLASH, TokenType.STAR]):
#             operator = self.previous()
#             right = self.unary()
#             expr = BinaryExpr(expr, operator, right)

#         return expr

#     def unary(self) -> Expr:
#         if self.match([TokenType.BANG, TokenType.MINUS]):
#             operator = self.previous()
#             right = self.unary()
#             return UnaryExpr(operator, right)

#         return self.primary()

#     def primary(self) -> Expr:
#         if self.match([TokenType.FALSE]):
#             return LiteralExpr(self.previous())
#         if self.match([TokenType.TRUE]):
#             return LiteralExpr(self.previous())
#         if self.match([TokenType.NOTHING]):
#             return LiteralExpr(self.previous())

#         if self.match([TokenType.INTEGER, TokenType.FLOAT, TokenType.STRING]):
#             return LiteralExpr(self.previous())

#         if self.match([TokenType.IDENTIFIER]):
#             return VariableExpr(self.previous())

#         if self.match([TokenType.LEFT_PAREN]):
#             expr = self.expression()
#             self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
#             return GroupingExpr(expr)

#         raise Exception("Expected expression")

#     def parse(self) -> List[Expr]:
#         expressions: List[Expr] = []
#         while not self.is_at_end():
#             expr = self.expression()
#             self.consume(TokenType.SEMICOLON, "expect semicolon after expression.")
#             expressions.append(expr)
#         return expressions
