from typing import List, TypeVar

from koda import Err, Just, Maybe, Result, nothing

T = TypeVar("T")
S = TypeVar("S")


def get_errs(*results: Result[T, S]) -> List[Err[S]]:
    def _get_err(result: Result[T, S]) -> Maybe[Err[S]]:
        if isinstance(result, Err):
            return Just(result)
        else:
            return nothing

    errors = [_get_err(result) for result in results]
    return [err.val for err in errors if isinstance(err, Just)]
