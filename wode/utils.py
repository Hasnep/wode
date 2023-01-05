from wode.constants import DIGITS, LETTERS, WHITESPACE_CHARACTERS
from wode.types import Bool, Int, List, Optional, Str, TypeVar

T = TypeVar("T")


def is_letter(c: Str) -> Bool:
    return c in LETTERS


def is_digit(c: Str) -> Bool:
    return c in DIGITS


def is_whitespace(c: Str) -> Bool:
    return c in WHITESPACE_CHARACTERS


def safe_slice(
    iterator: List[T],
    *,
    start: Int,
    length: Optional[Int] = None,
    end: Optional[Int] = None,
) -> List[T]:
    """Slice an iterator and raise an IndexError if you try to access an out of bounds index."""
    match (length, end):
        case (None, None):
            raise ValueError("One of `length` or `end` must be specified.")
        case (None, end):
            return [iterator[i] for i in range(start, end)]  # type: ignore
        case (length, None):
            return [iterator[i] for i in range(start, start + length)]  # type: ignore
        case (length, end):
            raise ValueError("One of `length` or `end` must be specified.")


def safe_substring(
    s: Str,
    *,
    start: Int,
    length: Optional[Int] = None,
    end: Optional[Int] = None,
) -> Str:
    """Get a substring and raise an IndexError if you try to access an out of bounds index."""
    return "".join(safe_slice(List(s), start=start, length=length, end=end))


class UnreachableError(Exception):
    pass
