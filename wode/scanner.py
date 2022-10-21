from dataclasses import dataclass
from typing import Callable, List, Tuple

from koda import Err, Just, Maybe, Ok, Result, mapping_get, nothing

from wode.constants import DIGITS, LETTERS


def is_letter(c: str) -> bool:
    return c in LETTERS


def is_digit(c: str) -> bool:
    return c in DIGITS


@dataclass
class Source:
    text: str
    position: int = 0


ScannerOutput = Maybe[Tuple[str, Source]]


def chomp(source: Source, n: int = 1) -> ScannerOutput:
    """Return the first n characters and the remaining source."""
    if len(source.text) < n:
        return nothing
    first_n_characters = source.text[:n]
    remaining_source = Source(source.text[n:], source.position + n)
    return Just((first_n_characters, remaining_source))


# def peek(source: str, n: int = 1) -> ScannerOutput:
#     """Return the first n characters and the source."""
#     if len(source) < n:
#         return nothing
#     return Just((source[:n], source))


def scan_literal(source: Source, value: str) -> ScannerOutput:
    match chomp(source, len(value)):
        case Just((first_n_characters, remaining_source)):
            if first_n_characters == value:
                return Just((first_n_characters, remaining_source))
            else:
                return nothing
        case _:
            return nothing


def scan_literals(source: Source, values: List[str]) -> ScannerOutput:
    # Scan the longest tokens first
    values = sorted(values, key=len, reverse=True)
    for value in values:
        match scan_literal(source, value):
            case Just(x):
                return Just(x)
            case _:
                pass
    return nothing


def scan_while_callback(
    source: Source, continue_callback: Callable[[str], Maybe[bool]]
) -> ScannerOutput:
    token_length = 1
    while True:
        match chomp(source, token_length):
            case Just((first_n_characters, _)):
                match continue_callback(first_n_characters):
                    case Just(callback_output):
                        if callback_output:
                            token_length += 1
                        else:
                            return chomp(source, token_length - 1)
                    case _:
                        return nothing
            case _:
                return nothing


def scan_delimited(
    source: Source, left_delimiter: str, right_delimiter: str
) -> ScannerOutput:
    middle_bite_size = 0
    while True:
        the_source = source

        # Try matching the left delimiter
        match scan_literal(the_source, left_delimiter):
            case Just((_, remaining_source)):
                the_source = remaining_source
            case _:
                return nothing

        # Try matching the middle section
        match chomp(the_source, middle_bite_size):
            case Just((middle_bite, remaining_source)):
                middle_bite = middle_bite
                the_source = remaining_source
            case _:
                middle_bite_size += 1
                continue

        # Try matching the right delimiter
        match scan_literal(the_source, right_delimiter):
            case Just((_, remaining_source_again_again)):
                return Just((middle_bite, remaining_source_again_again))
            case _:
                middle_bite_size += 1
                continue


def scan_string(source: Source) -> ScannerOutput:
    return scan_delimited(source, '"', '"')


def scan_comment(source: Source) -> ScannerOutput:
    return scan_delimited(source, "#", "\n")


# def scan_multiple(source,scanner)


# class Scanner:
#     def __init__(self, source: str) -> None:
#         self.source = source
#         self.current_position: int = 0
#         self.tokens: List[Token] = []

#     def get_remaining_source(self) -> str:
#         return self.source[self.current_position :]

#     def is_at_end(self) -> bool:
#         return self.current_position == len(self.source)

#     def advance(self, by: int = 1) -> None:
#         self.current_position += by

#     def look_one(self) -> str:
#         return self.source[self.current_position]

#     def look_ahead(self) -> Maybe[str]:
#         try:
#             return Just(self.source[self.current_position + 1])
#         except IndexError:
#             return nothing

#     def scan_for_end_of_file_token(self) -> Maybe[Token]:
#         if not self.is_at_end():
#             return nothing

#         return Just(Token(TokenType.EOF, "", self.current_position))

#     def scan_for_whitespace_token(self) -> Maybe[str]:
#         first_character = self.get_remaining_source()[:1]
#         if first_character not in [" ", "\t", "\n"]:
#             return nothing

#         return Just(first_character)

#     def scan_for_comment_token(self) -> Maybe[Token]:
#         if self.look_one() != "#":
#             return nothing

#         comment = ""
#         while not self.is_at_end() and self.look_one() != "\n":
#             comment += self.look_one()
#             self.advance()
#         return Just(Token(TokenType.COMMENT, comment, self.current_position))

#     def scan_for_string_token(self) -> Result[Maybe[Token], WodeError]:
#         if self.look_one() != '"':
#             return Ok(nothing)

#         n_quotation_marks_seen = 0
#         string = ""
#         while n_quotation_marks_seen < 2:
#             if self.is_at_end():
#                 return Err(
#                     WodeError(
#                         WodeErrorType.UnexpectedEndOfFileError,
#                         self.source,
#                         self.current_position - 1,
#                     )
#                 )
#             if self.look_one() == '"':
#                 n_quotation_marks_seen += 1
#             else:
#                 string += self.look_one()
#             self.advance()
#         return Ok(Just(Token(TokenType.STRING, string, self.current_position)))

#     def scan_for_double_character_token(self) -> Maybe[Token]:
#         lexeme = self.get_remaining_source()[:2]
#         maybe_token_type = mapping_get(double_character_token_mapping, lexeme)
#         maybe_token = maybe_token_type.map(
#             lambda token_type: Token(token_type, lexeme, self.current_position)
#         )
#         return maybe_token

#     def scan_for_single_character_token(self) -> Maybe[Token]:
#         lexeme = self.get_remaining_source()[:1]
#         maybe_token_type = mapping_get(single_character_token_mapping, lexeme)
#         maybe_token = maybe_token_type.map(
#             lambda token_type: Token(token_type, lexeme, self.current_position)
#         )
#         return maybe_token

#     def scan_for_number_token(self) -> Result[Maybe[Token], WodeError]:
#         def is_digit(c: str) -> bool:
#             return c in DIGITS

#         c = self.look_one()
#         if not is_digit(c):
#             if c == ".":
#                 self.advance()
#                 return Err(
#                     WodeError(
#                         WodeErrorType.NoLeadingZeroOnFloatError,
#                         self.source,
#                         self.current_position,
#                     )
#                 )
#             else:
#                 return Ok(nothing)

#         number = ""
#         while True:
#             c = self.look_one()
#             if is_digit(c):
#                 number += c
#                 self.advance()
#             else:
#                 if c == ".":
#                     maybe_next_c = self.look_ahead()
#                     match maybe_next_c:
#                         case Just(next_c):
#                             if is_digit(next_c):
#                                 number += c
#                                 self.advance()
#                                 while True:
#                                     c = self.look_one()
#                                     if is_digit(c):
#                                         number += c
#                                         self.advance()
#                                     else:
#                                         return Ok(
#                                             Just(
#                                                 Token(
#                                                     TokenType.FLOAT,
#                                                     number,
#                                                     self.current_position,
#                                                 )
#                                             )
#                                         )
#                             else:
#                                 self.advance()
#                                 return Err(
#                                     WodeError(
#                                         WodeErrorType.UnterminatedFloatError,
#                                         self.source,
#                                         self.current_position,
#                                     )
#                                 )
#                         case _:
#                             return Err(
#                                 WodeError(
#                                     WodeErrorType.UnexpectedEndOfFileError,
#                                     self.source,
#                                     self.current_position,
#                                 )
#                             )
#                 else:
#                     return Ok(
#                         Just(Token(TokenType.INTEGER, number, self.current_position))
#                     )

#     def scan_for_identifier_token(self) -> Maybe[Token]:
#         valid_identifier_prefixes = ["_"] + LETTERS
#         valid_identifier_characters = ["_"] + LETTERS + DIGITS
#         c = self.look_one()
#         if c not in valid_identifier_prefixes:
#             return nothing

#         identifier = ""

#         while True:
#             c = self.look_one()
#             if c in valid_identifier_characters:
#                 identifier += c
#                 self.advance()
#             else:
#                 break

#         if identifier in reserved_keywords.keys():
#             return Just(
#                 Token(
#                     TokenType(reserved_keywords[identifier]),
#                     identifier,
#                     self.current_position,
#                 )
#             )
#         else:
#             return Just(Token(TokenType.IDENTIFIER, identifier, self.current_position))

#     def scan_once(self) -> Result[Maybe[Token], WodeError]:
#         match self.scan_for_end_of_file_token():
#             case Just(end_of_file_token):
#                 return Ok(Just(end_of_file_token))
#             case _:
#                 pass

#         match self.scan_for_whitespace_token():
#             case Just(_):
#                 self.advance()
#                 return Ok(nothing)
#             case _:
#                 pass

#         match self.scan_for_comment_token():
#             case Just(_):
#                 # TODO: Add parsing for comments
#                 # return Ok(Just(comment_token))
#                 return Ok(nothing)
#             case _:
#                 pass

#         match self.scan_for_string_token():
#             case Ok(maybe_string_token):
#                 match maybe_string_token:
#                     case Just(string_token):
#                         return Ok(Just(string_token))
#                     case _:
#                         pass
#             case err:
#                 return err

#         match self.scan_for_number_token():
#             case Ok(maybe_number_token):
#                 match maybe_number_token:
#                     case Just(number_token):
#                         return Ok(Just(number_token))
#                     case _:
#                         pass
#             case err:
#                 return err

#         maybe_double_character_token = self.scan_for_double_character_token()
#         match maybe_double_character_token:
#             case Just(double_character_token):
#                 self.advance(2)
#                 return Ok(Just(double_character_token))
#             case _:
#                 pass

#         maybe_single_character_token = self.scan_for_single_character_token()
#         match maybe_single_character_token:
#             case Just(single_character_token):
#                 self.advance()
#                 return Ok(Just(single_character_token))
#             case _:
#                 pass

#         maybe_identifier_token = self.scan_for_identifier_token()
#         match maybe_identifier_token:
#             case Just(identifier_token):
#                 return Ok(Just(identifier_token))
#             case _:
#                 pass

#         err = Err(
#             WodeError(
#                 WodeErrorType.UnknownCharacterError, self.source, self.current_position
#             )
#         )
#         self.advance()
#         return err

#     def scan(self) -> Tuple[List[Token], List[WodeError]]:
#         errors: List[WodeError] = []
#         while True:
#             match self.scan_once():
#                 case Ok(maybe_token):
#                     match maybe_token:
#                         case Just(token):
#                             self.tokens.append(token)
#                             if token.token_type == TokenType.EOF:
#                                 return self.tokens, errors
#                         case _:
#                             pass
#                 case Err(error):
#                     errors.append(error)
