from .lines import get_line, get_line_number_of_position, get_position_in_line
from enum import Enum


class WodeErrorType(Enum):
    UnexpectedEndOfFileError = "unexpected_end_of_file_error"
    UnknownCharacterError = "unknown_character_error"


class WodeError:
    def __init__(self, error_type: WodeErrorType, source: str, position: int) -> None:
        line_number = get_line_number_of_position(source, position)
        line = get_line(source, line_number)
        position_in_line = get_position_in_line(source, position)
        arrow_string = position_in_line * " " + "^"
        self.message = "\n".join(
            [f"{error_type} on line {line_number}:", line, arrow_string]
        )
        print(self.message)
