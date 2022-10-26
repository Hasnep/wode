from typing import TypeVar

from koda import Err, Ok, Result

S = TypeVar("S")
T = TypeVar("T")


def unwrap(r: Result[S, T]) -> S:
    return r.val
