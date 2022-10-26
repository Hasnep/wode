from koda import Err, Just, Ok, Result, nothing

from wode.constants import DIGITS, LETTERS
from wode.errors import WodeError, WodeErrorType
from wode.scanner import (
    ScannerOutput,
    ScannerState,
    get_any_literal_scanner,
    get_delimited_scanner,
    get_literal_scanner,
    get_one_or_more_of_any_literal_scanner,
    get_sequence_scanner,
    get_while_or_zero_characters_scanner,
)


def scan_string(state: ScannerState) -> Result[ScannerOutput, WodeError]:
    quotation_mark_scanner = get_literal_scanner('"')
    match quotation_mark_scanner(state):
        case Just((_, new_state)):
            state = new_state
        case _:
            return Ok(nothing)

    is_not_a_quotation_mark_scanner = get_while_or_zero_characters_scanner(
        lambda c: c != '"'
    )
    match is_not_a_quotation_mark_scanner(state):
        case Just((string_contents, new_state)):
            state = new_state
            output = string_contents
        case _:
            return Err(
                WodeError(
                    WodeErrorType.UnexpectedEndOfFileError,
                    state.raw_source,
                    state.position,
                )
            )

    match quotation_mark_scanner(state):
        case Just((_, new_state)):
            state = new_state
        case _:
            return Err(
                WodeError(
                    WodeErrorType.UnexpectedEndOfFileError,
                    state.raw_source,
                    state.position,
                )
            )

    return Ok(Just((output, state)))


def scan_comment(source: ScannerState) -> ScannerOutput:
    is_not_a_newline_character_scanner = get_while_or_zero_characters_scanner(
        lambda c: c != "\n"
    )
    return get_delimited_scanner(
        get_literal_scanner("#"),
        is_not_a_newline_character_scanner,
        get_literal_scanner("\n"),
    )(source)


def scan_identifier(source: ScannerState) -> ScannerOutput:
    return get_sequence_scanner(
        [
            get_any_literal_scanner(LETTERS + ["_"]),
            get_while_or_zero_characters_scanner(
                lambda c: c in (LETTERS + DIGITS + ["_"])
            ),
        ]
    )(source)


def scan_float(source: ScannerState) -> ScannerOutput:
    return get_sequence_scanner(
        [
            get_one_or_more_of_any_literal_scanner(DIGITS),
            get_literal_scanner("."),
            get_one_or_more_of_any_literal_scanner(DIGITS),
        ]
    )(source)


def scan_integer(source: ScannerState) -> ScannerOutput:
    return get_one_or_more_of_any_literal_scanner(DIGITS)(source)


def scan_whitespace(source: ScannerState) -> ScannerOutput:
    return get_one_or_more_of_any_literal_scanner([" ", "\t", "\n", "\r"])(source)
