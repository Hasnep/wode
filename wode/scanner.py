from typing import List

from koda import Err, Just, Maybe, Ok, Result, mapping_get, nothing

from .errors import WodeError, WodeErrorType
from .token import Token
from .token_type import TokenType

double_character_token_mapping = {
    "!=": TokenType.BANG_EQUAL,
    "==": TokenType.EQUAL_EQUAL,
    ">=": TokenType.GREATER_EQUAL,
    "<=": TokenType.LESS_EQUAL,
}
single_character_token_mapping = {
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
    "{": TokenType.LEFT_BRACE,
    "}": TokenType.RIGHT_BRACE,
    ",": TokenType.COMMA,
    ".": TokenType.DOT,
    "-": TokenType.MINUS,
    "+": TokenType.PLUS,
    ";": TokenType.SEMICOLON,
    "/": TokenType.SLASH,
    "*": TokenType.STAR,
    # Possibly double tokens
    "!": TokenType.BANG,
    "=": TokenType.EQUAL,
    ">": TokenType.GREATER,
    "<": TokenType.LESS,
}


class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.current_position: int = 0
        self.tokens: List[Token] = []

    def get_remaining_source(self) -> str:
        return self.source[self.current_position :]

    def is_at_end(self) -> bool:
        return self.current_position == len(self.source)

    def advance(self, by: int = 1) -> None:
        self.current_position += by

    def look_one(self) -> str:
        return self.source[self.current_position]

    def look_ahead(self) -> str:
        return self.source[self.current_position + 1]

    def scan_for_end_of_file_token(self) -> Maybe[Token]:
        if not self.is_at_end():
            return nothing

        return Just(Token(TokenType.EOF, ""))

    def scan_for_whitespace_token(self) -> Maybe[str]:
        first_character = self.get_remaining_source()[:1]
        if first_character not in [" ", "\t", "\n"]:
            return nothing

        return Just(first_character)

    def scan_for_comment_token(self) -> Maybe[Token]:
        if self.look_one() != "#":
            return nothing

        comment = ""
        while not self.is_at_end() and self.look_one() != "\n":
            comment += self.look_one()
            self.advance()
        return Just(Token(TokenType.COMMENT, comment))

    def scan_for_string_token(self) -> Result[Maybe[Token], WodeError]:
        if self.look_one() != '"':
            return Ok(nothing)

        n_quotation_marks_seen = 0
        string = ""
        while n_quotation_marks_seen < 2:
            if self.is_at_end():
                return Err(
                    WodeError(
                        WodeErrorType.UnexpectedEndOfFileError,
                        self.source,
                        self.current_position - 1,
                    )
                )
            if self.look_one() == '"':
                n_quotation_marks_seen += 1
            string += self.look_one()
            self.advance()
        return Ok(Just(Token(TokenType.STRING, string)))

    def scan_for_double_character_token(self) -> Maybe[Token]:
        lexeme = self.get_remaining_source()[:2]
        maybe_token_type = mapping_get(double_character_token_mapping, lexeme)
        maybe_token = maybe_token_type.map(lambda token_type: Token(token_type, lexeme))
        return maybe_token

    def scan_for_single_character_token(self) -> Maybe[Token]:
        lexeme = self.get_remaining_source()[:1]
        maybe_token_type = mapping_get(single_character_token_mapping, lexeme)
        maybe_token = maybe_token_type.map(lambda token_type: Token(token_type, lexeme))
        return maybe_token

    def scan_once(self) -> Result[Maybe[Token], WodeError]:
        match self.scan_for_end_of_file_token():
            case Just(end_of_file_token):
                return Ok(Just(end_of_file_token))
            case _:
                pass

        match self.scan_for_whitespace_token():
            case Just(_):
                self.advance()
                return Ok(nothing)
            case _:
                pass

        match self.scan_for_comment_token():
            case Just(comment_token):
                return Ok(Just(comment_token))
            case _:
                pass

        match self.scan_for_string_token():
            case Ok(maybe_string_token):
                match maybe_string_token:
                    case Just(string_token):

                        return Ok(Just(string_token))
                    case _:
                        pass
            case err:
                self.advance()
                return err

        double_character_token = self.scan_for_double_character_token()
        match double_character_token:
            case Just(token):
                self.advance(2)
                return Ok(Just(token))
            case _:
                pass

        single_character_token = self.scan_for_single_character_token()
        match single_character_token:
            case Just(token):
                self.advance()
                return Ok(Just(token))
            case _:
                pass

        err = Err(
            WodeError(
                WodeErrorType.UnknownCharacterError, self.source, self.current_position
            )
        )
        self.advance()
        return err

    def scan(self) -> Result[List[Token], List[WodeError]]:
        errors: List[WodeError] = []
        while True:
            match self.scan_once():
                case Ok(maybe_token):
                    match maybe_token:
                        case Just(token):
                            self.tokens.append(token)
                            if token.token_type == TokenType.EOF:
                                if len(errors) > 0:
                                    return Err(errors)
                                else:
                                    return Ok(self.tokens)
                        case _:
                            pass
                case Err(err):
                    errors.append(err)
