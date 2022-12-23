from typing import List, Optional, TypeVar

from wode.constants import DIGITS, LETTERS, WHITESPACE_CHARACTERS

T = TypeVar("T")


def is_letter(c: str) -> bool:
    return c in LETTERS


def is_digit(c: str) -> bool:
    return c in DIGITS


def is_whitespace(c: str) -> bool:
    return c in WHITESPACE_CHARACTERS


def safe_slice(
    iterator: List[T],
    *,
    begin: int,
    length: Optional[int] = None,
    end: Optional[int] = None,
) -> List[T]:
    """Slice an iterator and raise an IndexError if you try to access an out of bounds index."""
    match (length, end):
        case (None, None):
            raise ValueError("One of `length` or `end` must be specified.")
        case (None, end):
            return [iterator[i] for i in range(begin, end)]  # type: ignore
        case (length, None):
            return [iterator[i] for i in range(begin, begin + length)]  # type: ignore
        case (length, end):
            raise ValueError("One of `length` or `end` must be specified.")


def safe_substring(
    s: str,
    *,
    begin: int,
    length: Optional[int] = None,
    end: Optional[int] = None,
) -> str:
    """Get a substring and raise an IndexError if you try to access an out of bounds index."""
    return "".join(safe_slice(list(s), begin=begin, length=length, end=end))


class UnreachableError(Exception):
    pass
