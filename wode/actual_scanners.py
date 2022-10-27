from koda import Err, Just, Ok, nothing

from wode.constants import (
    DIGITS,
    HORIZONTAL_WHITESPACE_CHARACTERS,
    LETTERS,
    WHITESPACE_CHARACTERS,
)
from wode.scanner import (
    ScannerOutput,
    ScannerState,
    get_any_literal_scanner,
    get_literal_scanner,
    get_one_or_more_of_any_literal_scanner,
    get_sequence_scanner,
    get_while_or_zero_characters_scanner,
    get_zero_or_more_of_any_literal_scanner,
)


def scan_string(state: ScannerState) -> ScannerOutput:
    quotation_mark_scanner = get_literal_scanner('"')
    match quotation_mark_scanner(state):
        case Ok(Just((_, new_state))):
            state = new_state
        case Ok(_):
            return Ok(nothing)
        case Err(err):
            return Err(err)

    scan_until_a_quotation_mark_scanner = get_while_or_zero_characters_scanner(
        lambda c: c != '"', callback_checks="only_last_character"
    )
    match scan_until_a_quotation_mark_scanner(state):
        case Ok(Just((string_contents, new_state))):
            state = new_state
            output = string_contents
        case Ok(_):
            raise ValueError("Scanner unexpectedly returned `nothing`.")
        case Err(err):
            return Err(err)

    match quotation_mark_scanner(state):
        case Ok(Just((_, new_state))):
            state = new_state
        case Ok(_):
            raise ValueError("Scanner unexpectedly returned `nothing`.")
        case Err(err):
            return Err(err)

    return Ok(Just((output, state)))


def scan_comment(state: ScannerState) -> ScannerOutput:
    hash_scanner = get_literal_scanner("#")
    optional_whitespace_scanner = get_zero_or_more_of_any_literal_scanner(
        HORIZONTAL_WHITESPACE_CHARACTERS
    )
    scan_until_a_newline_character_scanner = get_while_or_zero_characters_scanner(
        lambda c: c != "\n", callback_checks="only_last_character"
    )
    newline_scanner = get_literal_scanner("\n")

    match hash_scanner(state):
        case Ok(Just((_, new_state))):
            state = new_state
        case Ok(_):
            return Ok(nothing)
        case Err(err):
            return Err(err)

    match optional_whitespace_scanner(state):
        case Ok(Just((_, new_state))):
            state = new_state
        case Ok(_):
            return Ok(nothing)
        case Err(err):
            return Err(err)

    match scan_until_a_newline_character_scanner(state):
        case Ok(Just((comment_contents, new_state))):
            output = comment_contents
            state = new_state
        case Ok(_):
            raise ValueError("Scanner unexpectedly returned `nothing`.")
        case Err(err):
            return Err(err)

    match newline_scanner(state):
        case Ok(Just((_, new_state))):
            state = new_state
        case Ok(_):
            raise ValueError("Scanner unexpectedly returned `nothing`.")
        case Err(err):
            return Err(err)

    return Ok(Just((output, state)))


def scan_identifier(state: ScannerState) -> ScannerOutput:
    first_character_of_identifier_scanner = get_any_literal_scanner(LETTERS + ["_"])
    subsequent_characters_of_identifier_scanner = get_while_or_zero_characters_scanner(
        lambda c: c in (LETTERS + DIGITS + ["_"]),
        callback_checks="only_last_character",
    )

    token = ""
    match first_character_of_identifier_scanner(state):
        case Ok(Just((c, new_state))):
            token += c
            state = new_state
        case Ok(_):
            return Ok(nothing)
        case Err(err):
            return Err(err)

    match subsequent_characters_of_identifier_scanner(state):
        case Ok(Just((subsequent_characters, new_state))):
            token += subsequent_characters
            state = new_state
        case Ok(_):
            raise ValueError("Scanner unexpectedly returned `nothing`.")
        case Err(err):
            return Err(err)

    return Ok(Just((token, state)))


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
    return get_one_or_more_of_any_literal_scanner(WHITESPACE_CHARACTERS)(source)
