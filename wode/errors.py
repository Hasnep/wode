from wode.lines import get_line, get_line_number_of_position, get_position_in_line
from wode.types import Int, Str


class WodeError:
    def __init__(
        self, error_type: Str, message: Str, source: Str, position: Int
    ) -> None:
        self.error_type = error_type
        self.message = message
        self.source = source
        self.position = position
        self.line_number = get_line_number_of_position(source, position)
        self.line = get_line(source, self.line_number).rstrip("\n")
        self.position_in_line = get_position_in_line(source, position)

    def get_message(self) -> Str:
        arrow_string = self.position_in_line * " " + "^"
        return "\n".join(
            [
                self.message,
                f"Occurred on line {self.line_number}:",
                self.line,
                arrow_string,
            ]
        )


class UnexpectedEndOfFileError(WodeError):
    def __init__(self, source: Str, position: Int) -> None:
        error_type = "UnexpectedEndOfFileError"
        message = "The file ended unexpectedly."
        super().__init__(error_type, message, source, position)


class UnknownCharacterError(WodeError):
    def __init__(self, source: Str, position: Int, *, unknown_character: Str) -> None:
        error_type = "UnknownCharacterError"
        message = f"The character `{unknown_character}` is not known by the transpiler."
        super().__init__(error_type, message, source, position)


class UnterminatedFloatError(WodeError):
    def __init__(self, source: Str, position: Int, *, unterminated_float: Str) -> None:
        error_type = "UnterminatedFloatError"
        message = f"The float `{unterminated_float}0` needs some numbers after its decimal point."
        super().__init__(error_type, message, source, position)


class NoLeadingZeroOnFloatError(WodeError):
    def __init__(
        self, source: Str, position: Int, *, float_without_leading_zero: Str
    ) -> None:
        error_type = "NoLeadingZeroOnFloatError"
        message = f"The float `0{float_without_leading_zero}` needs a leading zero."
        super().__init__(error_type, message, source, position)


class UnexpectedEndOfExpressionError(WodeError):
    def __init__(self, source: Str, position: Int) -> None:
        error_type = "UnexpectedEndOfExpressionError"
        message = "This expression ended unexpectedly."
        super().__init__(error_type, message, source, position)


class UnexpectedTokenTypeError(WodeError):
    def __init__(self, source: Str, position: Int) -> None:
        error_type = "UnexpectedTokenType"
        message = "This token type wasn't expected here."
        super().__init__(error_type, message, source, position)


class ExpectedSemicolonError(WodeError):
    def __init__(self, source: Str, position: Int) -> None:
        error_type = "ExpectedSemicolonError"
        message = "A semicolon was expected, try adding a semicolon here."
        super().__init__(error_type, message, source, position)


class TooManyDecimalPointsError(WodeError):
    def __init__(
        self, source: Str, position: Int, *, float_with_too_many_decimal_points: Str
    ) -> None:
        error_type = "TooManyDecimalPointsError"
        message = f"The float `{float_with_too_many_decimal_points}` has too many decimal points."
        super().__init__(error_type, message, source, position)
