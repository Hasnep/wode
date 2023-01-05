from wode.source import SourcePosition, SourceRange
from wode.types import Str


class WodeError:
    def __init__(
        self,
        error_type: Str,
        message: Str,
        location: SourceRange | SourcePosition,
    ) -> None:
        self.error_type = error_type
        self.message = message
        match location:
            case SourcePosition():
                source_range = SourceRange(location.source, location, location)
            case SourceRange():
                source_range = location
        self.source_range = source_range
        self.source = source_range.source

    def _get_position_specifier(self) -> Str:
        file_specifier = (
            ""
            if self.source.file_path is None
            else (Str(self.source.file_path.resolve()) + ":")
        )
        start_specifier = Str(self.source_range.start)
        end_specifier = Str(self.source_range.end)
        return (
            file_specifier
            + start_specifier
            + ("" if len(self.source_range) == 0 else ("to" + end_specifier))
        )

    def get_message(self) -> Str:
        arrow_length = len(self.source_range)
        arrow_string = (self.source_range.start.column.value * " ") + (
            arrow_length * "^"
        )
        position_specifier = self._get_position_specifier()
        return "\n".join(
            [
                f"An error occurred at {position_specifier}",
                self.source.get_line(self.source_range.start.line_number).rstrip("\n"),
                arrow_string,
                self.message,
            ]
        )


class UnexpectedEndOfFileError(WodeError):
    def __init__(self, location: SourcePosition) -> None:
        error_type = "UnexpectedEndOfFileError"
        message = "The file ended unexpectedly."
        super().__init__(error_type, message, location)


class UnknownCharacterError(WodeError):
    def __init__(self, location: SourcePosition) -> None:
        error_type = "UnknownCharacterError"
        unknown_character = location.lexeme
        message = f"The character `{unknown_character}` is not known by the transpiler."
        super().__init__(error_type, message, location)


class UnterminatedFloatError(WodeError):
    def __init__(self, location: SourceRange) -> None:
        error_type = "UnterminatedFloatError"
        unterminated_float = location.lexeme
        message = f"The float `{unterminated_float}0` needs some numbers after its decimal point."
        super().__init__(error_type, message, location)


class NoLeadingZeroOnFloatError(WodeError):
    def __init__(self, location: SourceRange) -> None:
        error_type = "NoLeadingZeroOnFloatError"
        float_without_leading_zero = location
        message = f"The float `0{float_without_leading_zero}` needs a leading zero."
        super().__init__(error_type, message, location)


class UnexpectedEndOfExpressionError(WodeError):
    def __init__(self, location: SourcePosition) -> None:
        error_type = "UnexpectedEndOfExpressionError"
        message = "This expression ended unexpectedly."
        super().__init__(error_type, message, location)


class UnexpectedTokenTypeError(WodeError):
    def __init__(self, location: SourceRange) -> None:
        error_type = "UnexpectedTokenType"
        message = "This token type wasn't expected here."
        super().__init__(error_type, message, location)


class ExpectedSemicolonError(WodeError):
    def __init__(self, location: SourcePosition) -> None:
        error_type = "ExpectedSemicolonError"
        message = "A semicolon was expected, try adding a semicolon here."
        super().__init__(error_type, message, location)


class TooManyDecimalPointsError(WodeError):
    def __init__(self, location: SourceRange) -> None:
        error_type = "TooManyDecimalPointsError"
        float_with_too_many_decimal_points = location.lexeme
        message = f"The float `{float_with_too_many_decimal_points}` has too many decimal points."
        super().__init__(error_type, message, location)
