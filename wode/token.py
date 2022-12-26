from wode.token_type import TokenType
from wode.utils import safe_substring


class Token:
    def __init__(
        self, token_type: TokenType, position: int, length: int, source: str
    ) -> None:
        self.token_type = token_type
        self.position = position
        self.length = length
        self._source = source

    @property
    def lexeme(self) -> str:
        return safe_substring(self._source, begin=self.position, length=self.length)


class EOFToken(Token):
    def __init__(self, source: str) -> None:
        super().__init__(TokenType.EOF, len(source), 0, source)
