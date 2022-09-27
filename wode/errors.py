from enum import Enum

from wode.lines import get_line, get_line_number_of_position, get_position_in_line


class WodeErrorType(Enum):
    UnexpectedEndOfFileError = "unexpected_end_of_file_error"
    UnknownCharacterError = "unknown_character_error"


class WodeError:
    def __init__(self, error_type: WodeErrorType, source: str, position: int) -> None:
        self.error_type = error_type
        self.source = source
        self.position = position
        self.line_number = get_line_number_of_position(source, position)
        self.line = get_line(source, self.line_number)
        self.position_in_line = get_position_in_line(source, position)
        arrow_string = self.position_in_line * " " + "^"
        self.message = "\n".join(
            [f"{error_type} on line {self.line_number}:", self.line, arrow_string]
        )
