from itertools import accumulate
from typing import List


def get_lines(source: str) -> List[str]:
    return source.splitlines(keepends=True)


def get_line(source: str, line_number: int) -> str:
    return get_lines(source)[line_number - 1]


def get_line_number_of_position(source: str, position: int) -> int:
    lines = get_lines(source)
    line_lengths = (len(line) for line in lines)
    line_boundaries = accumulate(line_lengths)
    for line_number, line_boundary in enumerate(line_boundaries, start=1):
        if line_boundary > position:
            return line_number
    raise ValueError(f"Position {position} could not be found in source.")


def get_position_in_line(source: str, position: int) -> int:
    lines = get_lines(source)
    line_lengths = (len(line) for line in lines)
    line_boundaries = accumulate(line_lengths)

    previous_line_boundary = 0
    for line_boundary in line_boundaries:
        if line_boundary > position:
            return position - previous_line_boundary
        previous_line_boundary = line_boundary

    raise ValueError(f"Position {position} could not be found in source.")
