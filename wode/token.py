from dataclasses import dataclass
from typing import Optional

from wode.token_type import TokenType


@dataclass
class Token:
    token_type: TokenType
    lexeme: str
    literal: Optional[str] = None

    def to_string(self) -> str:
        return f"{self.token_type} {self.lexeme} {self.literal}"
