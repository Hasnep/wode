from functools import reduce
from operator import concat
from typing import List, TypeVar

from koda import Err, Ok, Result

A = TypeVar("A")
B = TypeVar("B")


def flatten(nested_list: List[List[A]]) -> List[A]:
    flattened_list = reduce(concat, nested_list, [])  # type: ignore
    return list(flattened_list)  # type: ignore


def is_ok(result: Result[A, B]) -> bool:
    return isinstance(result, Ok)


def get_oks(results: List[Result[A, B]]) -> List[Ok[A]]:
    return [r for r in results if is_ok(r)]  # type: ignore


def is_err(result: Result[A, B]) -> bool:
    return isinstance(result, Err)


def get_errs(results: List[Result[A, B]]) -> List[Err[B]]:
    return [r for r in results if is_err(r)]  # type: ignore


def combine_errs(*errs: Err[List[B]]) -> Err[List[B]]:
    messages = flatten([e.val for e in errs])
    return Err(messages)
