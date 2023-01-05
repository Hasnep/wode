from itertools import accumulate
from pathlib import Path

from wode.types import Int, List, Optional, Str, Tuple, Union
from wode.utils import safe_substring


class LineNumber:
    def __init__(self, value: Int) -> None:
        if value <= 0:
            raise ValueError(f"Line number `{value}` must be greater than zero.")
        self.value = value

    def to_line_index(self) -> "LineIndex":
        return LineIndex(self.value - 1)

    def to_line_number(self) -> "LineNumber":
        return self


class LineIndex:
    def __init__(self, value: Int) -> None:
        if value < 0:
            raise ValueError(
                f"Line index `{value}` must be greater than or equal to zero."
            )
        self.value = value

    def to_line_index(self) -> "LineIndex":
        return self

    def to_line_number(self) -> "LineNumber":
        return LineNumber(self.value + 1)


class Column:
    def __init__(self, value: Int) -> None:
        if value < 0:
            raise ValueError(f"Column `{value}` must be greater than or equal to zero.")
        self.value = value


class Source:
    def __init__(self, file_path: Optional[Path], code: Str) -> None:
        self._file_path: Optional[Path] = file_path
        self._code = code
        self._lines = self.code.splitlines(keepends=True)

    @property
    def file_path(self) -> Optional[Path]:
        return self._file_path

    @property
    def code(self) -> Str:
        return self._code

    @property
    def lines(self) -> List[Str]:
        return self._lines

    def get_line(self, line_number: LineNumber) -> Str:
        return self._lines[line_number.to_line_index().value]


class SourcePosition:
    def __init__(self, source: Source, position: Int) -> None:
        self.source = source
        self.position = position

    @property
    def line_index(self) -> LineIndex:
        line_lengths = [len(line) for line in self.source.lines]
        line_end_positions = list(accumulate(line_lengths))

        # Get the index of the first line that ends after the specified position
        return next(
            LineIndex(line_index)
            for line_index, line_end_position in enumerate(line_end_positions)
            if line_end_position > self.position
        )

    @property
    def line_number(self) -> LineNumber:
        return self.line_index.to_line_number()

    @property
    def column(self) -> Column:
        line_lengths = [len(line) for line in self.source.lines]
        line_end_positions = list(accumulate(line_lengths))

        # The start of the line is the end of the previous line
        line_start_position = (
            0
            if self.line_index.value == 0
            else line_end_positions[self.line_index.value - 1]
        )
        # The column is the offset from the start of the line
        return Column(self.position - line_start_position)

    @property
    def coordinates(self) -> Tuple[LineNumber, Column]:
        return self.line_number, self.column

    @property
    def lexeme(self) -> Str:
        return safe_substring(self.source.code, start=self.position, length=1)

    def __str__(self) -> Str:
        return Str(self.line_number.value) + ":" + Str(self.column.value)


class SourceRange:
    def __init__(
        self,
        source: Source,
        start: Union[Int, SourcePosition],
        end: Union[Int, SourcePosition],
    ) -> None:
        self.source = source
        match start:
            case Int():
                self.start = SourcePosition(self.source, start)
            case SourcePosition():
                if start.source.code != self.source.code:
                    raise ValueError("Start position bad")
                self.start = start
        match end:
            case Int():
                self.end = SourcePosition(self.source, end)
            case SourcePosition():
                if end.source.code != self.source.code:
                    raise ValueError("End position bad")
                self.end = end

    @property
    def lexeme(self) -> Str:
        return safe_substring(
            self.source.code, start=self.start.position, end=self.end.position
        )

    def __len__(self) -> Int:
        return self.end.position - self.start.position
