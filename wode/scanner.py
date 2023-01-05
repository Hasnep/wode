from koda import Err, Just, Maybe, Ok, Result, mapping_get, nothing

from wode.constants import VALID_IDENTIFIER_CHARACTERS, VALID_IDENTIFIER_PREFIXES
from wode.errors import (
    NoLeadingZeroOnFloatError,
    TooManyDecimalPointsError,
    UnexpectedEndOfFileError,
    UnknownCharacterError,
    UnterminatedFloatError,
    WodeError,
)
from wode.token import EOFToken, Token
from wode.token_type import TokenType
from wode.types import Int, List, Str, Tuple
from wode.utils import UnreachableError, is_digit, is_whitespace, safe_substring

token_mapping = {
    # Triple character tokens
    "...": TokenType.ELLIPSIS,
    # Double character tokens
    "->": TokenType.SINGLE_ARROW,
    "!=": TokenType.BANG_EQUAL,
    "<=": TokenType.LESS_EQUAL,
    "==": TokenType.EQUAL_EQUAL,
    "=>": TokenType.DOUBLE_ARROW,
    ">=": TokenType.GREATER_EQUAL,
    "|>": TokenType.PIPE,
    "&&": TokenType.AMPERSAND_AMPERSAND,
    "||": TokenType.BAR_BAR,
    # Single character tokens
    ",": TokenType.COMMA,
    ";": TokenType.SEMICOLON,
    ":": TokenType.COLON,
    "(": TokenType.LEFT_BRACKET,
    ")": TokenType.RIGHT_BRACKET,
    "[": TokenType.LEFT_SQUARE_BRACKET,
    "]": TokenType.RIGHT_SQUARE_BRACKET,
    "{": TokenType.LEFT_CURLY_BRACKET,
    "}": TokenType.RIGHT_CURLY_BRACKET,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    "^": TokenType.CARET,
    "+": TokenType.PLUS,
    # Possibly double character tokens
    "-": TokenType.MINUS,
    "!": TokenType.BANG,
    "<": TokenType.LESS,
    "=": TokenType.EQUAL,
    ">": TokenType.GREATER,
    # Possibly triple character tokens
    ".": TokenType.DOT,
}
reserved_keywords = {
    "elif": TokenType.ELIF,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "if": TokenType.IF,
    "in": TokenType.IN,
    "let": TokenType.LET,
    "match": TokenType.MATCH,
    "nothing": TokenType.NOTHING,
    "return": TokenType.RETURN,
    "struct": TokenType.STRUCT,
    "true": TokenType.TRUE,
    "while": TokenType.WHILE,
    "yield": TokenType.YIELD,
}


class ScannerState:
    def __init__(self, source: Str, position: Int = 0) -> None:
        self.source = source
        self.position: Int = position

    def chomp(self, n: Int = 1) -> Maybe[Tuple[Str, "ScannerState"]]:
        try:
            first_n_characters = safe_substring(
                self.source, start=self.position, length=n
            )
        except IndexError:
            return nothing
        new_position = self.position + n
        return Just((first_n_characters, ScannerState(self.source, new_position)))


def scan_for_eof_token(state: ScannerState) -> Maybe[Tuple[Token, ScannerState]]:
    match state.chomp():
        case Just(_):
            return nothing
        case _:
            return Just((EOFToken(state.source), state))


def scan_for_whitespace_token(state: ScannerState) -> Maybe[ScannerState]:
    match state.chomp():
        case Just((bite, new_state)):
            pass
        case _:  # pragma: no cover
            raise UnreachableError(
                "Scanning for whitespace happens after scanning for an EOF token."
            )

    if is_whitespace(bite):
        return Just(new_state)
    else:
        return nothing


def scan_for_comment_token(state: ScannerState) -> Maybe[ScannerState]:
    # TODO: Make this function return a comment token

    # Get the first character
    match state.chomp():
        case Just((bite, _)):
            pass
        case _:  # pragma: no cover
            raise UnreachableError(
                "Scanning for a comment token happens after scanning for an EOF token."
            )

    # If the first character is not a hash then we didn't find a comment
    if bite != "#":
        return nothing

    # If we found a comment, keep consuming characters until the end of the line
    while True:
        match state.chomp():
            case Just((bite, state)):
                # The comment finishes at the end of the line
                if bite == "\n":
                    return Just(state)
            # The comment also finishes when we reach the end of the file
            case _:
                return Just(state)


def scan_for_string_token(
    state: ScannerState,
) -> Maybe[Tuple[Result[Token, WodeError], ScannerState]]:
    # Get the first character
    match state.chomp():
        case Just((bite, state)):
            pass
        case _:  # pragma: no cover
            raise UnreachableError(
                "Scanning for a string token happens after scanning for an EOF token."
            )

    # If the first character isn't a quotation mark it's not a string
    if bite != '"':
        return nothing

    start_of_string_position = state.position
    while True:
        match state.chomp():
            case Just((bite, state)):
                pass
            case _:
                unexpected_end_of_file_error = UnexpectedEndOfFileError(
                    state.source, state.position - 1
                )
                return Just((Err(unexpected_end_of_file_error), state))

        # Check if we found the closing quotation mark
        if bite == '"':
            end_of_string_position = state.position - 1
            token_length = end_of_string_position - start_of_string_position
            string_token = Token(
                TokenType.STRING,
                start_of_string_position,
                token_length,
                state.source,
            )
            return Just((Ok(string_token), state))


def scan_for_n_character_token(
    state: ScannerState, n_characters: Int
) -> Maybe[Tuple[Token, ScannerState]]:
    # Check if we've reached the end of the file
    match state.chomp():
        case Just((_, _)):
            pass
        case _:  # pragma: no cover
            raise UnreachableError(
                f"Scanning for a {n_characters} character token happens after scanning for an EOF token."
            )

    # Get the next n characters
    match state.chomp(n_characters):
        case Just((bite, new_state)):
            pass
        case _:
            # If we reach the end of the file now it means the token is less than n characters
            return nothing

    maybe_token_type = mapping_get(token_mapping, bite)
    maybe_token = maybe_token_type.map(
        lambda token_type: Token(token_type, state.position, n_characters, state.source)
    )
    return maybe_token.map(lambda token: (token, new_state))


def scan_for_number_token(
    state: ScannerState,
) -> Maybe[Tuple[Result[Token, WodeError], ScannerState]]:
    start_of_number_position = state.position

    # Get the first character
    match state.chomp():
        case Just((bite, new_state)):
            pass
        case _:  # pragma: no cover
            raise UnreachableError(
                "Scanning for a number token happens after scanning for an EOF token."
            )

    # If the first character is a decimal point, the number has no leading zero
    if bite == ".":
        state = new_state
        while True:
            match state.chomp():
                case Just((bite, new_state)):
                    if is_digit(bite):
                        pass
                    else:
                        break
                case _:
                    break
            state = new_state
        float_without_leading_zero = safe_substring(
            state.source, start=start_of_number_position, end=state.position
        )
        no_leading_zero_on_float_error = NoLeadingZeroOnFloatError(
            state.source,
            state.position,
            float_without_leading_zero=float_without_leading_zero,
        )
        return Just((Err(no_leading_zero_on_float_error), new_state))
    elif is_digit(bite):
        pass
    else:
        return nothing

    found_a_decimal_point = False
    while True:
        match state.chomp():
            case Just((".", new_state)):
                # When we find a decimal point, start parsing the fractional part
                found_a_decimal_point = True
                state = new_state
                break
            case Just((bite, new_state)):
                if is_digit(bite):
                    pass
                else:
                    # If the character isn't a number or a decimal then the number has ended
                    break
            case _:
                # If we reach the end of the file then the number has ended
                break
        state = new_state

    # Check if we need to parse the fractional part
    if found_a_decimal_point:
        found_a_fractional_part = False
        while True:
            match state.chomp():
                case Just((".", new_state)):
                    # If we find another decimal point, return an error
                    while True:
                        match state.chomp():
                            case Just((bite, new_state)):
                                if is_digit(bite) or bite == ".":
                                    state = new_state
                                else:
                                    break
                            case _:
                                break
                    float_with_too_many_decimal_points = safe_substring(
                        state.source, start=start_of_number_position, end=state.position
                    )
                    too_many_decimal_points_error = TooManyDecimalPointsError(
                        state.source,
                        state.position,
                        float_with_too_many_decimal_points=float_with_too_many_decimal_points,
                    )
                    return Just((Err(too_many_decimal_points_error), state))
                case Just((bite, new_state)):
                    if is_digit(bite):
                        found_a_fractional_part = True
                    else:
                        # If the character isn't a number or a decimal then the number has ended
                        break
                case _:
                    # If we reach the end of the file then the number has ended
                    break
            state = new_state
        if not found_a_fractional_part:
            unterminated_float = safe_substring(
                state.source,
                start=start_of_number_position,
                end=state.position,
            )
            unterminated_float_error = UnterminatedFloatError(
                state.source,
                state.position,
                unterminated_float=unterminated_float,
            )
            return Just((Err(unterminated_float_error), state))

    # Return the number token
    token_length = state.position - start_of_number_position
    if found_a_decimal_point:
        token_type = TokenType.FLOAT
    else:
        token_type = TokenType.INTEGER

    token = Token(token_type, start_of_number_position, token_length, state.source)
    return Just((Ok(token), state))


def scan_for_identifier_token(state: ScannerState) -> Maybe[Tuple[Token, ScannerState]]:
    # Get the first character
    match state.chomp():
        case Just((bite, _)):
            pass
        case _:  # pragma: no cover
            raise UnreachableError(
                "Scanning for an identifier token happens after scanning for an EOF token."
            )

    # Make sure the identifier starts with a valid character
    if bite not in VALID_IDENTIFIER_PREFIXES:
        return nothing

    start_of_identifier_position = state.position
    while True:
        match state.chomp():
            case Just((bite, new_state)):
                if bite in VALID_IDENTIFIER_CHARACTERS:
                    pass
                else:
                    break
            case _:
                # If we reached the end of the file the identifier has ended
                break
        state = new_state

    # Return the identifier token
    end_of_identifier_position = state.position
    identifier = safe_substring(
        state.source,
        start=start_of_identifier_position,
        end=end_of_identifier_position,
    )
    token = Token(
        reserved_keywords.get(identifier, TokenType.IDENTIFIER),
        start_of_identifier_position,
        len(identifier),
        state.source,
    )
    return Just((token, state))


def scan_one_token(
    state: ScannerState,
) -> Tuple[Result[Maybe[Token], WodeError], ScannerState]:
    match scan_for_eof_token(state):
        case Just((token, state)):
            return Ok(Just(token)), state
        case _:
            pass

    match scan_for_whitespace_token(state):
        case Just(new_state):
            return Ok(nothing), new_state
        case _:
            pass

    match scan_for_comment_token(state):
        case Just(new_state):
            return Ok(nothing), new_state
        case _:
            pass

    match scan_for_string_token(state):
        case Just((Ok(token), state)):
            return Ok(Just(token)), state
        case Just((Err(wode_error), state)):
            return Err(wode_error), state
        case _:
            pass

    match scan_for_n_character_token(state, 3):
        case Just((token, state)):
            return Ok(Just(token)), state
        case _:
            pass

    match scan_for_n_character_token(state, 2):
        case Just((token, state)):
            return Ok(Just(token)), state
        case _:
            pass

    match scan_for_number_token(state):
        case Just((Ok(token), state)):
            return Ok(Just(token)), state
        case Just((Err(wode_error), state)):
            return Err(wode_error), state
        case _:
            pass

    # Must go after number token so we don't accidentally parse the dot in .123
    match scan_for_n_character_token(state, 1):
        case Just((token, state)):
            return Ok(Just(token)), state
        case _:
            pass

    match scan_for_identifier_token(state):
        case Just((token, state)):
            return Ok(Just(token)), state
        case _:
            pass

    match state.chomp():
        case Just((bite, new_state)):
            unknown_character_error = UnknownCharacterError(
                state.source, state.position, unknown_character=bite
            )
            return (Err(unknown_character_error), new_state)
        case _:  # pragma: no cover
            raise UnreachableError(
                "Reaching an unknown character error happens after scanning for an EOF token."
            )


def scan_all_tokens(source: Str) -> Tuple[List[Token], List[WodeError]]:
    tokens: List[Token] = []
    errors: List[WodeError] = []
    state = ScannerState(source)
    while True:
        match scan_one_token(state):
            case (Ok(Just(token)), new_state):
                tokens.append(token)
                state = new_state
                if token.token_type == TokenType.EOF:
                    return tokens, errors
            case (Err(wode_error), new_state):
                errors.append(wode_error)
                state = new_state
                # if wode_error.error_type==WodeErrorType.UnexpectedEndOfFileError:
                #     return tokens,errors
            case (_, new_state):
                state = new_state
