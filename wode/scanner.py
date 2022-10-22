from dataclasses import dataclass
from typing import Any, Callable, List, Set, Tuple

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
Scanner = Callable[[Source], ScannerOutput]


def chomp(source: Source, n: int = 1) -> ScannerOutput:
    """Return the first n characters and the remaining source."""
    if len(source.text) < n:
        return nothing
    first_n_characters = source.text[:n]
    remaining_source = Source(source.text[n:], source.position + n)
    return Just((first_n_characters, remaining_source))


def get_literal_scanner(value: str) -> Scanner:
    def literal_scanner(source: Source) -> ScannerOutput:
        match chomp(source, len(value)):
            case Just((first_n_characters, remaining_source)):
                if first_n_characters == value:
                    return Just((first_n_characters, remaining_source))
                else:
                    return nothing
            case _:
                return nothing

    return literal_scanner


def get_while_scanner(continue_callback: Callable[[str], Maybe[bool]]) -> Scanner:
    def while_scanner(source: Source) -> ScannerOutput:
        token_length = 1
        while True:
            match chomp(source, token_length):
                case Just((bite, _)):
                    last_character = bite[-1]
                    match continue_callback(last_character):
                        case Just(callback_output):
                            if callback_output:
                                token_length += 1
                            else:
                                return chomp(source, token_length - 1)
                        case _:
                            return nothing
                case _:
                    return nothing

    return while_scanner


def get_while_is_any_literal_scanner(continue_values: List[str]) -> Scanner:
    return get_while_scanner(lambda c: Just(c in continue_values))


def get_while_is_not_any_literal_scanner(terminate_values: Set[str]) -> Scanner:
    return get_while_scanner(lambda c: Just(c not in terminate_values))


def get_delimited_scanner(
    scan_left_delimiter: Scanner, scan_middle: Scanner, scan_right_delimiter: Scanner
) -> Scanner:
    def delimited_scanner(source: Source) -> ScannerOutput:
        match scan_left_delimiter(source):
            case Just((_, remaining_source)):
                source = remaining_source
            case _:
                return nothing

        match scan_middle(source):
            case Just((middle_bite_, remaining_source)):
                middle_bite = middle_bite_
                source = remaining_source
            case _:
                return nothing

        match scan_right_delimiter(source):
            case Just((_, remaining_source)):
                source = remaining_source
            case _:
                return nothing

        return Just((middle_bite, source))

    return delimited_scanner


def get_sequence_scanner(scanners: List[Scanner]) -> Scanner:
    def sequence_scanner(source: Source) -> ScannerOutput:
        output = ""
        for scanner in scanners:
            match scanner(source):
                case Just((bite, remaining_source)):
                    output += bite
                    source = remaining_source
                case _:
                    return nothing

        return Just((output, source))

    return sequence_scanner


def get_any_scanner(scanners: List[Scanner]) -> Scanner:
    def any_scanner(source: Source) -> ScannerOutput:
        for scanner in scanners:
            match scanner(source):
                case Just((bite, remaining_source)):
                    return Just((bite, remaining_source))
                case _:
                    pass
        return nothing

    return any_scanner


def get_any_literal_scanner(literal_values: List[str]) -> Scanner:
    return get_any_scanner([get_literal_scanner(literal) for literal in literal_values])


def get_repeat_scanner(scanner: Scanner) -> Scanner:
    def repeat_scanner(source: Source) -> ScannerOutput:
        output = ""
        while True:
            match scanner(source):
                case Just((bite, remaining_source)):
                    output += bite
                    source = remaining_source
                case _:
                    if len(output) == 0:
                        return nothing
                    return Just((output, source))

    return repeat_scanner
