from wode.token_type import TokenType
from wode.types import Int, Str
from wode.utils import safe_substring


class Token:
    def __init__(
        self, token_type: TokenType, position: Int, length: Int, source: Str
    ) -> None:
        self.token_type = token_type
        self.position = position
        self.length = length
        self._source = source

    @property
    def lexeme(self) -> Str:
        return safe_substring(self._source, start=self.position, length=self.length)


class EOFToken(Token):
    def __init__(self, source: Str) -> None:
        super().__init__(TokenType.EOF, len(source), 0, source)
