from dataclasses import dataclass

from wode.token_type import TokenType


@dataclass
class Token:
    token_type: TokenType
    lexeme: str
