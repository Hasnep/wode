from wode.source import Source, SourceRange
from wode.token_type import TokenType
from wode.types import Str


class Token:
    def __init__(self, token_type: TokenType, source_range: SourceRange) -> None:
        self.token_type = token_type
        self.source_range = source_range

    @property
    def lexeme(self) -> Str:
        return self.source_range.lexeme


class EOFToken(Token):
    def __init__(self, source: Source) -> None:
        end_of_source_position = len(source.code)
        super().__init__(
            TokenType.EOF,
            SourceRange(source, end_of_source_position, end_of_source_position),
        )
