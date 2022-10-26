from dataclasses import dataclass
from typing import Callable, List, Literal, Tuple

from koda import Err, Just, Maybe, Ok, Result, nothing

from wode.constants import DIGITS, LETTERS
from wode.errors import WodeError, WodeErrorType
from wode.utils import unwrap

BiteAndNewState = Tuple[str, "ScannerState"]
ScannerOutput = Result[Maybe[BiteAndNewState], WodeError]
Scanner = Callable[["ScannerState"], ScannerOutput]


def is_letter(c: str) -> bool:
    return c in LETTERS


def is_digit(c: str) -> bool:
    return c in DIGITS


@dataclass
class ScannerState:
    _source: str
    position: int = 0

    @property
    def remaining_source(self) -> str:
        return self._source[self.position :]

    @property
    def raw_source(self) -> str:
        return self._source

    def chomp(self, n: int = 1) -> Result[BiteAndNewState, WodeError]:
        """Return the first n characters and the remaining source."""
        if len(self.remaining_source) < n:
            return Err(
                WodeError(
                    WodeErrorType.UnexpectedEndOfFileError,
                    self.raw_source,
                    self.position,
                )
            )
        first_n_characters = self.remaining_source[:n]
        new_state = ScannerState(self.raw_source, self.position + n)
        return Ok((first_n_characters, new_state))


def get_literal_scanner(value: str, ignore_unexpected_eof: bool = False) -> Scanner:
    """Get a scanner that matches exactly the target string."""

    def literal_scanner(state: ScannerState) -> ScannerOutput:
        match state.chomp(len(value)):
            case Ok((first_n_characters, remaining_source)):
                if first_n_characters == value:
                    # Found match
                    return Ok(Just((first_n_characters, remaining_source)))
                else:
                    # Did not match
                    return Ok(nothing)
            case Err(err):
                # Got an unexpected end of file
                if ignore_unexpected_eof:
                    return Ok(nothing)
                else:
                    return Err(err)

    return literal_scanner


def get_while_or_zero_characters_scanner(
    continue_callback: Callable[[str], bool],
    callback_checks: Literal["only_last_character", "entire_bite"],
) -> Scanner:
    """Get a scanner that matches characters while the callback returns true for that character, including returning zero characters."""

    def while_or_zero_characters_scanner(state: ScannerState) -> ScannerOutput:
        bite_size = 1
        while True:
            match state.chomp(bite_size):
                case Ok((bite, _)):
                    if callback_checks == "only_last_character":
                        callback_input = bite[-1]
                    else:
                        callback_input = bite
                    if continue_callback(callback_input):
                        # Continue scanning
                        bite_size += 1
                    else:
                        return Ok(Just(unwrap(state.chomp(bite_size - 1))))
                case Err(err):
                    # Unexpected end of file
                    return Err(err)

    return while_or_zero_characters_scanner


def get_while_one_or_more_scanner(
    continue_callback: Callable[[str], bool],
    callback_checks: Literal["only_last_character", "entire_bite"],
) -> Scanner:
    """Get a scanner that matches characters while the callback returns true for that character, failing if no characters are matched."""

    def while_one_or_more_scanner(state: ScannerState) -> ScannerOutput:
        while_or_zero_characters_scanner = get_while_or_zero_characters_scanner(
            continue_callback, callback_checks
        )
        match while_or_zero_characters_scanner(state):
            case Ok(Just((bite, new_state))):
                if len(bite) == 0:
                    return Ok(nothing)
                else:
                    return Ok(Just((bite, new_state)))
            case Ok(_):
                return Ok(nothing)
            case Err(err):
                return Err(err)

    return while_one_or_more_scanner


def get_zero_or_more_of_any_literal_scanner(
    continue_values: List[str],
) -> Scanner:
    return get_while_or_zero_characters_scanner(
        lambda bite: bite in continue_values, callback_checks="entire_bite"
    )


def get_one_or_more_of_any_literal_scanner(continue_values: List[str]) -> Scanner:
    return get_while_one_or_more_scanner(
        lambda bite: bite in continue_values, callback_checks="entire_bite"
    )


def get_delimited_scanner(
    scan_left_delimiter: Scanner, scan_middle: Scanner, scan_right_delimiter: Scanner
) -> Scanner:
    def delimited_scanner(state: ScannerState) -> ScannerOutput:
        match scan_left_delimiter(state):
            case Ok(Just((_, new_state))):
                state = new_state
            case Ok(_):
                return Ok(nothing)
            case Err(err):
                return Err(err)

        match scan_middle(state):
            case Ok(Just((middle_bite_, new_state))):
                middle_bite = middle_bite_
                state = new_state
            case Ok(_):
                return Ok(nothing)
            case Err(err):
                return Err(err)

        match scan_right_delimiter(state):
            case Ok(Just((_, new_state))):
                state = new_state
            case Ok(_):
                return Ok(nothing)
            case Err(err):
                return Err(err)

        return Ok(Just((middle_bite, state)))

    return delimited_scanner


def get_sequence_scanner(scanners: List[Scanner]) -> Scanner:
    def sequence_scanner(state: ScannerState) -> ScannerOutput:
        output = ""
        for scanner in scanners:
            match scanner(state):
                case Ok(Just((bite, new_state))):
                    output += bite
                    state = new_state
                case Ok(_):
                    return Ok(nothing)
                case Err(err):
                    return Err(err)

        return Ok(Just((output, state)))

    return sequence_scanner


def get_any_scanner(scanners: List[Scanner]) -> Scanner:
    def any_scanner(state: ScannerState) -> ScannerOutput:
        for scanner in scanners:
            match scanner(state):
                case Ok(Just((bite, new_state))):
                    return Ok(Just((bite, new_state)))
                case Ok(_):
                    pass
                case Err(err):
                    return Err(err)
        return Ok(nothing)

    return any_scanner


def get_any_literal_scanner(literal_values: List[str]) -> Scanner:
    return get_any_scanner([get_literal_scanner(literal) for literal in literal_values])


def get_repeat_scanner(scanner: Scanner) -> Scanner:
    def repeat_scanner(state: ScannerState) -> ScannerOutput:
        output = ""
        while True:
            match scanner(state):
                case Ok(Just((bite, new_state))):
                    output += bite
                    state = new_state
                case Ok(_):
                    if len(output) == 0:
                        return nothing
                    else:
                        return Just((output, state))
                case Err(err):
                    return Err(err)

    return repeat_scanner


def get_eof_scanner() -> Scanner:
    def eof_scanner(state: ScannerState) -> ScannerOutput:
        if len(state.remaining_source) == 0:
            return nothing
        else:
            return Just(("", state))

    return eof_scanner
